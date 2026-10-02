# Roadmap

eJPTv2 learning path. Track your progress here — update checkboxes as you complete machines.

## Current state

See [[overview]] for the detailed snapshot. Bottom line: **35 boxes done** across three platforms ([[dockerlabs]], [[tryhackme]], [[hack-the-box]]), solid fundamentals in enumeration, brute-force, and privilege escalation; pivoting now covered ([[littlepivoting]]), SQLi/SUID/vhost depth growing, WAF blacklist bypass now documented ([[waf-bypass]]), IDOR actually documented on [[broken-access-control]] (via [[cap]]), still light on Active Directory and deep web pentesting.

---

## Completed boxes (checklist)

### DockerLabs — super-easy

- [x] [[breakmyssh]] — SSH brute-force
- [x] [[first-hacking]] — vsftpd backdoor (CVE-2011-2523)
- [x] [[hedgehog]] — source leak → brute-force → chained sudo
- [x] [[trust]] — fuzzing → brute-force → sudo vim
- [x] [[tproot]] — vsftpd backdoor
- [x] [[obsession]] — anonymous FTP → sudo vim
- [x] [[vacaciones]] — comment usernames → sudo ruby
- [x] [[borazuwara]] — image metadata → sudo group
- [x] [[acme]] — SSH banner creds → SUID bash

### DockerLabs — easy

- [x] [[los-3-hackers]] — SQLi → session → cron → capabilities
- [x] [[hannah-coffee]] — LFI + log poisoning → debugfs → capabilities
- [x] [[balufood]] — leaked creds → secret_key reuse → .bashrc alias
- [x] [[balulero]] — .env leak → sudo php → group-owned script
- [x] [[nodeclimb]] — anon FTP → zip crack → sudo node
- [x] [[psycho]] — LFI → SSH key → chained sudo
- [x] [[autoescuela]] — Node.js Inspector RCE → React2Shell (CVE-2025-55182)
- [x] [[wargames]] — prompt injection → hash crack → SUID binary
- [x] [[grooti]] — MySQL leak → value brute-force → SSH brute-force → cron
- [x] [[winfake]] — CSS username leak → SSH brute-force → acrostic root password
- [x] [[duque]] — SQLi bypass → sqlmap file-read → SSH → env SUID
- [ ] [[injection]] — error-based SQLi → SSH → ⚠️ incomplete (privesc pending)
- [x] [[walkingcms]] — WordPress → wpscan brute-force → theme-editor shell → env SUID
- [x] [[anonymous-pingu]] — anon FTP upload → PHP shell → chained sudo (man → nmap → chown)
- [x] [[internal]] — 303 vhost leak → WAF blacklist bypass → reverse shell → leaked wordlist → vaultctl

### DockerLabs — intermediate

- [x] [[adopting]] — cache deception → writable /etc/passwd
- [x] [[pipepwned]] — SSTI → `.env` creds → root gitlab-runner abuse
- [x] [[trailpack]] — MFA brute-force → cookie role tampering → command injection → SUID env
- [x] [[bruteshock]] — Shellshock → 5-hop sudo chain (arithmetic injection → exim → dos2unix)
- [x] [[littlepivoting]] — 3-host pivoting chain (LFI → SSH brute-force → su → sudo ×3 → Metasploit routing), re-run manual (chisel/socat/proxychains)

### DockerLabs — hard

- [x] [[baluhome]] — XSS → cookie theft → reverse shell → cron

### TryHackMe

- [x] [[basic-pentesting]] — SMB enum → brute-force → key cracking
- [x] [[simple-ctf]] — CMS SQLi → sudo vim
- [x] [[ignite]] — Fuel CMS SQLi + RCE
- [x] [[guided-pentest]] — UnrealIRCd via Metasploit
- [x] [[madeyes-castle]] — vhost → SQLite UNION SQLi → SHA-512 crack → pico sudo → SUID PATH-hijack

### Hack The Box

- [x] [[cap]] — IDOR → pcap credential leak → FTP/SSH → python `cap_setuid`

---

## eJPTv2 domains — coverage & next steps

### 1. Assessment Methodologies (`ejpt:assessment`)

**Covered:** [[information-gathering]], [[directory-fuzzing]], [[parameter-fuzzing]], [[smb-enumeration]], [[mysql-enumeration]], [[source-code-disclosure]], [[acrostic-decoding]], [[ftp-anonymous-login]], [[hardcoded-credentials]].

