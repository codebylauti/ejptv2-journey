---
type: machine
platform: dockerlabs
difficulty: super-easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, hydra]
techniques: [directory-fuzzing, ssh-bruteforce, sudo-abuse, source-code-disclosure]
tags: [ejpt:assessment, ejpt:host-net-pentest, ejpt:web-pentest]
related: [[obsession]], [[hedgehog]]
---

# Vacaciones

Two-user SSH chain with an email-based password handoff and a [[sudo-abuse|sudo ruby]] escalation.

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` and `80/tcp http`.
2. **Web enum** — an HTML comment names two possible users (`juan`, `camilo`).
3. **Brute force** — `hydra -l camilo -P rockyou.txt` → `password1`.
4. **Pivot** — as `camilo`, read `correo.txt`, which hands off `juan`'s password (`2k84dicb`).
5. **Escalation** — as `juan`, `sudo -l` shows `(ALL) NOPASSWD: /usr/bin/ruby`; `sudo ruby -e 'exec "/bin/sh"'` → root.

## Credentials

| User | Password |
|------|----------|
| camilo | `password1` |
| juan | `2k84dicb` |

## Takeaways

- HTML comments are a reliable way to harvest candidate usernames ([[source-code-disclosure]]).
- Passwords often move between users via files/mail — read home directories after each login.
- `sudo` + a scripting language (`ruby`, `python`, `perl`) is a direct [[sudo-abuse]] path to root.
