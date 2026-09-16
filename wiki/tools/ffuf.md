---
type: tool
category: fuzzer
related: [[parameter-fuzzing]]
---

# ffuf

Fast web fuzzer for directories, parameters, virtual hosts, and more.

## Command

```sh
ffuf -u "http://TARGET/index.php?FUZZ=test" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fw 198
```

## Seen in

[[hannah-coffee]] (hidden `studio` parameter discovery), [[psycho]] (hidden `secret` parameter)
