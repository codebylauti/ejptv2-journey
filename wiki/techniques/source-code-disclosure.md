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
- **Backup/text files** — `backup.txt` leaking a username ([[obsession]]); `permission.txt` inside `wow.zip` ([[los-3-hackers]]); `instrucciones.txt` + `README.txt` leaking `rocket`/`password1` ([[grooti]]).
- **Image metadata/source** — username hidden in `imagen.jpeg` ([[borazuwara]]).
- **Config files** — `database.php` leaking a DB password ([[ignite]]); `app.py` Flask `secret_key` reused as an OS password ([[balufood]]); `config.php` returning `200` size 0 but `cat`-able once on-box, leaking MySQL `root`/`paso` ([[injection]]).
- **robots.txt** — reveals disallowed paths (`/fuel`, `/simple`) ([[ignite]], [[simple-ctf]]).
- **Exposed dotfiles/`.env`** — `.env_de_baluchingon` leaking `balu:balubalulerobalulei` ([[balulero]]).
- **Hidden-in-plain-sight attributes/CSS** — a username as a CSS property value (`top: pipe;`) and an `hidden="acrostico inicial"` clue ([[winfake]]).
- **Source leak via SQLi file-read** — `sqlmap --file-read` (or `LOAD_FILE`) pulls a PHP file's source through a blind SQLi, exposing hardcoded arrays/comments that hint at secrets ([[duque]]).
- **SSTI file-read** — RCE via [[server-side-template-injection]] lets you `cat` the runner's `.env` to extract SSH creds ([[pipepwned]]).
- **Plain hint files served as-is** — a no-extension `/info` text file naming the next host (`20.20.20.3`) and the narrative reason to visit it ([[dark]]).
- **Encoded pair in the page body** — no comment needed: the default index's *last line* is `user : pass` in base64, invisible until you `tail -1` the raw response ([[extraviado]], [[encoded-credentials]]).
- **Post-exploit source read** — `cat main.py` after a [[command-injection]] foothold exposes the in-memory `USERS` dict and `MFA_PINS` ([[trailpack]]).

## Seen in

[[hedgehog]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[ignite]], [[simple-ctf]], [[balufood]], [[balulero]], [[guided-pentest]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[pipepwned]], [[trailpack]], [[dark]], [[rutas]], [[extraviado]]
