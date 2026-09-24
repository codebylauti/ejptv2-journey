---
type: overview
related: [[dockerlabs]], [[tryhackme]], [[roadmap]]
---

# Overview

Current state of the cybersecurity learning vault.

## Progress snapshot

- **30 boxes** completed across two platforms: [[dockerlabs]] (26) and [[tryhackme]] (4).
- Difficulty spread is bottom-heavy: mostly **super-easy/easy**, with four intermediate ([[adopting]], [[pipepwned]], [[trailpack]], [[bruteshock]]) and one hard ([[baluhome]]).
- **1 box in progress** (not counted above): [[injection]] — foothold reached, privesc pending.

## Technique coverage so far

| Domain | Techniques exercised |
|--------|----------------------|
| Assessment | [[information-gathering]], [[directory-fuzzing]], [[parameter-fuzzing]], [[smb-enumeration]], [[mysql-enumeration]], [[source-code-disclosure]], [[acrostic-decoding]], [[ftp-anonymous-login]], [[hardcoded-credentials]] |
| Host & Network Pentest | [[ssh-bruteforce]], [[sudo-abuse]], [[arithmetic-injection]], [[exim-lpe]], [[python-library-hijacking]], [[suid-enumeration]], [[cron-job-abuse]], [[group-ownership-enumeration]], [[linux-capabilities]], [[writable-etc-passwd]], [[reverse-shells]], [[node-inspector-rce]], [[vsftpd-backdoor]], [[ssh-key-cracking]], [[zip-cracking]], [[hash-cracking]], [[hardcoded-credentials]], [[ftp-anonymous-login]], [[ci-cd-pipeline-abuse]] |
| Web Pentest | [[sql-injection]], [[xss-and-cookie-theft]], [[web-cache-deception]], [[session-and-cookie-abuse]], [[broken-access-control]], [[local-file-inclusion]], [[log-poisoning]], [[parameter-fuzzing]], [[value-brute-force]], [[mfa-bruteforce]], [[directory-fuzzing]], [[source-code-disclosure]], [[acrostic-decoding]], [[prototype-pollution]], [[prompt-injection]], [[wordpress-enumeration]], [[web-shell-upload]], [[server-side-template-injection]], [[command-injection]], [[shellshock]], [[http-login-bruteforce]] |

## Notable gaps (see [[roadmap]])

- Minimal **Active Directory / pivoting / network-level attacks** (localhost-only service discovery seen in [[autoescuela]]).
- Metasploit only lightly touched ([[guided-pentest]]).
- No hands-on **password cracking of OS hashes** (`/etc/shadow`, NTLM) — raw-hash cracking is now covered via [[hash-cracking]] ([[wargames]]), but OS credential-store hashes remain untried.
- Web pentesting still light on **SSRF and CSRF** (command injection now covered via [[command-injection]]; IDOR/broken access control via [[broken-access-control]]; SSTI via [[pipepwned]]; LFI/[[log-poisoning]] via [[hannah-coffee]]; [[prototype-pollution]] via [[autoescuela]]). SQLi depth is improving — time-based blind + `--file-read` via [[sqlmap]] added in [[duque]]; verbose `SQLSTATE` error-based detection in [[injection]]. CMS coverage now includes [[wordpress-enumeration]] ([[walkingcms]]).

The learning path and next steps are tracked in [[roadmap]].
