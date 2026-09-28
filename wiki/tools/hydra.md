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
- **Through a SOCKS tunnel:** wrap the whole command — `proxychains hydra -l <user> -P rockyou.txt TARGET ssh` ([[proxychains]]).

## HTTP form brute force (`http-post-form`)

```sh
hydra -l admin -P rockyou.txt TARGET http-post-form \
  "/index.php:username=^USER^&password=^PASS^:H=Cookie: PHPSESSID=xxx:F=Credenciales incorrectas."
```

- `F=` = failure text; `H=` = a header (session cookie) injected per attempt.

## Seen in

[[breakmyssh]], [[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[basic-pentesting]], [[simple-ctf]], [[grooti]], [[winfake]], [[bruteshock]], [[littlepivoting]] (SSH `manchi`/`mario`, second host via `portfwd`'d `127.0.0.1:2200`; manual re-run via `proxychains`), [[madeyes-castle]] (`smb2` brute-force → `avadakedavra:123456`)
