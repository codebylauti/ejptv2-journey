---
type: technique
tags: [ejpt:web-pentest, ejpt:assessment]
tools: [ffuf]
cves: []
related: ["[[directory-fuzzing]]", "[[local-file-inclusion]]"]
---

# Parameter Fuzzing

Discovering hidden GET/POST parameters by brute-forcing parameter names.

## Command

```sh
ffuf -u "http://TARGET/index.php?FUZZ=test" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fw 198
```

- `FUZZ` marks the parameter name position.
- Filter by response size/words (`-fw`, `-fs`) to drop identical "not found" pages.

## Why it matters

- Sites may have undocumented parameters (e.g. `studio` in [[hannah-coffee]], `secret` in [[psycho]]) that expose LFI or other behavior.

## Seen in

[[hannah-coffee]] (hidden `studio` parameter → LFI), [[psycho]] (hidden `secret` parameter → LFI)
