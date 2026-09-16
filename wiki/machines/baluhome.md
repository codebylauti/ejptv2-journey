---
type: machine
platform: dockerlabs
difficulty: hard
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, burp-suite, netcat]
techniques: [xss-and-cookie-theft, reverse-shells, cron-job-abuse, directory-fuzzing]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: [[adopting]], [[los-3-hackers]]
---

# BaluHome

Hard Node.js (Express) box chaining stored [[xss-and-cookie-theft|XSS → cookie theft]], an uploaded [[reverse-shells|Node reverse shell]], `su` brute-force, and a [[cron-job-abuse|writable backup script]].

## Path

1. **Recon** — `nmap` shows only `3000/tcp` (Node.js Express; a YouTube clone).
2. **Web enum** — [[gobuster]] finds `login`, `register`, `upload`, `uploads`, etc.
3. **XSS** — create an account; a stored XSS in the subtitle (`<script>alert()</script>`) works because cookies are not `HttpOnly`.
4. **Cookie theft** — a `.vtt` payload fetches the admin's cookie to an attacker listener; use it to impersonate the admin.
5. **Shell** — upload a `payload.js` reverse shell (Content-Type spoofed to `image/png` via [[burp-suite]]) → `www-data`.
6. **Pivot** — brute-force `su balutin` → `123123`.
7. **Escalation** — `balutin` is in the `mantenimiento` group with write access to `/opt/balutube-backup/backup.sh`; overwrite it with a reverse shell → root.

## Credentials

| User | Password |
|------|----------|
| balutin | `123123` |

## Takeaways

- Missing `HttpOnly`/`Secure` cookie flags make XSS trivially weaponizable for session theft ([[xss-and-cookie-theft]]).
- Content-Type spoofing is a classic file-upload bypass ([[reverse-shells]]).
- Group-writable automated scripts are a recurring root vector ([[cron-job-abuse]]).
