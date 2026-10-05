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

- `secret.php` in [[trust]], `backup/` and `important/` in [[obsession]], `dashboard`/`login`/`wow.zip` in [[los-3-hackers]], `uploads`/`upload` in [[baluhome]], `index.php` + listable `/pages/` in [[hannah-coffee]], `/admin`/`/console`/`/login`/`/logout` in [[balufood]], listable `/assets/` + `index.php` in [[psycho]], `secret`/`imagenes`/`archives` in [[grooti]], `bills/` (login) + `intranet/` (401) + `proveedores/` in [[duque]], `config.php` (size 0 — silent DB config) in [[injection]], `wordpress/` (hidden CMS behind default page) in [[walkingcms]], `upload/` in [[anonymous-pingu]], `health` + `/api/pipelines` + `/api/jobs/{id}/trace` in [[pipepwned]], `shop/` in [[littlepivoting]] (→ `shop/index.php?archivo=` LFI) and `secret.php` on the pivoted `trust` host, `login` (405) + `static/` + `javascript/` + `logout` in [[madeyes-castle]], `data` + `ip` + `netstat` + `capture` (302 → `/data/1`, an object-ID leak) in [[cap]], `info` (plaintext hint naming an internal host) + `process.php` (500 on GET — a POST-only sink) + `server-status` (403) in [[dark]], `index.php` (1116 → **901** once you send the credential) behind a vhost in [[rutas]], `uploads/` (301) + `file_upload.php` (200, 468 — a *form renderer*, whose `action=` is a second, un-fuzzed endpoint) in [[file]].

## Reading the statuses

- **500 with size 0 on a GET** is not "broken" — it's an endpoint that expects input (`process.php` on [[dark]]).
- **403** (`server-status` on [[dark]]) means the path exists but is gated; worth a note, not a dead end.
- **The same path at two sizes is a finding.** Re-fuzz *with* the credential you found (`-H "Authorization: Basic …"`) and a length filter (`--xl`/`-fs`); a `200` that shrinks from 1116 to 901 means the auth is real ([[rutas]], [[virtual-hosting]]).
- **A small `200` that renders a `<form>` is a lead, not a result.** Read its `action=` — that path is a *second* endpoint your wordlist probably never tested ([[file]]: `file_upload.php` renders, `subir_archivo.php` accepts).

## Seen in

[[hedgehog]], [[trust]], [[tproot]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[adopting]], [[baluhome]], [[simple-ctf]], [[ignite]], [[hannah-coffee]], [[balufood]], [[psycho]], [[grooti]], [[duque]], [[injection]], [[walkingcms]], [[anonymous-pingu]], [[pipepwned]], [[littlepivoting]], [[madeyes-castle]], [[cap]], [[dark]], [[rutas]], [[file]]
