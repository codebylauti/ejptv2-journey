---
type: technique
tags: [ejpt:web-pentest]
tools: [curl, searchsploit]
cves: [CVE-2019-9053, CVE-2021-47980]
related: [[cve-2019-9053]], [[cve-2021-47980]]
---

# SQL Injection

Injecting SQL into input fields or query parameters to bypass auth or extract data.

## Variants seen

- **Auth bypass** — `username=admin'--` in a login form ([[los-3-hackers]]).
- **CMS SQLi** — CMS Made Simple 2.2.8 ([[cve-2019-9053]]) leaks salt/username/hash ([[simple-ctf]]).
- **Time-based / param SQLi** — Fuel CMS `col=` parameter ([[cve-2021-47980]]) ([[ignite]]).

## Notes

- Pair with a CMS version banner → `searchsploit <cms>` for a ready exploit.
- Auth bypass payloads: `admin'--`, `admin' OR '1'='1`.

## Seen in

[[los-3-hackers]], [[simple-ctf]], [[ignite]]
