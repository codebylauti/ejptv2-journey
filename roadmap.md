# Roadmap

eJPTv2 learning path. Track your progress here — update checkboxes as you complete machines.

## Current state

See [[overview]] for the detailed snapshot. Bottom line: **49 boxes done** across three platforms ([[dockerlabs]], [[tryhackme]], [[hack-the-box]]), solid fundamentals in enumeration, brute-force, and privilege escalation; pivoting now covered three times ([[littlepivoting]] ×2, [[dark]]), SQLi/SUID/vhost depth growing, WAF blacklist bypass now documented ([[waf-bypass]]), IDOR actually documented on [[broken-access-control]] (via [[cap]]), pcap traffic analysis now a documented technique ([[pcap-analysis]], via [[analyst]]), SMB workflow hardened three times by real incidents ([[smb-enumeration]] via [[domain]], [[chmod-4755]], and [[dance-samba]]), SSRF got its first sighting ([[server-side-request-forgery]], via [[dark]]) and RFI its own ([[remote-file-inclusion]], via [[rutas]]), **upload-filter fuzzing** documented with a rejection-size baseline ([[web-shell-upload]], via [[file]]), **encoded-credential decoding** its own technique ([[encoded-credentials]], via [[extraviado]] — extended to ASCII85 by [[jenkhack]]), **Jenkins Script Console RCE** now documented ([[jenkins-script-console-rce]], via [[jenkhack]]) with its pre-auth cousin **CVE-2024-23897 file read** exploited ([[cve-2024-23897]], via [[secretjenkins]]), still light on Active Directory and deep web pentesting.

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
- [x] [[flynn]] — default SSH creds → sudo `env`
- [x] [[analyst]] — pcap triage → captured SSH creds → sudo ALL
- [x] [[file]] — anon FTP hash → upload extension fuzz (`.phar`) → reverse shell → su spray → steghide → 3-hop sudo chain
- [x] [[extraviado]] — base64 default-page creds → SSH → `find` password files → riddle root
- [x] [[dockerlabs-box]] — upload refusal fuzz (`.phar`) → reverse shell → sudo `grep` file read → root
- [x] [[jenkhack]] — hidden-span creds → Jenkins script console → ASCII85 → sudo wrapper overwrite
- [x] [[library]] — default-page camouflage → inverted SSH brute → sudo python library hijack
- [x] [[secretjenkins]] — Jenkins 2.441 file-read CVE (CVE-2024-23897) → user enum → SSH brute → chained sudo
- [x] [[amor]] — news-feed usernames → SSH brute → steghide + base64 → sudo ruby

### DockerLabs — intermediate

- [x] [[adopting]] — cache deception → writable /etc/passwd
- [x] [[pipepwned]] — SSTI → `.env` creds → root gitlab-runner abuse
- [x] [[trailpack]] — MFA brute-force → cookie role tampering → command injection → SUID env
- [x] [[bruteshock]] — Shellshock → 5-hop sudo chain (arithmetic injection → exim → dos2unix)
- [x] [[littlepivoting]] — 3-host pivoting chain (LFI → SSH brute-force → su → sudo ×3 → Metasploit routing), re-run manual (chisel/socat/proxychains)
- [x] [[domain]] — SMB enum → nxc spray → writable share → SUID nano (reclassified from easy)
- [x] [[chmod-4755]] — SMB hints → rbash escape → SUID curl overwrites /etc/passwd
- [x] [[dance-samba]] — FTP note hint → SMB spray → writable home share → SSH key → sudo `file` leak
- [x] [[dark]] — SSRF/LFI on one `url` param → SSH brute-force → Metasploit pivot → `cmd` RCE → SUID curl
- [x] [[rutas]] — anon FTP → zip crack → steghide → Basic-auth vhost → param fuzz → RFI → PATH hijack → writable MOTD

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

**Covered:** [[information-gathering]], [[directory-fuzzing]], [[parameter-fuzzing]], [[smb-enumeration]], [[mysql-enumeration]], [[source-code-disclosure]], [[pcap-analysis]], [[acrostic-decoding]], [[ftp-anonymous-login]], [[hardcoded-credentials]], [[steganography]], [[encoded-credentials]], [[virtual-hosting]], [[wordpress-enumeration]].

**Gaps & next steps**
- [ ] Practice full enumeration toolchain: `nmap` script engine, `nikto`, `dirb`, SNMP/WinRM enumeration.
- [ ] Web + OSINT: `whatweb` (first use on [[cap]]), `wpscan`, DNS enumeration.
- [ ] Do more DockerLabs **easy** boxes to build enumeration fluency.

