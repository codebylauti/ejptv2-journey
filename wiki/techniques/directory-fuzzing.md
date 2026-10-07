---
type: technique
tags: [ejpt:web-pentest, ejpt:assessment]
tools: [gobuster]
cves: []
related: ["[[information-gathering]]"]
---

# Directory Fuzzing

Brute-forcing web paths to find hidden directories/files not linked anywhere.

## Command

```sh
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt
# or
dirb http://TARGET /usr/share/wordlists/dirb/common.txt
```

- `-x` adds extensions to test (e.g. `.php`, `.html`).
- Filter noise (403 `.htaccess`, default pages) with `--exclude-length`.

## Key finds

- `secret.php` in [[trust]], `backup/` and `important/` in [[obsession]], `dashboard`/`login`/`wow.zip` in [[los-3-hackers]], `uploads`/`upload` in [[baluhome]], `index.php` + listable `/pages/` in [[hannah-coffee]], `/admin`/`/console`/`/login`/`/logout` in [[balufood]], listable `/assets/` + `index.php` in [[psycho]], `secret`/`imagenes`/`archives` in [[grooti]], `bills/` (login) + `intranet/` (401) + `proveedores/` in [[duque]], `config.php` (size 0 — silent DB config) in [[injection]], `wordpress/` (hidden CMS behind default page) in [[walkingcms]], `upload/` in [[anonymous-pingu]], `health` + `/api/pipelines` + `/api/jobs/{id}/trace` in [[pipepwned]], `shop/` in [[littlepivoting]] (→ `shop/index.php?archivo=` LFI) and `secret.php` on the pivoted `trust` host, `login` (405) + `static/` + `javascript/` + `logout` in [[madeyes-castle]], `data` + `ip` + `netstat` + `capture` (302 → `/data/1`, an object-ID leak) in [[cap]], `info` (plaintext hint naming an internal host) + `process.php` (500 on GET — a POST-only sink) + `server-status` (403) in [[dark]], `index.php` (1116 → **901** once you send the credential) behind a vhost in [[rutas]], `uploads/` (301) + `file_upload.php` (200, 468 — a *form renderer*, whose `action=` is a second, un-fuzzed endpoint) in [[file]], `index.php` (200, **26 bytes**) hiding in plain sight behind the default `index.html` (10671) in [[library]] — the root `<title>` said *"Apache2 Ubuntu Default Page: It works"*, and the real finding was the other `200` in the same run, `login` (200) + `builds` (200, 35 KB) + a fence of 403s (`script`, `configure`, `log`, `me`, `cloud`) mapping Jenkins's admin surface in [[secretjenkins]], `index.html` (200, 589 — while the root path itself 404s) + `notes/` (301 → the planted-pair `note.txt`) + `server-status` (403) in [[pkgpoison]], on [[elevator]] two passes: `themes/` + `javascript/` at the root, then one recursion into `themes/` finding `upload.php` (200, **0 B**) + `archivo.html` + `uploads/` — the entire foothold one level down, and in [[vulnvault]] `index.php` (200, 2832 — the injection) beside `upload.html` + `upload.php` (200, 33) + `old/` (301), three of which were **found and never visited**.

## Reading the statuses

- **500 with size 0 on a GET** is not "broken" — it's an endpoint that expects input (`process.php` on [[dark]]). A **200 with size 0** is its sibling: nothing renders, everything posts (`upload.php` on [[elevator]]).
- **403** (`server-status` on [[dark]]) means the path exists but is gated; worth a note, not a dead end — *unless the "path" is nonsense*. [[elevator]]'s run was full of `# license, visit http://creativecommons.org/…` entries: those are the **wordlist's own comment lines** being fuzzed as URLs, so the 403s belong to the list, not the server. Sanity-check weird hits against your wordlist before writing them down.
- **The same path at two sizes is a finding.** Re-fuzz *with* the credential you found (`-H "Authorization: Basic …"`) and a length filter (`--xl`/`-fs`); a `200` that shrinks from 1116 to 901 means the auth is real ([[rutas]], [[virtual-hosting]]).
- **A small `200` that renders a `<form>` is a lead, not a result.** Read its `action=` — that path is a *second* endpoint your wordlist probably never tested ([[file]]: `file_upload.php` renders, `subir_archivo.php` accepts).
- **The size outliers at both ends are findings.** Sort by size: a 26-byte `200` behind a 10671-byte default page was the entire secret on [[library]] — the default page was camouflage, and the smallest response held the token.
- **A cluster of 403s on app-shaped names is a floor plan.** `script`, `configure`, `log` all refusing you *before* you can log in proves an admin layer exists and hands you its exact URLs — Jenkins's own vocabulary in [[secretjenkins]]. Clustered 403s aren't dead ends; they're the map of the door you'll want after the exploit.
- **The root path is not the site.** `/` answered `404 Not Found` (nmap even reported it as the page title) while `/index.html` sat right there at 200 — fuzz before judging a host dead ([[pkgpoison]]).
- **Two hits in 1.66 M requests is an answer too.** When a thorough pass empties out — [[pequeñas-mentirosas]] got only `index.html` (85 B) + `server-status` across the whole DirBuster-medium list — stop hunting for deeper paths and re-read the bytes you already fetched: that 85-byte `index.html` was a hint naming the next attack surface (SSH user `a`). A near-empty result set means the content isn't *behind* a path.
- **Recurse into every directory the first pass finds.** A 301 is an invitation, not a result: [[elevator]]'s root pass showed only `themes/`, and one more `gobuster` run *on that path* uncovered `upload.php` — the entire foothold. The first pass finds the map; the second pass finds the door.

## Seen in

[[hedgehog]], [[trust]], [[tproot]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[adopting]], [[baluhome]], [[simple-ctf]], [[ignite]], [[hannah-coffee]], [[balufood]], [[psycho]], [[grooti]], [[duque]], [[injection]], [[walkingcms]], [[anonymous-pingu]], [[pipepwned]], [[littlepivoting]], [[madeyes-castle]], [[cap]], [[dark]], [[rutas]], [[file]], [[dockerlabs-box]], [[library]], [[secretjenkins]], [[pkgpoison]], [[elevator]]
