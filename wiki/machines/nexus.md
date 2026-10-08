---
type: machine
platform: hack-the-box
difficulty: easy
ip: 10.129.158.122
cves: [CVE-2026-38526]
tools: [nmap, gobuster, curl, ssh, netcat, find]
techniques: [information-gathering, virtual-hosting, source-code-disclosure, hardcoded-credentials, web-shell-upload, reverse-shells, cron-job-abuse, git-tree-path-traversal]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[hack-the-box]]", "[[virtual-hosting]]", "[[source-code-disclosure]]", "[[hardcoded-credentials]]", "[[web-shell-upload]]", "[[reverse-shells]]", "[[git-tree-path-traversal]]", "[[cve-2026-38526]]"]
---

# Nexus

**Writeup:** [raw writeup](../../writeups/hack-the-box/easy/nexus.md)

Easy HTB box: vhost fuzzing splits `nexus.htb` into a Gitea instance and a Krayin CRM — a repo's **commit history** yields the CRM admin password → **CVE-2026-38526** unrestricted PHP upload → `www-data` → on-disk `.env` password → `su jones` → root via a Gitea template-sync timer that materializes git tree entries with `..` path traversal into `/root/.ssh/authorized_keys`.

## Path

1. **Recon** — `ping -c 2` then `sudo nmap -p- --open -sS --min-rate 5000 -n -Pn` → `22/tcp` (OpenSSH 9.6p1 Ubuntu), `80/tcp` (nginx 1.24.0) whose `http-title` note — *"Did not follow redirect to http://nexus.htb/"* — hands you the base domain for `/etc/hosts` ([[information-gathering]]).
2. **Vhost enum** — `gobuster vhost -w subdomains-top1million-5000.txt -u http://nexus.htb --append-domain` → `git.nexus.htb` (200) and `billing.nexus.htb` (302 → `/admin/login`); both mapped in `/etc/hosts` ([[virtual-hosting]], [[gobuster]]).
3. **Source disclosure** — `git clone http://git.nexus.htb/admin/krayin-docker-setup` (anonymous clone of an exposed Gitea repo): at HEAD `.env` has `DB_PASSWORD=` **blanked**, but the **commit history** still carries `N27xh!!2ucY04` ([[source-code-disclosure]]).
4. **CRM login** — `j.matthew@nexus.htb:N27xh!!2ucY04` on `billing.nexus.htb/admin/login` → dashboard shows **Krayin CRM 2.2.0** ([[hardcoded-credentials]]).
5. **RCE via upload** — **CVE-2026-38526** unrestricted PHP upload: compose a mail (`POST /admin/mail/create`) with `attachments[]` = pentestmonkey `rev.php` → the JSON response hands back the public URL `http://billing.nexus.htb/storage/emails/1/rev.php` → GET it with `sudo nc -lvnp 443` listening → `www-data` ([[web-shell-upload]], [[reverse-shells]]).
6. **Lateral to jones** — `find / -name .env` → `/var/www/krayin/.env` → `DB_PASSWORD=y27xb3ha!!74GbR` → `su jones` → `/home/jones/user.txt` ([[hardcoded-credentials]], [[find]]).
7. **Privesc discovery** — `systemctl list-timers` → `gitea-template-sync.timer` firing every minute (→ `gitea-template-sync.service`); `/etc/gitea/template-sync.py` clones Gitea **template** repos and materializes tree entries without normalizing `..` ([[cron-job-abuse]]).
8. **Root** — sign in to Gitea as `jones`, create a repo marked *Make repository a template*, force-push a crafted commit whose tree embeds `..` entries building `root/.ssh/authorized_keys` with an attacker key → `ssh -i /tmp/.k root@nexus.htb` → `/root/root.txt` ([[git-tree-path-traversal]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| `j.matthew@nexus.htb` (Krayin CRM admin) | `N27xh!!2ucY04` — `DB_PASSWORD` recovered from the Gitea repo's commit history (HEAD is blank) |
| `jones` (local `su` + Gitea login) | `y27xb3ha!!74GbR` — `DB_PASSWORD` in `/var/www/krayin/.env` |
| root (SSH) | keypair `/tmp/.k` (ed25519, no passphrase), planted via git tree traversal |

## Takeaways

- **Blanking a secret at HEAD does not delete it.** The repo's tip commit had an empty `DB_PASSWORD`; the real value sat one revision back. An exposed git remote is a disclosure vector *even when the current tree is clean* — always walk `git log -p` on any cloned repo ([[source-code-disclosure]], [[hardcoded-credentials]]).
- **One application, two credential stores.** The repo's stale `.env` (history) opened the CRM; the *live* on-disk `/var/www/krayin/.env` yielded a different password that became `jones`'s login — replay every recovered secret against every surface that accepts it ([[hardcoded-credentials]]).
- **An upload response that echoes the stored URL is your trigger path.** The mail-attachment JSON returned `storage/emails/1/rev.php` directly — no directory fuzzing needed to find the shell ([[web-shell-upload]]).
- **Enumerate systemd timers, not just cron.** `systemctl list-timers` is the systemd twin of `crontab -l`: every `.timer` names a `.service` worth reading, and root's scheduled jobs are where one-box privescs hide ([[cron-job-abuse]]).
- **Automation trusts repository data as filesystem paths.** Git happily stores tree entries named `..`; a sync job that joins them onto its workspace without normalization writes attacker-chosen content — here, an `authorized_keys` — to an arbitrary root-owned path. The payload is *data*, not a script ([[git-tree-path-traversal]]).
