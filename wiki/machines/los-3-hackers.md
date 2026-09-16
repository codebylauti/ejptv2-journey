---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl]
techniques: [sql-injection, session-and-cookie-abuse, cron-job-abuse, linux-capabilities, reverse-shells, directory-fuzzing, source-code-disclosure]
tags: [ejpt:assessment, ejpt:host-net-pentest, ejpt:web-pentest]
related: [[baluhome]], [[ignite]]
---

# Los 3 Hackers

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/los-3-hackers.md)

Three-user machine themed around three hacker mentalities, chaining [[sql-injection|SQLi]], a session cookie, a writable cron script, and [[linux-capabilities|Linux capabilities]].

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` and `80/tcp http` (Gunicorn).
2. **SQLi** — bypass the login form with `username=admin'--` → admin dashboard (first flag).
3. **Session abuse** — use the admin session cookie to download `wow.zip`; it contains `redhacker`'s SSH credentials.
4. **Pivot (redhacker → bluehacker)** — a note points to an internal portal; enumeration reveals `bluehacker`'s password in an HTML file.
5. **Pivot (bluehacker → blackhacker)** — a [[cron-job-abuse|writable cron script]] (`/opt/maintenance/m.sh`) is overwritten with a [[reverse-shells|reverse shell]] to become `blackhacker`.
6. **Escalation** — `getcap -r /` finds `/usr/local/bin/syscheck cap_setuid=ep`; abuse it to spawn a root shell.

## Credentials

| User | Password |
|------|----------|
| redhacker | `h4ck1NNN62026!!` |
| bluehacker | `xKpIEAE3fkp--` |

## Takeaways

- `admin'--` is the canonical auth-bypass SQLi payload ([[sql-injection]]).
- Session cookies can unlock protected files (`wow.zip`).
- Writable cron scripts and `cap_setuid` are two distinct [[cron-job-abuse]] / [[linux-capabilities]] privesc routes.
