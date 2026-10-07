---
type: technique
tags: [ejpt:web-pentest]
tools: [ffuf]
cves: []
related: ["[[reverse-shells]]", "[[ftp-anonymous-login]]", "[[directory-fuzzing]]"]
---

# Web Shell Upload

Gaining RCE by writing a malicious script into a web-accessible directory, then requesting it over HTTP.

## Workflow

1. Find a way to **write** files into the webroot. Common vectors:
   - **Anonymous FTP** with upload permission → `put payload.php` ([[ftp-anonymous-login]]).
   - A web upload form — usually surfaced by [[directory-fuzzing]] as a small `200` page (e.g. `file_upload.php` on [[file]]).
   - A **writable SMB share mapped to the site directory** — no HTTP attack needed: `smbclient //TARGET/html -U bob --password=star` → `put payload.php` ([[domain]]).
2. **Work out what the form will accept** (next section) before you pick a payload.
3. Upload a shell — e.g. the pentestmonkey PHP reverse shell, or a one-liner `<?php system($_GET['cmd']); ?>`.
4. Request it over HTTP to trigger execution. Locate the directory first with [[directory-fuzzing]] (e.g. an `upload/` path).

## Finding the accepted extension

The form tells you *where* to upload, never *what* will be allowed. Fuzz the filename's extension with [[ffuf]] — and note that the `FUZZ` keyword has to live **inside the multipart body**, after the dot:

- Build the body by hand: `-H "Content-Type: multipart/form-data; boundary=…"` plus `-d $'…filename="probe.FUZZ"…'`. A plain urlencoded `-d "archivo=probe.php"` lands in `$_POST` and never touches `$_FILES`, so *every* response looks identical and you conclude "nothing works" when you simply never reached the upload check.
- **Calibrate on the rejection, not on a 404.** Upload one thing the filter refuses, measure it, and `-fs` that number. When every answer is `200`, length is the only signal left — the single entry that *disagrees* with the baseline is your answer.
- **A refusal *message* is an oracle too.** When the filter answers with a fixed sentence ("*No se permite la subida de archivos que no sean .zip*"), fuzz until that exact sentence *disappears* — same calibration as `-fs`, phrased in words instead of bytes. [[dockerlabs-box]] did it with a hand-rolled bash loop over `web-extensions.txt` + `grep -q`; ffuf would express it as a negative filter.
- Watch for the **two endpoints**: the page that renders the `<form>` and the `action=` that accepts the file are different paths. Fuzz the action.

## Notes

- The FTP (or SMB) share and the webroot may be the *same* directory — that shared path is the whole trick in [[anonymous-pingu]] and [[domain]].
- Mind the extension: the extension must *execute*, not download. A `.php.txt` or server misconfig silently breaks the payload.
- **Ask what the server runs, not what the filter allows.** An allow-list that excludes `.php` may still permit `.phar`, `.phtml`, or `.php5` — all of which PHP executes by default. On [[file]] the fuzz never surfaced `.php`; the winner was **`phar`**, and requesting `/uploads/revshell.phar` gave `www-data`. **Two boxes, same ending** — [[dockerlabs-box]] (a `.zip`-only rule, same one-word answer) repeated it, which makes `phar` the *first* extension to test on any PHP upload filter.
- **The allow-list reads the name you *send*.** When the refusal is a literal extension rule ("*Solo se permiten archivos con la extensión .jpg*"), the declared filename is client-controlled: `curl -F "file=@shell.php;filename=revshell.jpg"` declares `.jpg` while the body stays PHP. [[elevator]] accepted it, renamed it to a random hash (`6ac67879e7091.jpg` — the response link is your only pointer), and the GET **executed** it — meaning `.jpg` was wired to the PHP handler there. Same sentence, two readings: the filter checks *names*, the server decides *execution*, and neither was checked properly. (The handler config was never read — recorded as a gap on [[elevator]].)
- Chain straight into [[reverse-shells]] for an interactive foothold.

## Seen in

[[anonymous-pingu]], [[littlepivoting]] (PHP reverse shell uploaded to `/uploads/payload.php` on `upload`), [[domain]] (`payload.php` via SMB write to the `html` share → `www-data`), [[file]] (multipart extension fuzz → `phar` → `/uploads/revshell.phar` → `www-data`), [[dockerlabs-box]] (refusal-phrase fuzz → `phar` again → `/uploads/revshell.phar` → `www-data`), [[elevator]] (`.jpg`-only allow-list → `;filename=` override → hash-renamed `6ac67879e7091.jpg` → executed → `www-data`)