### 2. Host & Network Auditing (`ejpt:auditing`)

**Covered:** [[smb-enumeration]] (null-session users, share perms, login spray — standalone Samba only, no AD/DC).

**Gaps & next steps**
- [ ] Study auditing fundamentals: `netstat`, `tcpdump`, `wireshark`, `nmap` NSE. (Partial: CLI capture analysis now covered via [[tshark]]/[[pcap-analysis]] on [[analyst]] — still no live sniffing with `tcpdump` or the Wireshark GUI.)
- [ ] Practice Linux/Windows service and network auditing labs.

### 3. Host & Network Penetration Testing (`ejpt:host-net-pentest`)

**Covered:** [[ssh-bruteforce]], [[sudo-abuse]], [[arithmetic-injection]], [[exim-lpe]], [[suid-enumeration]], [[cron-job-abuse]], [[linux-capabilities]], [[writable-etc-passwd]], [[writable-motd]], [[reverse-shells]], [[restricted-shell-escape]], [[node-inspector-rce]], [[jenkins-script-console-rce]], [[vsftpd-backdoor]], [[ssh-key-cracking]], [[zip-cracking]], [[hash-cracking]], [[hardcoded-credentials]], [[group-ownership-enumeration]], [[python-library-hijacking]], [[ftp-anonymous-login]], [[ci-cd-pipeline-abuse]], [[pivoting]], [[port-forwarding]], [[metasploit-pivoting]], [[su-brute-force]], [[path-hijacking]], [[smb-enumeration]], [[steganography]], [[pcap-analysis]], [[log-poisoning]], [[shellshock]], [[command-injection]], [[encoded-credentials]].

**Gaps & next steps**
- [ ] **Metasploit** — depth growing: [[littlepivoting]] exercised `route`/`portfwd`/`shell_to_meterpreter` ([[metasploit-pivoting]]). Still do THM "Metasploit" module.
- [ ] **Password cracking** — raw-hash cracking covered via [[hash-cracking]] ([[wargames]], [[madeyes-castle]] with `--rules=best64`); `NTLM`/`/etc/shadow` OS hashes still untried.
- [ ] **Pivoting & lateral movement** — Metasploit routing covered twice ([[littlepivoting]], [[dark]]: `ping_sweep` → `portscan/tcp` → `portfwd`), and the manual re-run now exercises [[chisel]] + [[proxychains]] + [[socat]] end-to-end ([[pivoting]], [[port-forwarding]]). **Next: SSH tunneling** (`-D`/`-L`/`-R` — documented, not yet exercised on a box).
- [ ] **Active Directory** — SMB relays, Kerberoasting, LLMNR poisoning.
- [ ] Complete more DockerLabs **intermediate/hard** boxes.

### 4. Web Application Penetration Testing (`ejpt:web-pentest`)

**Covered:** [[sql-injection]], [[xss-and-cookie-theft]], [[web-cache-deception]], [[session-and-cookie-abuse]], [[broken-access-control]], [[local-file-inclusion]], [[remote-file-inclusion]], [[server-side-request-forgery]], [[log-poisoning]], [[parameter-fuzzing]], [[value-brute-force]], [[mfa-bruteforce]], [[directory-fuzzing]], [[source-code-disclosure]], [[acrostic-decoding]], [[prototype-pollution]], [[prompt-injection]], [[wordpress-enumeration]], [[web-shell-upload]], [[server-side-template-injection]], [[command-injection]], [[shellshock]], [[http-login-bruteforce]], [[virtual-hosting]], [[encoded-credentials]], [[waf-bypass]], [[jenkins-script-console-rce]].

**Gaps & next steps**
- [ ] **LFI/RFI** — RFI now covered via [[rutas]] ([[remote-file-inclusion]]); LFI basics solid ([[local-file-inclusion]]). **Remaining:** `/proc`-based tricks and LFI → RCE pairing beyond [[log-poisoning]]. SSTI covered via [[server-side-template-injection]]; command injection via [[command-injection]].
- [ ] **SSRF** — first sighting on [[dark]] (`process.php` `url=` fetched the internal `20.20.20.3` page and echoed it back), but only the "fetch an internal URL and reflect it" shape: still no `127.0.0.1`/service-on-localhost target, no cloud metadata (`169.254.169.254`), no protocol smuggling. **CSRF** — not yet seen. (IDOR/broken access control now covered via [[broken-access-control]].)
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
