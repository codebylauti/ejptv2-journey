---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, hydra]
techniques: [directory-fuzzing, ssh-bruteforce, sudo-abuse, source-code-disclosure]
tags: [ejpt:assessment, ejpt:host-net-pentest, ejpt:web-pentest]
related: [[vacaciones]], [[hedgehog]]
---

# Borazuwara CTF

**Writeup:** [raw writeup](../../writeups/dockerlabs/super-easy/borazuwara-ctf.md)

Web box where the SSH username is hidden in an image file.

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` and `80/tcp http`.
2. **Web enum** — `index.html` only renders `imagen.jpeg`; download it with `wget` and extract the username (`borazuwarah`) from the image's source/metadata.
3. **Brute force** — `hydra -l borazuwarah -P rockyou.txt` → `123456`.
4. **Escalation** — the user is in the `sudo` group; `sudo -l` shows `(ALL : ALL) ALL` and `NOPASSWD: /bin/bash` → `sudo su` → root.

## Credentials

| User | Password |
|------|----------|
| borazuwarah | `123456` |

## Takeaways

- Always inspect files served by the web app — images can hide usernames in their source or metadata ([[source-code-disclosure]]).
- Group membership matters: `id` reveals `sudo`, which trivially enables [[sudo-abuse]].
