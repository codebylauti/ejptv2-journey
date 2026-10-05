---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: []
tools: [nmap, ssh]
techniques: [information-gathering, hardcoded-credentials, suid-enumeration]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: ["[[breakmyssh]]", "[[wargames]]"]
---

# ACME

**Writeup:** [raw writeup](../../writeups/dockerlabs/super-easy/acme.md)

Maintenance-portal box where the **SSH pre-auth banner hands you valid credentials**, then a SUID `bash` finishes it.

## Path

1. **Recon** — `ping` + `nmap -sS -sC -sV -p- --open -Pn` → `22/tcp` (OpenSSH 8.9p1 Ubuntu) and `80/tcp` (Apache 2.4.52, title *ACME Corporation - Portal en Mantenimiento*). The `-sC` scripts also flag `robots.txt` disallowing `/migration_notes.txt`.
2. **Foothold** — `ssh cualquier_usuario@172.17.0.2`: before prompting for a password, the MOTD banner prints the maintenance credentials (`usuario` / `P@ssw0rd2026_CTF!`). Log in as `usuario`.
3. **User flag** — `cat user.txt`.
4. **Escalation** — `find / -perm -4000 2>/dev/null | grep /bin/bash` → `/usr/bin/bash` is SUID; `/usr/bin/bash -p` spawns a root shell.
5. **Root flag** — `cat /root/root.txt`.

## Credentials

| Service | User | Password |
|---------|------|----------|
| SSH | usuario | `P@ssw0rd2026_CTF!` |

## Takeaways

- Service banners/MOTD can leak **live credentials before authentication** — connect with any username and read the whole banner ([[hardcoded-credentials]]).
- `nmap -sC`'s `http-robots.txt` script surfaces hidden paths (`/migration_notes.txt`) worth curling even when the landing page looks empty.
- SUID shells are the cheapest privesc: hunt with `find / -perm -4000`, then invoke with `-p` to keep the effective UID ([[suid-enumeration]], [[gtfobins]]).
