# Index

Content catalog. Read this first on any query.

## Overview

- [[overview]] — synthesis of current progress and gaps

## Platforms

- [[dockerlabs]] — DockerLabs platform page + completed boxes
- [[tryhackme]] — TryHackMe platform page + completed boxes
- [[hack-the-box]] — Hack The Box platform page + completed boxes

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
- [[acme]] — SSH banner credential leak → SUID bash

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
- [[duque]] — SQLi bypass → sqlmap file-read → SSH → env SUID
- [[injection]] — error-based SQLi → SSH → ⚠️ incomplete (privesc pending)
- [[walkingcms]] — WordPress → wpscan brute-force → theme-editor shell → env SUID
- [[anonymous-pingu]] — anon FTP upload → PHP shell → chained sudo (man → nmap → chown)
- [[internal]] — 303 vhost leak → WAF blacklist bypass → reverse shell → leaked wordlist → vaultctl
- [[flynn]] — default SSH creds → sudo `env`
- [[analyst]] — pcap triage (tshark) → captured SSH creds → sudo ALL
- [[file]] — anon FTP hash → upload extension fuzz (`.phar`) → reverse shell → su spray → steghide → 3-hop sudo chain
- [[extraviado]] — base64 default-page creds → SSH → `find` password files → riddle root
- [[dockerlabs-box]] — upload refusal fuzz (`.phar`) → reverse shell → sudo `grep` file read → root
- [[jenkhack]] — hidden-span creds → Jenkins script console → ASCII85 → sudo wrapper overwrite
- [[library]] — default-page camouflage → 26-byte token → inverted SSH brute → Python import hijack
- [[secretjenkins]] — Jenkins 2.441 file-read CVE → user enum → SSH brute → chained sudo (python3)
- [[amor]] — news-feed usernames → SSH brute → steghide + base64 → sudo ruby
- [[pkgpoison]] — stale planted creds → hydra → `.pyc` strings leak → sudo pip3 wildcard
- [[elevator]] — `.jpg` filename-lie upload → RCE → 6-hop sudo chain (env → ash → ruby → lua → gcc → sudo)
- [[pequeñas-mentirosas]] — page hint → hydra → `find` username hash → sudo python3
- [[vulnvault]] — report-form injection as a file reader → stolen SSH key → world-writable `echo.sh` PID 1 loop

### DockerLabs — intermediate

- [[adopting]] — web cache deception → writable /etc/passwd
- [[pipepwned]] — SSTI → `.env` creds → root gitlab-runner abuse
- [[trailpack]] — MFA brute-force → cookie role tampering → command injection → SUID env
- [[bruteshock]] — Shellshock → 5-hop sudo chain (arithmetic injection → exim → dos2unix)
- [[littlepivoting]] — 3-host pivoting chain, done twice (Metasploit routing + manual chisel/socat/proxychains)
- [[domain]] — SMB enum → nxc spray → writable share → SUID nano (reclassified from easy)
- [[chmod-4755]] — SMB hints → rbash escape → SUID curl overwrites /etc/passwd
- [[dance-samba]] — FTP note hint → SMB spray → writable home share → SSH key → sudo `file` read
- [[dark]] — one `url` param = SSRF + LFI → SSH brute-force → Metasploit pivot → `cmd` RCE → SUID curl
- [[rutas]] — anon FTP → zip crack → steghide → Basic-auth vhost → `love` param → RFI → PATH hijack → writable MOTD

### DockerLabs — hard

- [[baluhome]] — XSS → cookie theft → Node reverse shell → cron abuse

### TryHackMe

- [[basic-pentesting]] — SMB enum → SSH brute-force → key cracking
- [[simple-ctf]] — CMS Made Simple SQLi → sudo vim
- [[ignite]] — Fuel CMS SQLi + RCE → config credential
- [[guided-pentest]] — UnrealIRCd via Metasploit
- [[madeyes-castle]] — vhost → SQLite UNION SQLi → SHA-512 crack → pico sudo → SUID PATH-hijack

### Hack The Box

- [[cap]] — IDOR → pcap credential leak → FTP/SSH → python `cap_setuid`

## Techniques

