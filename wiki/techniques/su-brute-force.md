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
2. **Pick the target from the box itself:** `cat /etc/passwd | grep /bin/bash` lists every interactive shell account. On [[file]] that returned four named users in order — `fernando`, `mario`, `julen`, `iker` — which is a *queue* of hops to work through, not a curiosity.
3. Serve the script + wordlist from Kali: `python3 -m http.server 5000`.
4. Download and run it against the target user:
   ```sh
   ./Linux-Su-Force.sh seller rockyou.txt
   ```
5. Switch with the recovered password: `su seller`.
6. **Then re-enumerate as the new user** — `sudo -l`, `ls -l`, and any files in *their* home are all new ([[sudo-abuse]]).

## Seen in

[[littlepivoting]] (manchi → seller via Linux-Su-Force.sh), [[file]] (www-data → `fernando:chocolate` from rockyou; fernando's home then handed over the stego carrier for the next hop)
