---
type: technique
tags: [ejpt:web-pentest, ejpt:assessment]
tools: [curl]
cves: []
related: ["[[directory-fuzzing]]"]
---

# Source Code Disclosure

Extracting secrets (usernames, passwords, hints) from exposed source files.

## Vectors

- **HTML comments** — `<!-- De : Juan Para: Camilo ... -->` ([[vacaciones]]); "same username for all services" ([[obsession]]); `<!-- Backup de acceso: sysadmin:backup123 -->` ([[balufood]]); *"nos han vuelto a romper"* + *"lo hace todo muy obvio"* — plus an `<aside>` of three candidate vhostnames ([[rutas]]).
- **Backup/text files** — `backup.txt` leaking a username ([[obsession]]); `permission.txt` inside `wow.zip` ([[los-3-hackers]]); `instrucciones.txt` + `README.txt` leaking `rocket`/`password1` ([[grooti]]); `notes/note.txt` an admin's reminder that doubles as a planted pair — `dev:developer123`, already rotated by the time you replay it ([[pkgpoison]], [[hardcoded-credentials]]).
- **Image metadata/source** — username hidden in `imagen.jpeg` ([[borazuwara]]).
- **Config files** — `database.php` leaking a DB password ([[ignite]]); `app.py` Flask `secret_key` reused as an OS password ([[balufood]]); `config.php` returning `200` size 0 but `cat`-able once on-box, leaking MySQL `root`/`paso` ([[injection]]).
- **robots.txt** — reveals disallowed paths (`/fuel`, `/simple`) ([[ignite]], [[simple-ctf]]).
- **Exposed dotfiles/`.env`** — `.env_de_baluchingon` leaking `balu:balubalulerobalulei` ([[balulero]]).
- **Hidden-in-plain-sight attributes/CSS** — a username as a CSS property value (`top: pipe;`) and an `hidden="acrostico inicial"` clue ([[winfake]]); `class="hidden"` spans pairing a **username and password** (`jenkins-admin` / `cassandra`), with the image `alt`s repeating both words — and the words themselves naming the service on a *different* port ([[jenkhack]]).
- **Source leak via SQLi file-read** — `sqlmap --file-read` (or `LOAD_FILE`) pulls a PHP file's source through a blind SQLi, exposing hardcoded arrays/comments that hint at secrets ([[duque]]).
- **SSTI file-read** — RCE via [[server-side-template-injection]] lets you `cat` the runner's `.env` to extract SSH creds ([[pipepwned]]).
- **Plain hint files served as-is** — a no-extension `/info` text file naming the next host (`20.20.20.3`) and the narrative reason to visit it ([[dark]]).
- **Encoded pair in the page body** — no comment needed: the default index's *last line* is `user : pass` in base64, invisible until you `tail -1` the raw response ([[extraviado]], [[encoded-credentials]]).
- **Post-exploit source read** — `cat main.py` after a [[command-injection]] foothold exposes the in-memory `USERS` dict and `MFA_PINS` ([[trailpack]]).
- **Compiled artifacts** — no `.py` needed: Python's `__pycache__/x.cpython-38.pyc` keeps every string literal in its constant pool, so `strings` on the bytecode hands back the credentials the source would have ([[pkgpoison]] → `admin`/`p@$$w0r8321` via [[strings]]). Compilation strips whitespace, not secrets — if `find` turns up a `.pyc`, treat it as readable source.
- **Visible body text — nothing hidden at all** — disclosure can mean simply *reading* the rendered page: a security-news feed narrates an employee's firing for emailing a password and signs another entry from "Carlota, Departamento de ciberseguridad", beside a "weak password detected" notice → two usernames and a brute-force mandate, with no comment, backup, or attribute involved ([[amor]]). If the page tells a story about people, the people are candidate accounts.

## Seen in

[[hedgehog]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[ignite]], [[simple-ctf]], [[balufood]], [[balulero]], [[guided-pentest]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[pipepwned]], [[trailpack]], [[dark]], [[rutas]], [[extraviado]], [[jenkhack]], [[amor]], [[pkgpoison]]
