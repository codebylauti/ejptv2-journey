---
type: overview
related: [[dockerlabs]], [[tryhackme]], [[roadmap]]
---

# Overview

Current state of the cybersecurity learning vault.

## Progress snapshot

- **32 boxes** completed across two platforms: [[dockerlabs]] (27) and [[tryhackme]] (5).
- Difficulty spread is bottom-heavy: mostly **super-easy/easy**, with five intermediate ([[adopting]], [[pipepwned]], [[trailpack]], [[bruteshock]], [[littlepivoting]]) and one hard ([[baluhome]]).
- **1 box in progress** (not counted above): [[injection]] — foothold reached, privesc pending.

## Technique coverage so far

| Domain | Techniques exercised |
|--------|----------------------|
| Assessment | [[information-gathering]], [[directory-fuzzing]], [[parameter-fuzzing]], [[smb-enumeration]], [[mysql-enumeration]], [[source-code-disclosure]], [[acrostic-decoding]], [[ftp-anonymous-login]], [[hardcoded-credentials]] |
| Host & Network Pentest | [[ssh-bruteforce]], [[sudo-abuse]], [[arithmetic-injection]], [[exim-lpe]], [[python-library-hijacking]], [[suid-enumeration]], [[cron-job-abuse]], [[group-ownership-enumeration]], [[linux-capabilities]], [[writable-etc-passwd]], [[reverse-shells]], [[node-inspector-rce]], [[vsftpd-backdoor]], [[ssh-key-cracking]], [[zip-cracking]], [[hash-cracking]], [[hardcoded-credentials]], [[ftp-anonymous-login]], [[ci-cd-pipeline-abuse]], [[pivoting]], [[port-forwarding]], [[metasploit-pivoting]], [[su-brute-force]], [[path-hijacking]] |
| Web Pentest | [[sql-injection]], [[xss-and-cookie-theft]], [[web-cache-deception]], [[session-and-cookie-abuse]], [[broken-access-control]], [[local-file-inclusion]], [[log-poisoning]], [[parameter-fuzzing]], [[value-brute-force]], [[mfa-bruteforce]], [[directory-fuzzing]], [[source-code-disclosure]], [[acrostic-decoding]], [[prototype-pollution]], [[prompt-injection]], [[wordpress-enumeration]], [[web-shell-upload]], [[server-side-template-injection]], [[command-injection]], [[shellshock]], [[http-login-bruteforce]], [[virtual-hosting]] |

## Notable gaps (see [[roadmap]])

- **Pivoting** now covered via [[littlepivoting]] (Metasploit `route`/`portfwd` — [[metasploit-pivoting]], [[pivoting]], [[port-forwarding]]). **Remaining:** manual chisel/proxychains + SSH tunneling (documented, not yet exercised).
- **Active Directory / network-level attacks** still minimal.
- Metasploit now used beyond [[guided-pentest]] (full pivoting in [[littlepivoting]]).
- No hands-on **password cracking of OS hashes** (`/etc/shadow`, NTLM) — raw-hash cracking is now covered via [[hash-cracking]] ([[wargames]]), but OS credential-store hashes remain untried.
- Web pentesting still light on **SSRF and CSRF** (command injection now covered via [[command-injection]]; IDOR/broken access control via [[broken-access-control]]; SSTI via [[pipepwned]]; LFI/[[log-poisoning]] via [[hannah-coffee]]; [[prototype-pollution]] via [[autoescuela]]). SQLi depth is improving — time-based blind + `--file-read` via [[sqlmap]] added in [[duque]]; verbose `SQLSTATE` error-based detection in [[injection]]; **SQLite UNION** (`sqlite_master` + `group_concat`) in [[madeyes-castle]]. CMS coverage includes [[wordpress-enumeration]] ([[walkingcms]]). Vhost discovery now covered via [[virtual-hosting]].

The learning path and next steps are tracked in [[roadmap]].
