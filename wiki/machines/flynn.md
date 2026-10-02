---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, ssh]
techniques: [information-gathering, hardcoded-credentials, sudo-abuse]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: [[acme]], [[littlepivoting]]
---

# Flynn

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/flynn.md)

Easy box that rewards trying the **dumbest credential first**: the SSH username doubles as the password, and a single `env` GTFOBins payload finishes it.

## Path

1. **Recon** — `ping -c 2` then `sudo nmap -p- --open -sS -sCV --min-rate 5000 -n -Pn` → `22/tcp` (OpenSSH 10.2p1 Ubuntu) and `80/tcp` (Apache 2.4.66, empty title) ([[information-gathering]]).
2. **Foothold (weak keys)** — no brute-force: `flynn` / `flynn` works directly on SSH — the classic *username = password* default ([[hardcoded-credentials]]).
3. **Privesc** — `sudo -l` → `(ALL) NOPASSWD: /usr/bin/env` → `sudo /usr/bin/env /bin/sh -p` → `whoami` = **root** ([[sudo-abuse]], [[gtfobins]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| `flynn` (SSH) | `flynn` |

## Takeaways

- **Before rockyou, try the username as the password** (and `admin:admin`, box name, etc.). Default/weak credentials are their own class — a dictionary attack on a box like this is wasted effort ([[hardcoded-credentials]]).
- `sudo -l` the moment you land — this box dies to a one-line [[gtfobins]] lookup on `env` (same payload family as [[littlepivoting]]'s `env /bin/bash`).
- `-p` on the spawned shell (`/bin/sh -p`) is what keeps the effective UID privileged when the interpreter would otherwise drop it.
