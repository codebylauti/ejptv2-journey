---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: [CVE-2011-2523]
tools: [nmap, gobuster, netcat]
techniques: [vsftpd-backdoor, directory-fuzzing]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: ["[[first-hacking]]"]
---

# Tproot

**Writeup:** [raw writeup](../../writeups/dockerlabs/super-easy/tproot.md)

Second box exercising the [[vsftpd-backdoor|vsftpd 2.3.4 backdoor]] ([[cve-2011-2523]]).

## Path

1. **Recon** — `nmap` shows `21/tcp ftp vsftpd 2.3.4` and `80/tcp http` (Apache default page).
2. **Web enum** — [[gobuster]] finds nothing useful; the FTP banner is the real lead.
3. **Exploit** — trigger the backdoor (`USER username:)`), then `nc 172.17.0.2 6200` → root shell.

## Steps to reproduce

1. Connect to the FTP service.
2. Enter a username followed by `:)`.
3. Enter any password.
4. The backdoor opens a root shell on port 6200.

## Takeaways

- Same CVE as [[first-hacking]]; reinforces that a version banner is often enough to choose the exploit.
- Don't over-focus on the web app when an obvious service-level vuln is present.
