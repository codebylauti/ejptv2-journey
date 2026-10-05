---
type: technique
tags: [ejpt:web-pentest]
tools: []
cves: []
related: ["[[reverse-shells]]", "[[ftp-anonymous-login]]", "[[directory-fuzzing]]"]
---

# Web Shell Upload

Gaining RCE by writing a malicious script into a web-accessible directory, then requesting it over HTTP.

## Workflow

1. Find a way to **write** files into the webroot. Common vectors:
   - **Anonymous FTP** with upload permission → `put payload.php` ([[ftp-anonymous-login]]).
   - A web upload form with missing/misconfigured validation.
   - A **writable SMB share mapped to the site directory** — no HTTP attack needed: `smbclient //TARGET/html -U bob --password=star` → `put payload.php` ([[domain]]).
2. Upload a shell — e.g. the pentestmonkey PHP reverse shell, or a one-liner `<?php system($_GET['cmd']); ?>`.
3. Request it over HTTP to trigger execution. Locate the directory first with [[directory-fuzzing]] (e.g. an `upload/` path).

## Notes

- The FTP (or SMB) share and the webroot may be the *same* directory — that shared path is the whole trick in [[anonymous-pingu]] and [[domain]].
- Mind the extension: `.php` must *execute*, not download. A `.php.txt` or server misconfig silently breaks the payload.
- Chain straight into [[reverse-shells]] for an interactive foothold.

## Seen in

[[anonymous-pingu]], [[littlepivoting]] (PHP reverse shell uploaded to `/uploads/payload.php` on `upload`), [[domain]] (`payload.php` via SMB write to the `html` share → `www-data`)
