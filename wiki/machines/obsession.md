---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, hydra]
techniques: [ftp-anonymous-login, directory-fuzzing, ssh-bruteforce, sudo-abuse, source-code-disclosure]
tags: [ejpt:assessment, ejpt:host-net-pentest, ejpt:web-pentest]
related: ["[[vacaciones]]", "[[hedgehog]]"]
---

# Obsession

**Writeup:** [raw writeup](../../writeups/dockerlabs/super-easy/obsession.md)

Chains anonymous FTP, web source hints, SSH brute-force, and a [[sudo-abuse|sudo vim]] escalation.

## Path

1. **Recon** — `nmap` shows `21/tcp ftp`, `22/tcp ssh`, `80/tcp http`.
2. **Web enum** — [[gobuster]] finds `backup/` and `important/`. An HTML comment reveals all services share one username; `backup.txt` leaks it (`russoski`).
3. **FTP enum** — [[ftp-anonymous-login|anonymous login]] yields two text files with hints (including a mention of the eJPTv2 voucher).
4. **Brute force** — `hydra -l russoski -P rockyou.txt` → password `iloveme`.
5. **Escalation** — `sudo -l` shows `(root) NOPASSWD: /usr/bin/vim`; `sudo vim -c ':!/bin/sh' /dev/null` → root.

## Credentials

| User | Password |
|------|----------|
| russoski | `iloveme` |

## Takeaways

- Anonymous FTP is a common goldmine for usernames and hints ([[ftp-anonymous-login]]).
- HTML comments and `backup.txt` are textbook [[source-code-disclosure]] vectors.
