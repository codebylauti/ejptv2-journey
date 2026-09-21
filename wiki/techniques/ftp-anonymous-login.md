---
type: technique
tags: [ejpt:host-net-pentest, ejpt:assessment]
tools: []
cves: []
related: [[ssh-bruteforce]]
---

# FTP Anonymous Login

Logging into an FTP service without credentials (`anonymous`) to read exposed files.

## Command

```sh
ftp TARGET
Name: anonymous
Password: (blank)
```

## What to look for

- Text files containing usernames, passwords, or hints (e.g. `chat-gonza.txt`, `pendientes.txt` in [[obsession]]).
- Password-protected archives (e.g. `secretitopicaron.zip` in [[nodeclimb]]) → crack with [[zip-cracking]].
- **Write access** — if the anonymous user can `put` files, upload a web shell into the webroot and trigger it over HTTP ([[anonymous-pingu]], see [[web-shell-upload]]).

## Seen in

[[obsession]], [[nodeclimb]], [[anonymous-pingu]]
