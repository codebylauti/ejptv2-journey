---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: ["[[ssh-bruteforce]]"]
---

# su Brute Force

Brute-forcing the password of another *local* user via `su`, from an existing foothold (no SSH/network login needed).

## Tool

`Linux-Su-Force.sh` — loops `su <user>` against a wordlist until it lands the password.

## Workflow

1. Get a foothold as any user (e.g. `manchi`).
2. Serve the script + wordlist from Kali: `python3 -m http.server 5000`.
3. Download and run it against the target user:
   ```sh
   ./Linux-Su-Force.sh seller rockyou.txt
   ```
4. Switch with the recovered password: `su seller`.

## Seen in

[[littlepivoting]] (manchi → seller via Linux-Su-Force.sh)
