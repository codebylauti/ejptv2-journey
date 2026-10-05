---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, burp-suite]
techniques: [web-cache-deception, writable-etc-passwd, directory-fuzzing]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[baluhome]]"]
---

# Adopting

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/adopting.md)

Intermediate box demonstrating [[web-cache-deception]] and a [[writable-etc-passwd]] privilege escalation.

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` and `2300/tcp` (unrecognized HTTP web app).
2. **Web enum** — [[gobuster]] on port 2300 finds `assets/`, `products/`, `static/`.
3. **Match & Replace** — in [[burp-suite]], swapping `role=user` → `role=admin` exposes an admin "Panel de Operaciones", but the backend still denies access.
4. **Cache deception** — responses carry `X-Cache: HIT`; a `credentials-report.pdf` is cached. Trick an admin into visiting a crafted URL so the cached PDF becomes retrievable.
5. **SSH login** — the report leaks credentials (`pingu` / `chocolate`).
6. **Escalation** — the `pinguinos` group can write `/etc/passwd`; replace root's entry with `root::0:0:root:/root:/bin/sh` (empty password), then `su` to root.

## Credentials

| User | Password |
|------|----------|
| pingu | `chocolate` |

## Takeaways

- `X-Cache` headers signal cache-based attacks ([[web-cache-deception]]).
- A group-writable `/etc/passwd` is an instant root via a password-less entry ([[writable-etc-passwd]]).
