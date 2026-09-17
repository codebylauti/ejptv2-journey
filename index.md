# Index

Content catalog. Read this first on any query.

## Overview

- [[overview]] — synthesis of current progress and gaps

## Platforms

- [[dockerlabs]] — DockerLabs platform page + completed boxes
- [[tryhackme]] — TryHackMe platform page + completed boxes

## Machines

### DockerLabs — super-easy

- [[breakmyssh]] — SSH brute-force to root
- [[first-hacking]] — vsftpd 2.3.4 backdoor
- [[hedgehog]] — web source leak → SSH brute-force → chained sudo
- [[trust]] — gobuster → hydra → sudo vim
- [[tproot]] — vsftpd 2.3.4 backdoor
- [[obsession]] — anonymous FTP + web hints → sudo vim
- [[vacaciones]] — HTML comment usernames → sudo ruby
- [[borazuwara]] — image metadata username → sudo group

### DockerLabs — easy

- [[los-3-hackers]] — SQLi → session → cron → capabilities
- [[hannah-coffee]] — LFI + log poisoning → debugfs → capabilities
- [[balufood]] — leaked creds → secret_key reuse → .bashrc alias
- [[balulero]] — .env leak → sudo php → group-owned script → root
- [[nodeclimb]] — anon FTP → zip crack → sudo node writable script
- [[psycho]] — LFI → SSH key → chained sudo (perl → python3)
- [[autoescuela]] — Node.js Inspector RCE → React2Shell (CVE-2025-55182)
- [[wargames]] — prompt injection → hash crack → SUID binary
- [[grooti]] — MySQL leak → value brute-force → SSH brute-force → cron
- [[winfake]] — CSS username leak → SSH brute-force → acrostic root password

### DockerLabs — intermediate

- [[adopting]] — web cache deception → writable /etc/passwd

### DockerLabs — hard

- [[baluhome]] — XSS → cookie theft → Node reverse shell → cron abuse

### TryHackMe

- [[basic-pentesting]] — SMB enum → SSH brute-force → key cracking
- [[simple-ctf]] — CMS Made Simple SQLi → sudo vim
- [[ignite]] — Fuel CMS SQLi + RCE → config credential
- [[guided-pentest]] — UnrealIRCd via Metasploit

## Techniques

- [[information-gathering]] — ping + nmap recon
- [[directory-fuzzing]] — gobuster/dirb web path enumeration
- [[parameter-fuzzing]] — ffuf hidden parameter discovery
- [[value-brute-force]] — brute-force a param value, spot the odd response by length
- [[local-file-inclusion]] — LFI path traversal
- [[log-poisoning]] — inject code into logs → RCE via LFI
- [[ssh-bruteforce]] — hydra dictionary attack on SSH
- [[ftp-anonymous-login]] — anonymous FTP file access
- [[sudo-abuse]] — sudo -l + GTFOBins escalation
- [[python-library-hijacking]] — shadow Python imports via writable path
- [[suid-enumeration]] — setuid binary hunting
- [[vsftpd-backdoor]] — CVE-2011-2523 trigger
- [[sql-injection]] — auth bypass + CMS SQLi
- [[xss-and-cookie-theft]] — stored XSS → session theft
- [[web-cache-deception]] — cache poisoning for sensitive pages
- [[cron-job-abuse]] — writable cron scripts
- [[group-ownership-enumeration]] — find group-writable files (find -group)
- [[linux-capabilities]] — getcap + cap_setuid abuse
- [[writable-etc-passwd]] — password-less root entry
- [[reverse-shells]] — bash/Node reverse shells
- [[node-inspector-rce]] — RCE via Node.js Inspector (CDP, port 9229)
- [[smb-enumeration]] — enum4linux user/share discovery
- [[mysql-enumeration]] — MySQL/MariaDB enumeration (SHOW/DESCRIBE/SELECT)
- [[ssh-key-cracking]] — john on SSH key passphrases
- [[zip-cracking]] — zip2john + john on encrypted ZIPs
- [[hash-cracking]] — raw hash → plaintext (john/hashcat + online lookup)
- [[source-code-disclosure]] — comments, backups, configs, metadata
- [[hardcoded-credentials]] — hardcoded/reused credentials, shell history & aliases
- [[session-and-cookie-abuse]] — stolen/forged session tokens
- [[acrostic-decoding]] — first letters of headings spell a hidden password
- [[prototype-pollution]] — React2Shell: RSC Flight deserialization → Function() RCE
- [[prompt-injection]] — AI/chatbot instruction override → data leak

## Tools

- [[nmap]] — scanner
- [[curl]] — HTTP client
- [[gobuster]] — directory brute-forcer
- [[dirb]] — directory brute-forcer
- [[ffuf]] — parameter/path fuzzer
- [[hydra]] — login brute-forcer
- [[john-the-ripper]] — hash/key cracker
- [[burp-suite]] — intercepting proxy
- [[metasploit]] — exploitation framework
- [[searchsploit]] — Exploit-DB search
- [[enum4linux]] — SMB enumerator
- [[netcat]] — reverse-shell listener / network utility
- [[telnet]] — TCP client / manual banner grab
- [[mysql]] — MySQL/MariaDB client
- [[gtfobins]] — sudo/SUID payload reference

## CVEs

- [[cve-2011-2523]] — vsftpd 2.3.4 backdoor
- [[cve-2019-9053]] — CMS Made Simple SQLi
- [[cve-2018-16763]] — Fuel CMS RCE
- [[cve-2021-47980]] — Fuel CMS SQLi
- [[cve-2025-55182]] — React2Shell: RSC Flight deserialization RCE

## Learning

- [[roadmap]] — eJPTv2 learning path + checklist
