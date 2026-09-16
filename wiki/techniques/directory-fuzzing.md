---
type: technique
tags: [ejpt:web-pentest, ejpt:assessment]
tools: [gobuster]
cves: []
related: [[information-gathering]]
---

# Directory Fuzzing

Brute-forcing web paths to find hidden directories/files not linked anywhere.

## Command

```sh
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt
# or
dirb http://TARGET /usr/share/wordlists/dirb/common.txt
```

- `-x` adds extensions to test (e.g. `.php`, `.html`).
- Filter noise (403 `.htaccess`, default pages) with `--exclude-length`.

## Key finds

- `secret.php` in [[trust]], `backup/` and `important/` in [[obsession]], `dashboard`/`login`/`wow.zip` in [[los-3-hackers]], `uploads`/`upload` in [[baluhome]], `index.php` + listable `/pages/` in [[hannah-coffee]], `/admin`/`/console`/`/login`/`/logout` in [[balufood]], listable `/assets/` + `index.php` in [[psycho]].

## Seen in

[[hedgehog]], [[trust]], [[tproot]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[adopting]], [[baluhome]], [[simple-ctf]], [[ignite]], [[hannah-coffee]], [[balufood]], [[psycho]]
