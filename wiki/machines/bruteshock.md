---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 172.17.0.2
cves: [CVE-2014-6271]
tools: [nmap, gobuster, hydra, curl, john-the-ripper, netcat, gtfobins]
techniques: [directory-fuzzing, http-login-bruteforce, shellshock, reverse-shells, hash-cracking, hardcoded-credentials, sudo-abuse, arithmetic-injection, exim-lpe, writable-etc-passwd]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[trailpack]]", "[[pipepwned]]"]
---

# BruteShock

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/bruteshock.md)

Intermediate box: a [[shellshock]] foothold on Apache, then a long **multi-hop sudo chain** — darksblack → maci → pepe → root — each hop a different misconfiguration (arithmetic injection, exim expansion, dos2unix file-overwrite).

## Path

1. **Recon** — `nmap` shows `80/tcp` (Apache 2.4.62 Debian, PHP/`PHPSESSID`).
2. **Web enum** — [[gobuster]] finds only `server-status` (403); the login lives on `/index.php` ([[directory-fuzzing]]).
3. **Login brute force** — [[hydra]] `http-post-form` → `admin:christelle` ([[http-login-bruteforce]]).
4. **Shellshock** — `User-Agent: () { :;}; /bin/bash -c …` on `/pruebasUltraSecretas/` → RCE ([[shellshock]], [[cve-2014-6271]]) → reverse shell as `www-data` ([[reverse-shells]], `nohup … &` to detach from the short-lived request).
5. **www-data → darksblack** — `/var/backups/darksblack/.darksblack.txt` leaks a `/etc/shadow`-format yescrypt hash ([[hardcoded-credentials]]); crack with `john --format=crypt` → `darksblack:salvador1` ([[hash-cracking]]).
6. **darksblack → maci** — `sudo -l`: `(maci) /home/maci/script.sh`; the script's `[[ $num -eq 123123 ]]` is [[arithmetic-injection]]-vulnerable → `a[$(/bin/bash -p >&2)]` ([[sudo-abuse]]).
7. **maci → pepe** — `sudo -l`: `(pepe) /usr/sbin/exim`; `exim -be '${run{…}}'` executes commands as pepe ([[exim-lpe]]).
8. **pepe → root** — `sudo -l`: `(ALL) /usr/bin/dos2unix`; `dos2unix -f -n /tmp/passwd.new /etc/passwd` blanks root's password → `su -` ([[writable-etc-passwd]], [[gtfobins]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| web login | `admin` / `christelle` |
| `darksblack` | `salvador1` (yescrypt, john) |
| `pepe` | uid 1002 (via exim) |
| `root` | via blanked `/etc/passwd` |

## Takeaways

- `() { :;};` in a header → [[shellshock]] RCE on any vulnerable-bash CGI.
- A sudo'd script using `[[ $var -eq N ]]` is [[arithmetic-injection]] (use `==` to be safe).
- Exim's `${run{}}` is a command-execution primitive even on patched builds ([[exim-lpe]]).
- `dos2unix -f -n` is a GTFOBins file-overwrite → blank `/etc/passwd` root ([[writable-etc-passwd]]).
