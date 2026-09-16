---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, hydra]
techniques: [directory-fuzzing, ssh-bruteforce, sudo-abuse, source-code-disclosure]
tags: [ejpt:assessment, ejpt:host-net-pentest, ejpt:web-pentest]
related: [[vacaciones]], [[obsession]]
---

# HegdgeHog

Multi-user SSH box that chains [[directory-fuzzing]], [[ssh-bruteforce]], and a two-stage [[sudo-abuse|sudo escalation]].

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` and `80/tcp http` (Apache 2.4.58).
2. **Web enum** — [[gobuster]] finds only `index.html`; its content leaks a valid SSH username (`tails`).
3. **Brute force** — `hydra -l tails -P rockyou_reversed.txt` cracks the password.
4. **Escalation 1** — as `tails`, `sudo -l` shows `(sonic) NOPASSWD: ALL`; read `sonic`'s password file via `sudo -u sonic`.
5. **Escalation 2** — as `sonic`, `sudo -l` shows `(ALL) NOPASSWD: ALL`; `sudo su` → root.

## Credentials

| User | Password |
|------|----------|
| tails | `3117548331` |
| sonic | `perritos!` |

## Takeaways

- Usernames are often hidden in web page source — read `index.html` carefully ([[source-code-disclosure]]).
- `sudo -l` is the first thing to run after any foothold; here it yields two chained escalations ([[sudo-abuse]]).
