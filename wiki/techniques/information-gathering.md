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

## Seen in

- Every box in this vault starts with this phase (e.g. [[breakmyssh]], [[ignite]]).
