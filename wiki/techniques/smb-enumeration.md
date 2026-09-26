---
type: technique
tags: [ejpt:assessment, ejpt:auditing]
tools: [enum4linux]
cves: []
related: [[ssh-bruteforce]]
---

# SMB Enumeration

Enumerating SMB shares and users, a rich source of account names for later brute-force.

## Command

```sh
enum4linux TARGET
# or, for a NULL session + share listing
smbmap -H TARGET
smbclient //TARGET/share -N
```

## What to extract

- Valid usernames (e.g. `jan`, `kay` in [[basic-pentesting]]).
- Share names and permissions.
- Files inside readable shares — including **hidden dotfiles** (`.notes.txt`) that hold hints for later steps ([[madeyes-castle]]).

## Seen in

[[basic-pentesting]], [[madeyes-castle]] (anon `sambashare` → `spellnames.txt` + `.notes.txt`)
