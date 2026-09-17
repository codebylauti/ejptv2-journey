---
type: technique
tags: [ejpt:assessment]
tools: [nmap]
cves: []
related: [[directory-fuzzing]]
---

# Information Gathering

The first phase of any engagement: confirm reachability and discover open ports/services.

## Workflow

1. **ICMP** — `ping -c 2 <target>` confirms the host is up and shows TTL (a hint at the OS: ~64 Linux, ~128 Windows).
2. **Port scan** — `nmap -sV -sC -p-` (or `-sS` for SYN scan) enumerates ports, service versions, and runs default scripts.
3. **Analyze** — service/version banners (e.g. `vsftpd 2.3.4`) frequently map straight to a known CVE.

## Correlate, don't trust one signal

- Banners and shells can lie: [[winfake]] drops you into a `PS C:\Users\pipe>` PowerShell prompt on what is actually Ubuntu — the `ttl=64` was the honest tell. Cross-check TTL, service banners, and the post-login shell.

## Seen in

- Every box in this vault starts with this phase (e.g. [[breakmyssh]], [[ignite]]).
