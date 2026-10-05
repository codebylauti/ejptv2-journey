---
type: machine
platform: tryhackme
difficulty: easy
ip: 10.67.173.54
cves: [CVE-2021-47980, CVE-2018-16763]
tools: [nmap, gobuster, netcat]
techniques: [sql-injection, reverse-shells, suid-enumeration, directory-fuzzing, source-code-disclosure]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[simple-ctf]]", "[[los-3-hackers]]"]
---

# Ignite

**Writeup:** [raw writeup](../../writeups/tryhackme/ignite.md)

TryHackMe box exploiting Fuel CMS 1.4 ([[sql-injection|SQLi]] + RCE) and a hardcoded database credential.

## Path

1. **Recon** — only `80/tcp` (Apache 2.5.18).
2. **Web enum** — `/fuel` (Fuel CMS), `/robots.txt` (disallows `/fuel`), default creds `admin:admin`.
3. **Exploit 1** — [[cve-2021-47980]]: SQLi in the `col=` param of `/fuel/logs`.
4. **Exploit 2** — [[cve-2018-16763]]: unauthenticated RCE → reverse shell as `www-data`.
5. **Escalation** — [[suid-enumeration|SUID]] scan, then read `/var/www/html/fuel/application/config/database.php` to find a password (`mememe`); `su -` to root.

## Credentials

| User | Password |
|------|----------|
| fuel admin | `admin` / `admin` |
| root (via su) | `mememe` |

## Takeaways

- Fuel CMS 1.4 has both a SQLi and an RCE — a two-for-one ([[cve-2021-47980]], [[cve-2018-16763]]).
- Config files (`database.php`) frequently leak credentials ([[source-code-disclosure]]).
