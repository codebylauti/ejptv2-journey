---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, netcat, gtfobins]
techniques: [ftp-anonymous-login, directory-fuzzing, web-shell-upload, reverse-shells, sudo-abuse, writable-etc-passwd]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[nodeclimb]]", "[[adopting]]"]
---

# Anonymous Pingu

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/anonymous-pingu.md)

Easy box: anonymous FTP **upload** → PHP reverse shell, then a three-hop `sudo` lateral-movement chain (`man` → `nmap` → `chown`) ending in a password-less root via `/etc/passwd`.

## Path

1. **Recon** — `nmap` shows `21/tcp ftp` (vsftpd 3.0.5) and `80/tcp` (Apache).
2. **Anonymous FTP** — `ftp anonymous` logs in with **write** access ([[ftp-anonymous-login]]).
3. **Web enum** — [[gobuster]] finds an `upload/` directory.
4. **Foothold** — `put` a PHP reverse shell into the webroot via FTP, then trigger it over HTTP → `www-data` ([[web-shell-upload]], [[reverse-shells]]).
5. **→ pingu** — `sudo -l` shows `(pingu) NOPASSWD: /usr/bin/man`; spawn a shell with `!/bin/bash` inside `man`.
6. **→ gladys** — `sudo -l` shows `(gladys) NOPASSWD: /usr/bin/nmap`; abuse `nmap --script` with an NSE `os.execute` to drop a shell.
7. **→ root** — `sudo -l` shows `(root) NOPASSWD: /usr/bin/chown`; take ownership of `/etc/passwd`, `chmod 777`, blank root's password (`root:x:` → `root::`), then `su -` ([[writable-etc-passwd]]).

## Sudo chain

| From | `sudo -l` reveals | Escalation |
|------|-------------------|------------|
| www-data | `(pingu) /usr/bin/man` | `sudo -u pingu man man` → `!/bin/bash` |
| pingu | `(gladys) /usr/bin/nmap` | NSE script `os.execute("/bin/sh <&1 >&1 2>&1")` |
| gladys | `(root) /usr/bin/chown` | chown `/etc/passwd` → blank root password → `su -` |

## Takeaways

- Anonymous FTP **write** to the webroot is a foothold: upload a web shell, then request it over HTTP ([[web-shell-upload]]).
- `man`, `nmap --script`, and `chown` are all GTFOBins entries — any of them in `sudo -l` is an escalation ([[sudo-abuse]]).
- `chown` alone doesn't grant root; but owning `/etc/passwd` lets you blank root's password ([[writable-etc-passwd]]).
