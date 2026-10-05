---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, sqlmap, gtfobins]
techniques: [directory-fuzzing, sql-injection, source-code-disclosure, hardcoded-credentials, suid-enumeration]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[los-3-hackers]]", "[[grooti]]"]
---

# Duque

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/duque.md)

Easy box: SQLi auth bypass on a login → sqlmap time-based blind + `--file-read` leaks a source-code secret → SSH in with found creds → `env` SUID to root.

## Path

1. **Recon** — `nmap -p- -sS -sV -sC` shows `22/tcp` (OpenSSH 8.9p1) and `80/tcp` (Apache 2.4.52, "NaturGas Solutions - Dashboard Corporativo").
2. **Web enum** — [[gobuster]] finds `bills/` (login page), `intranet/` (401 unauthorized), `proveedores/`, and `index.php` ([[directory-fuzzing]]).
3. **SQLi auth bypass** — the `/bills/` login concatenates input raw. `username=admin'--` + any password returns `Login success: Admin` and redirects to `panel.php` ([[sql-injection]]).
4. **SQLi data extraction** — [[sqlmap]] on the `username` POST param ([[curl]] to drive the form) confirms a **time-based blind** (MySQL ≥ 5.0.12 / MariaDB, `SLEEP`). Dumps DB `register` → table `users` with three plaintext creds (`mario`/`jesus`/`admin`), none of which escalate beyond the panel.
5. **File read** — `sqlmap --file-read "/var/www/html/bills/panel.php"` leaks the source. It contains a hardcoded `$database` array of IDs where one entry is commented `// ID vulnerable`: `xyc724`. Passing that ID to `panel.php?id=` reveals the SSH credentials for user `duque` ([[source-code-disclosure]], [[hardcoded-credentials]]).
6. **SSH login** — `ssh duque@172.17.0.2` with the leaked password.
7. **Privesc** — `find / -perm -4000` shows `/usr/bin/env` is SUID. `env /bin/sh -p` spawns a **root** shell ([[suid-enumeration]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| `register.users` (Mario) | `mario123` |
| `register.users` (Jesus) | `jesus2026` |
| `register.users` (Admin) | `admin123` |
| `duque` (SSH) | leaked via `panel.php?id=xyc724` |

## Takeaways

- The login's raw concatenation (`admin'--`) is the *same* bug sqlmap then escalates into a full data + file extraction ([[sql-injection]]).
- `--file-read` turned a blind SQLi into a **source-code disclosure**: the `// ID vulnerable` comment was a breadcrumb to the SSH password ([[source-code-disclosure]]).
- Time-based blind is the *slowest* SQLi channel — it's the last resort when the server doesn't echo errors or results ([[sqlmap]]).
- `env` is a classic GTFOBins SUID payload (`env /bin/sh -p`) — see [[gtfobins]] ([[suid-enumeration]]).
