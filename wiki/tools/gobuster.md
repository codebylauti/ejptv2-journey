---
type: tool
category: scanner
related: [[directory-fuzzing]]
---

# Gobuster

Directory/file brute-forcer for web applications.

## Command

```sh
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt
```

- `dir` mode enumerates paths; `-x` appends extensions; `--exclude-length` filters noise.

## Seen in

[[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[adopting]], [[baluhome]], [[simple-ctf]], [[ignite]], [[tproot]], [[wargames]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[walkingcms]], [[anonymous-pingu]]
