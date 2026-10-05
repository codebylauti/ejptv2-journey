---
type: technique
tags: [ejpt:assessment]
tools: [nmap]
cves: []
related: ["[[directory-fuzzing]]"]
---

# Information Gathering

The first phase of any engagement: confirm reachability and discover open ports/services.

## Workflow

1. **ICMP** — [[ping]] `-c 2 <target>` confirms the host is up and shows TTL (a hint at the OS: ~64 Linux, ~128 Windows).
2. **Port scan** — `nmap -sV -sC -p-` (or `-sS` for SYN scan) enumerates ports, service versions, and runs default scripts.
3. **Fingerprint** — [[whatweb]] `http://TARGET` one-shots the web stack (framework, JS libs, server header, title) so you know what you're facing before fuzzing.
4. **Analyze** — service/version banners (e.g. `vsftpd 2.3.4`) frequently map straight to a known CVE.

## Host & network discovery (multi-host / pivoting)

On a lab with several subnets, map the topology before scanning blindly:

- `ip a` / `hostname -I` — your own interfaces and IPs (find the subnet you're on).
- `ip route` — which networks you can reach (and the gateway).
- `nmap -sn <net>` — ping sweep to find live hosts on that subnet.
- [[arp-scan]] `--localnet` — layer-2 sweep of the *directly connected* subnet (shows MACs; no route needed).

Or, from a shell, the classic one-liner: `for i in $(seq 254); do ping -c1 -W1 <net>.$i & done | grep from`.

This is the seed of [[pivoting]]: know your subnet, scan it, compromise a host, then read *its* interfaces for the next subnet.

## Correlate, don't trust one signal

- Banners and shells can lie: [[winfake]] drops you into a `PS C:\Users\pipe>` PowerShell prompt on what is actually Ubuntu — the `ttl=64` was the honest tell. Cross-check TTL, service banners, and the post-login shell.
- HTTP status lines are recon too: a **303 `See Other`** pointing at a hostname (`curl -s http://IP/`) hands you the real vhost name ([[virtual-hosting]], [[internal]]).

## Seen in

- Every box in this vault starts with this phase (e.g. [[breakmyssh]], [[ignite]]).
