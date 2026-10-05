---
type: overview
related: ["[[dockerlabs]]", "[[tryhackme]]", "[[roadmap]]"]
---

# Overview

Current state of the cybersecurity learning vault.

## Progress snapshot

- **42 boxes** completed across three platforms: [[dockerlabs]] (36), [[tryhackme]] (5), and [[hack-the-box]] (1).
- Difficulty spread is bottom-heavy: mostly **super-easy/easy**, with ten intermediate ([[adopting]], [[pipepwned]], [[trailpack]], [[bruteshock]], [[littlepivoting]], [[domain]], [[chmod-4755]], [[dance-samba]], [[dark]], [[rutas]]) and one hard ([[baluhome]]).
- **1 box in progress** (not counted above): [[injection]] — foothold reached, privesc pending.

## Technique coverage so far

| Domain | Techniques exercised |
|--------|----------------------|
| Assessment | [[information-gathering]], [[directory-fuzzing]], [[parameter-fuzzing]], [[smb-enumeration]], [[mysql-enumeration]], [[source-code-disclosure]], [[pcap-analysis]], [[acrostic-decoding]], [[ftp-anonymous-login]], [[hardcoded-credentials]], [[steganography]] |
| Host & Network Pentest | [[ssh-bruteforce]], [[sudo-abuse]], [[arithmetic-injection]], [[exim-lpe]], [[python-library-hijacking]], [[suid-enumeration]], [[cron-job-abuse]], [[group-ownership-enumeration]], [[linux-capabilities]], [[writable-etc-passwd]], [[writable-motd]], [[reverse-shells]], [[restricted-shell-escape]], [[node-inspector-rce]], [[vsftpd-backdoor]], [[ssh-key-cracking]], [[zip-cracking]], [[hash-cracking]], [[hardcoded-credentials]], [[ftp-anonymous-login]], [[ci-cd-pipeline-abuse]], [[pivoting]], [[port-forwarding]], [[metasploit-pivoting]], [[su-brute-force]], [[path-hijacking]] |
| Web Pentest | [[sql-injection]], [[xss-and-cookie-theft]], [[web-cache-deception]], [[session-and-cookie-abuse]], [[broken-access-control]], [[local-file-inclusion]], [[remote-file-inclusion]], [[server-side-request-forgery]], [[log-poisoning]], [[parameter-fuzzing]], [[value-brute-force]], [[mfa-bruteforce]], [[directory-fuzzing]], [[source-code-disclosure]], [[acrostic-decoding]], [[prototype-pollution]], [[prompt-injection]], [[wordpress-enumeration]], [[web-shell-upload]], [[server-side-template-injection]], [[command-injection]], [[waf-bypass]], [[shellshock]], [[http-login-bruteforce]], [[virtual-hosting]] |

## Notable gaps (see [[roadmap]])

- **Pivoting** covered twice via [[littlepivoting]] (Metasploit `route`/`portfwd` and a fully manual re-run with [[chisel]] + [[proxychains]] + [[socat]]) and again via [[dark]] (`ping_sweep` → `portscan/tcp` → `portfwd`). **Remaining:** SSH tunneling (`-D`/`-L`/`-R`, documented not yet exercised).
- **Active Directory / network-level attacks** still minimal.
- Metasploit now used beyond [[guided-pentest]] (full pivoting in [[littlepivoting]]).
- No hands-on **password cracking of OS hashes** (`/etc/shadow`, NTLM) — raw-hash cracking is now covered via [[hash-cracking]] ([[wargames]]), but OS credential-store hashes remain untried.
- Web pentesting now has a first **SSRF** sighting ([[server-side-request-forgery]] via [[dark]] — one `url` parameter that is both an SSRF and an LFI), but only the "fetch an internal URL and reflect it" shape: no `127.0.0.1` service target, no cloud metadata, no protocol smuggling. **RFI** now has its first sighting too ([[remote-file-inclusion]] via [[rutas]] — the *same* input classifies by URL shape: local path → LFI, `http://…` → fetch → SSRF, fetched **script executed** → RFI, which is why the LFI wordlist came back empty there). **CSRF** still unseen (command injection now covered via [[command-injection]]; IDOR/broken access control via [[broken-access-control]] — the IDOR half documented from [[cap]]; SSTI via [[pipepwned]]; LFI/[[log-poisoning]] via [[hannah-coffee]]; [[prototype-pollution]] via [[autoescuela]]). SQLi depth is improving — time-based blind + `--file-read` via [[sqlmap]] added in [[duque]]; verbose `SQLSTATE` error-based detection in [[injection]]; **SQLite UNION** (`sqlite_master` + `group_concat`) in [[madeyes-castle]]. CMS coverage includes [[wordpress-enumeration]] ([[walkingcms]]). Vhost discovery now covered via [[virtual-hosting]], including `gobuster vhost` subdomain fuzzing ([[internal]]), and filter evasion via [[waf-bypass]].

The learning path and next steps are tracked in [[roadmap]].
