---
type: technique
tags: [ejpt:web-pentest]
tools: [curl]
cves: []
related: ["[[log-poisoning]]", "[[parameter-fuzzing]]"]
---

# Local File Inclusion (LFI)

Including arbitrary local files via an unsanitized include/read parameter.

## Detection

- A URL parameter that controls page content (e.g. `?page=`, `?file=`, `?lang=`) may be injectable.
- Test with path traversal: `../../../etc/passwd`.

## Read files

```sh
curl -s "http://TARGET/index.php?param=../../../etc/passwd"
```

- Read SSH keys for a foothold: `?param=../../home/user/.ssh/id_rsa` ([[psycho]]).

## Same parameter, two bugs

Some sinks are a plain `file_get_contents($input)` — the *input itself* picks the behaviour: a bare word or `../` path reads a local file (this page), while `http://…` makes the server fetch a remote/internal URL ([[server-side-request-forgery]]). Test both schemes before you classify the parameter ([[dark]]).

If the fetched remote content is **executed** rather than echoed, you've crossed from SSRF into [[remote-file-inclusion]] — decide by what you can make it do, not by the URL shape ([[rutas]]).

## Chain to RCE

- Pair with [[log-poisoning]] to execute injected code.
- Or include `/proc/self/environ` with a poisoned User-Agent.

## Seen in

[[hannah-coffee]] (`?studio=../../../etc/passwd`), [[psycho]] (`?secret=` → `/etc/passwd` and `id_rsa`), [[littlepivoting]] (`?archivo=` → `/etc/passwd`, fuzzed with [[ffuf]] `LFI-Jhaddix.txt`), [[dark]] (POST `url=///////../../../etc/passwd` — same field also does SSRF), [[rutas]] (negative result: `LFI-Jhaddix.txt` through `?love=` came back empty because the sink wanted a URL — see [[remote-file-inclusion]])
