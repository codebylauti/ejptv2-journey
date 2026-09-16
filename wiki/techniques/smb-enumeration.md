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
```

## What to extract

- Valid usernames (e.g. `jan`, `kay` in [[basic-pentesting]]).
- Share names and permissions.

## Seen in

[[basic-pentesting]]