**Gaps & next steps**
- [ ] Practice full enumeration toolchain: `nmap` script engine, `nikto`, `dirb`, SNMP/WinRM enumeration.
- [ ] Web + OSINT: `whatweb` (first use on [[cap]]), `wpscan`, DNS enumeration.
- [ ] Do more DockerLabs **easy** boxes to build enumeration fluency.

### 2. Host & Network Auditing (`ejpt:auditing`)

**Covered:** [[smb-enumeration]] (light).

**Gaps & next steps**
- [ ] Study auditing fundamentals: `netstat`, `tcpdump`, `wireshark`, `nmap` NSE.
- [ ] Practice Linux/Windows service and network auditing labs.

### 3. Host & Network Penetration Testing (`ejpt:host-net-pentest`)

**Covered:** [[ssh-bruteforce]], [[sudo-abuse]], [[arithmetic-injection]], [[exim-lpe]], [[suid-enumeration]], [[cron-job-abuse]], [[linux-capabilities]], [[writable-etc-passwd]], [[reverse-shells]], [[node-inspector-rce]], [[vsftpd-backdoor]], [[ssh-key-cracking]], [[zip-cracking]], [[hash-cracking]], [[hardcoded-credentials]], [[group-ownership-enumeration]], [[python-library-hijacking]], [[ftp-anonymous-login]], [[ci-cd-pipeline-abuse]], [[pivoting]], [[port-forwarding]], [[metasploit-pivoting]], [[su-brute-force]], [[path-hijacking]].

**Gaps & next steps**
- [ ] **Metasploit** — depth growing: [[littlepivoting]] exercised `route`/`portfwd`/`shell_to_meterpreter` ([[metasploit-pivoting]]). Still do THM "Metasploit" module.
- [ ] **Password cracking** — raw-hash cracking covered via [[hash-cracking]] ([[wargames]], [[madeyes-castle]] with `--rules=best64`); `NTLM`/`/etc/shadow` OS hashes still untried.
- [ ] **Pivoting & lateral movement** — Metasploit routing covered ([[littlepivoting]]), and the manual re-run now exercises [[chisel]] + [[proxychains]] + [[socat]] end-to-end ([[pivoting]], [[port-forwarding]]). **Next: SSH tunneling** (`-D`/`-L`/`-R` — documented, not yet exercised on a box).
- [ ] **Active Directory** — SMB relays, Kerberoasting, LLMNR poisoning.
- [ ] Complete more DockerLabs **intermediate/hard** boxes.

### 4. Web Application Penetration Testing (`ejpt:web-pentest`)

**Covered:** [[sql-injection]], [[xss-and-cookie-theft]], [[web-cache-deception]], [[session-and-cookie-abuse]], [[broken-access-control]], [[local-file-inclusion]], [[log-poisoning]], [[parameter-fuzzing]], [[value-brute-force]], [[mfa-bruteforce]], [[directory-fuzzing]], [[source-code-disclosure]], [[acrostic-decoding]], [[prototype-pollution]], [[prompt-injection]], [[wordpress-enumeration]], [[web-shell-upload]], [[server-side-template-injection]], [[command-injection]], [[shellshock]], [[http-login-bruteforce]], [[virtual-hosting]].

**Gaps & next steps**
- [ ] **LFI/RFI** beyond the basics ([[local-file-inclusion]] done; extend to RFI and `/proc` tricks). SSTI covered via [[server-side-template-injection]]; command injection covered via [[command-injection]].
- [ ] **SSRF**, **CSRF** — not yet seen. (IDOR/broken access control now covered via [[broken-access-control]].)
- [ ] THM "Web Fundamentals" + "OWASP Top 10" paths.
- [ ] More DockerLabs web-focused boxes.

---

## Suggested next machines

1. **DockerLabs easy/intermediate** — build enumeration + web depth (e.g. boxes involving LFI/command injection).
2. **TryHackMe — Jr Penetration Tester path** — the canonical eJPTv2 prep.
3. **TryHackMe — Metasploit, Wireshark, Burp Suite rooms** — tool depth.
4. **A full eJPT-style engagement** — a multi-host network to practice pivoting end-to-end.

---

## Study flow

1. Pick a machine, add it to the "In progress" list here.
2. After root, ingest its writeup: I'll create the machine page, update techniques/tools/CVEs, and tick it off.
3. Every ~10 boxes, run a **lint** pass to spot gaps and contradictions.
