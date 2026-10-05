---
type: technique
tags: [ejpt:host-net-pentest, ejpt:assessment]
tools: []
cves: []
related: ["[[ssh-bruteforce]]"]
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

- Text files containing usernames, passwords, or hints (e.g. `chat-gonza.txt`, `pendientes.txt` in [[obsession]]). Read them as *data*: `nota.txt` — *"Macarena, she's obsessed with donald"* — was literally `macarena:donald`, user and password in one sentence ([[dance-samba]]).
- **File *names* too** — a 0-byte file still says something (`hola_disfruta` = "enjoy", `respeta.zip` = "respect"), and the pair often reads as an instruction ([[rutas]]).
- Password-protected archives (e.g. `secretitopicaron.zip` in [[nodeclimb]]) → crack with [[zip-cracking]].
- **A bare hash with no label.** `anon.txt` on [[file]] held nothing but `53dd9c6005f3cdfc5a69c5c07388016d` — no username, no `=` padding, no context. Length alone identifies it (32 hex = MD5) and `john --format=raw-MD5` turns it into a *username* (`justin`), which is a lead, not a credential ([[hash-cracking]]).
- **Write access** — if the anonymous user can `put` files, upload a web shell into the webroot and trigger it over HTTP ([[anonymous-pingu]], see [[web-shell-upload]]).

## Seen in

[[obsession]], [[nodeclimb]], [[anonymous-pingu]], [[dance-samba]], [[rutas]], [[file]]
