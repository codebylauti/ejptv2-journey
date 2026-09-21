---
type: technique
tags: [ejpt:web-pentest]
tools: [curl, searchsploit, sqlmap]
cves: [CVE-2019-9053, CVE-2021-47980]
related: [[cve-2019-9053]], [[cve-2021-47980]], [[source-code-disclosure]]
---

# SQL Injection

Injecting SQL into input fields or query parameters to bypass auth or extract data.

## Variants seen

- **Auth bypass** — `username=admin'--` in a login form ([[los-3-hackers]], [[duque]]); `name=' OR 1=1 '` ([[injection]]).
- **Error-based** — a bare `'` triggers a verbose `SQLSTATE[42000]` error that leaks the query shape (`... AND passwd = '...'`) ([[injection]]).
- **CMS SQLi** — CMS Made Simple 2.2.8 ([[cve-2019-9053]]) leaks salt/username/hash ([[simple-ctf]]).
- **Time-based / param SQLi** — Fuel CMS `col=` parameter ([[cve-2021-47980]]) ([[ignite]]).
- **Time-based blind** — the server returns no error and no data; a `SLEEP(n)` payload makes TRUE/FALSE observable via response *timing* ([[duque]]).
- **File read via SQLi** — `sqlmap --file-read` (or `LOAD_FILE`) reads server files through the injection point, turning a blind SQLi into [[source-code-disclosure]] ([[duque]]).

## Notes

- Pair with a CMS version banner → `searchsploit <cms>` for a ready exploit.
- Auth bypass payloads: `admin'--`, `admin' OR '1'='1`.
- A **verbose DB error** is a gift — it confirms SQLi *and* leaks the query structure in one request. Grep for `SQLSTATE`/`1064`.
- When a bare `'` does *not* 500 the page, don't rule out SQLi — it may be **blind**. Test TRUE vs FALSE (`1=1` vs `1=2`) or timing (`SLEEP`).
- The four detection channels: error-based, UNION-based, boolean-blind, time-blind — time is the slowest, so prefer it last.

## Seen in

[[los-3-hackers]], [[simple-ctf]], [[ignite]], [[duque]], [[injection]]
