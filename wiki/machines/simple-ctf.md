---
type: machine
platform: tryhackme
difficulty: easy
ip: 10.67.185.90
cves: [CVE-2019-9053]
tools: [hydra, gobuster]
techniques: [sql-injection, ssh-bruteforce, sudo-abuse, directory-fuzzing, source-code-disclosure]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: [[basic-pentesting]], [[ignite]]
---

# Simple CTF

**Writeup:** [raw writeup](../../writeups/tryhackme/simple-ctf.md)

Web box where a [[sql-injection|CMS Made Simple SQLi]] ([[cve-2019-9053]]) leaks credentials, leading to a [[sudo-abuse|sudo vim]] escalation.

## Path

1. **Recon** — open ports: `21` FTP, `80` HTTP, `2222` SSH.
2. **Web enum** — hidden paths `/simple` (CMS Made Simple) and `/robots.txt`.
3. **Exploit** — [[cve-2019-9053]] extracts the CMS salt, username (`mitch`), and password hash.
4. **Brute force** — crack the password (`secret`) with hydra and SSH in.
5. **Escalation** — `sudo vim` (GTFOBins) → root.

## Credentials

| User | Password |
|------|----------|
| mitch | `secret` |

## Takeaways

- CMS version identification + searchsploit is a fast path to a working exploit ([[sql-injection]]).
- The `sudo vim` escalation recurs (see [[trust]], [[obsession]]).
