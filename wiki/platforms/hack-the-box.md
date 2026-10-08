---
type: platform
difficulties: [easy]
related: ["[[dockerlabs]]", "[[tryhackme]]"]
---

# Hack The Box

Commercial lab platform with released retired machines — dense, well-scenario'd boxes mixing web, network, and privilege escalation.

## Completed boxes

### easy

- [[cap]] — IDOR → pcap credential leak → FTP/SSH → python `cap_setuid`
- [[nexus]] — vhost split → git-history DB password → Krayin CVE upload → on-disk `.env` password → git tree `..` traversal to root
