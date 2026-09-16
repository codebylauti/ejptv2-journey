---
type: technique
tags: [ejpt:web-pentest, ejpt:assessment]
tools: [curl]
cves: []
related: [[directory-fuzzing]]
---

# Source Code Disclosure

Extracting secrets (usernames, passwords, hints) from exposed source files.

## Vectors

- **HTML comments** — `<!-- De : Juan Para: Camilo ... -->` ([[vacaciones]]); "same username for all services" ([[obsession]]); `<!-- Backup de acceso: sysadmin:backup123 -->` ([[balufood]]).
- **Backup/text files** — `backup.txt` leaking a username ([[obsession]]); `permission.txt` inside `wow.zip` ([[los-3-hackers]]); `instrucciones.txt` + `README.txt` leaking `rocket`/`password1` ([[grooti]]).
- **Image metadata/source** — username hidden in `imagen.jpeg` ([[borazuwara]]).
- **Config files** — `database.php` leaking a DB password ([[ignite]]); `app.py` Flask `secret_key` reused as an OS password ([[balufood]]).
- **robots.txt** — reveals disallowed paths (`/fuel`, `/simple`) ([[ignite]], [[simple-ctf]]).
- **Exposed dotfiles/`.env`** — `.env_de_baluchingon` leaking `balu:balubalulerobalulei` ([[balulero]]).

## Seen in

[[hedgehog]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[ignite]], [[simple-ctf]], [[balufood]], [[balulero]], [[guided-pentest]], [[grooti]]