- [[information-gathering]] — ping + nmap recon
- [[directory-fuzzing]] — gobuster/dirb web path enumeration
- [[parameter-fuzzing]] — ffuf hidden parameter discovery
- [[value-brute-force]] — brute-force a param value, spot the odd response by length
- [[mfa-bruteforce]] — brute-force an OTP/MFA code, bypass the rate limiter via X-Forwarded-For
- [[local-file-inclusion]] — LFI path traversal
- [[remote-file-inclusion]] — the app *executes* a file at a URL you supply → RCE
- [[server-side-request-forgery]] — the server fetches a URL you choose (internal hosts, metadata)
- [[steganography]] — secrets hidden inside carriers (steghide), other alphabets, metadata
- [[log-poisoning]] — inject code into logs → RCE via LFI
- [[ssh-bruteforce]] — hydra dictionary attack on SSH
- [[http-login-bruteforce]] — hydra http-post-form on a web login form
- [[ftp-anonymous-login]] — anonymous FTP file access
- [[sudo-abuse]] — sudo -l + GTFOBins escalation
- [[exim-lpe]] — exim `${run{}}` expansion via sudo
- [[python-library-hijacking]] — shadow Python imports via writable path
- [[suid-enumeration]] — setuid binary hunting
- [[vsftpd-backdoor]] — CVE-2011-2523 trigger
- [[sql-injection]] — auth bypass + CMS SQLi
- [[server-side-template-injection]] — Jinja2 SSTI → RCE
- [[command-injection]] — shell metacharacter injection → RCE
- [[waf-bypass]] — defeat exact-string blacklists via quote/backslash splitting
- [[arithmetic-injection]] — bash `-eq` arithmetic eval → command substitution
- [[shellshock]] — CVE-2014-6271 env-var function definition → RCE
- [[xss-and-cookie-theft]] — stored XSS → session theft
- [[web-cache-deception]] — cache poisoning for sensitive pages
- [[cron-job-abuse]] — writable cron scripts
- [[ci-cd-pipeline-abuse]] — root CI runner / writable builds_dir
- [[group-ownership-enumeration]] — find group-writable files (find -group)
- [[linux-capabilities]] — getcap + cap_setuid abuse
- [[writable-etc-passwd]] — password-less root entry
- [[writable-motd]] — `/etc/update-motd.d/*` runs as root on every SSH login
- [[reverse-shells]] — bash/Node reverse shells
- [[web-shell-upload]] — write a shell to the webroot → RCE
- [[node-inspector-rce]] — RCE via Node.js Inspector (CDP, port 9229)
- [[smb-enumeration]] — enum4linux user/share discovery
- [[mysql-enumeration]] — MySQL/MariaDB enumeration (SHOW/DESCRIBE/SELECT)
- [[ssh-key-cracking]] — john on SSH key passphrases
- [[zip-cracking]] — zip2john + john on encrypted ZIPs
- [[hash-cracking]] — raw hash → plaintext (john/hashcat + online lookup)
- [[source-code-disclosure]] — comments, backups, configs, metadata
- [[pcap-analysis]] — reconstruct an attack from a capture (tshark filters, follow streams)
- [[wordpress-enumeration]] — WP user/plugin enum + wp-login brute-force + theme-editor RCE
- [[hardcoded-credentials]] — hardcoded/reused credentials, shell history & aliases
- [[session-and-cookie-abuse]] — stolen/forged session tokens
- [[broken-access-control]] — client-side role/authorization tampering → privilege escalation; IDOR object-ID sweeps
- [[acrostic-decoding]] — first letters of headings spell a hidden password
- [[prototype-pollution]] — React2Shell: RSC Flight deserialization → Function() RCE
- [[prompt-injection]] — AI/chatbot instruction override → data leak
- [[pivoting]] — multi-hop lateral movement via dual-homed hosts
- [[port-forwarding]] — SSH `-L`/`-R`/`-D` + Metasploit `portfwd` + chisel tunneling
- [[su-brute-force]] — brute-force a local user's password via `su` (Linux-Su-Force.sh)
- [[metasploit-pivoting]] — Metasploit `route`/`autoroute` + `portfwd` multi-hop routing
- [[virtual-hosting]] — vhost discovery behind a default page
- [[path-hijacking]] — hijack a relative command via `PATH` (SUID/sudo/cron)
- [[restricted-shell-escape]] — break out of `rbash` (python3 `pty.spawn` + PATH rebuild)
- [[encoded-credentials]] — base64/encoded secrets in source and files → decode → replay
- [[jenkins-script-console-rce]] — Groovy RCE via Jenkins admin Script Console (feature, not CVE)

## Tools

- [[nmap]] — scanner
- [[arp-scan]] — layer-2 host discovery (same-subnet ARP sweep)
- [[curl]] — HTTP client
- [[gobuster]] — directory brute-forcer
- [[dirb]] — directory brute-forcer
- [[ffuf]] — parameter/path fuzzer
- [[hydra]] — login brute-forcer
- [[john-the-ripper]] — hash/key cracker
- [[burp-suite]] — intercepting proxy
- [[tshark]] — CLI packet capture analyzer (pcap triage)
- [[metasploit]] — exploitation framework
- [[searchsploit]] — Exploit-DB search
- [[enum4linux]] — SMB enumerator
- [[nxc]] — NetExec: SMB user enum + login spray (successor to CrackMapExec)
- [[netcat]] — reverse-shell listener / network utility
- [[telnet]] — TCP client / manual banner grab
- [[mysql]] — MySQL/MariaDB client
- [[sqlmap]] — automated SQL injection detection & extraction
- [[wpscan]] — WordPress scanner + login brute-forcer
- [[gtfobins]] — sudo/SUID payload reference
- [[chisel]] — TCP/UDP tunnel over HTTP (pivoting without SSH)
- [[socat]] — bidirectional TCP relay (listener/`reverse-shell` chains through hops)
- [[proxychains]] — route arbitrary tools through a SOCKS proxy
- [[steghide]] — extract/embed data hidden in JPEG/BMP/WAV carriers
- [[stegseek]] — brute-force a steghide passphrase from a wordlist
- [[ssh]] — remote login + port forwarding (`-L`/`-R`/`-D`)
- [[ping]] — ICMP reachability + TTL/OS hint
- [[smbmap]] — SMB share enum (null vs authenticated permission delta)
- [[smbclient]] — interactive SMB client (get/put, FTP-style)
- [[ftp]] — interactive FTP client (banner + anonymous login)
- [[wget]] — non-interactive file download (staging tools onto a target)
- [[getcap]] — filesystem capability sweep (`getcap -r /`)
- [[whatweb]] — one-shot web fingerprinting
- [[strings]] — printable-run extractor for binaries, pcaps, and compiled bytecode

## CVEs

- [[cve-2011-2523]] — vsftpd 2.3.4 backdoor
- [[cve-2014-6271]] — Shellshock (bash env-var function RCE)
- [[cve-2019-9053]] — CMS Made Simple SQLi
- [[cve-2018-16763]] — Fuel CMS RCE
- [[cve-2021-47980]] — Fuel CMS SQLi
- [[cve-2025-55182]] — React2Shell: RSC Flight deserialization RCE
- [[cve-2024-23897]] — Jenkins CLI arbitrary file read (args4j `@file` expansion)

## Learning

- [[roadmap]] — eJPTv2 learning path + checklist
