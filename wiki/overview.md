---
type: overview
related: [[dockerlabs]], [[tryhackme]], [[roadmap]]
---

# Overview

Current state of the cybersecurity learning vault.

## Progress snapshot

- **24 boxes** completed across two platforms: [[dockerlabs]] (20) and [[tryhackme]] (4).
- Difficulty spread is bottom-heavy: mostly **super-easy/easy**, with one intermediate ([[adopting]]) and one hard ([[baluhome]]).

## Technique coverage so far

| Domain | Techniques exercised |
|--------|----------------------|
| Assessment | [[information-gathering]], [[directory-fuzzing]], [[parameter-fuzzing]], [[smb-enumeration]], [[mysql-enumeration]], [[source-code-disclosure]], [[acrostic-decoding]], [[ftp-anonymous-login]], [[hardcoded-credentials]] |
| Host & Network Pentest | [[ssh-bruteforce]], [[sudo-abuse]], [[python-library-hijacking]], [[suid-enumeration]], [[cron-job-abuse]], [[group-ownership-enumeration]], [[linux-capabilities]], [[writable-etc-passwd]], [[reverse-shells]], [[node-inspector-rce]], [[vsftpd-backdoor]], [[ssh-key-cracking]], [[zip-cracking]], [[hash-cracking]], [[hardcoded-credentials]], [[ftp-anonymous-login]] |
| Web Pentest | [[sql-injection]], [[xss-and-cookie-theft]], [[web-cache-deception]], [[session-and-cookie-abuse]], [[local-file-inclusion]], [[log-poisoning]], [[parameter-fuzzing]], [[value-brute-force]], [[directory-fuzzing]], [[source-code-disclosure]], [[acrostic-decoding]], [[prototype-pollution]], [[prompt-injection]] |

## Notable gaps (see [[roadmap]])

- Minimal **Active Directory / pivoting / network-level attacks** (localhost-only service discovery seen in [[autoescuela]]).
- Metasploit only lightly touched ([[guided-pentest]]).
- No hands-on **password cracking of OS hashes** (`/etc/shadow`, NTLM) — raw-hash cracking is now covered via [[hash-cracking]] ([[wargames]]), but OS credential-store hashes remain untried.
- Web pentesting still light on **SSRF, IDOR, CSRF, and command injection** (LFI/[[log-poisoning]] now covered via [[hannah-coffee]]; [[prototype-pollution]] added via [[autoescuela]]).

The learning path and next steps are tracked in [[roadmap]].
