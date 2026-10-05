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
- **Filter on both sides of a boundary.** Compare the same URL authenticated vs not before you set `-fs`: on [[rutas]] `index.php` was 1116 bytes out, 901 in — that delta is what tells you the credential mattered, and 901/1079 are exactly the sizes you then filter away.
- **A silent fuzz may mean the wrong vocabulary.** Feeding an LFI path wordlist at a parameter that wants `scheme://…` returns nothing ([[remote-file-inclusion]]).

## Seen in

[[hannah-coffee]] (hidden `studio` parameter → LFI), [[psycho]] (hidden `secret` parameter → LFI), [[rutas]] (parameter-name fuzz → `love`, then a URL-shaped value → [[remote-file-inclusion]])
