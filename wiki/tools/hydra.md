---
type: tool
category: bruteforcer
related: [[ssh-bruteforce]]
---

# Hydra

Fast network login cracker supporting SSH, FTP, HTTP, and more.

## Command

```sh
hydra -l <user> -P /usr/share/wordlists/rockyou.txt ssh://TARGET -t 4
```

- `-l` single login, `-L` list; `-P` password list.
- `-t` tasks; keep low (e.g. 4) for SSH to avoid throttling.

## Seen in

[[breakmyssh]], [[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[basic-pentesting]], [[simple-ctf]]
