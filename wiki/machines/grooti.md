---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, mysql, hydra, netcat]
techniques: [directory-fuzzing, source-code-disclosure, hardcoded-credentials, mysql-enumeration, value-brute-force, ssh-bruteforce, cron-job-abuse, reverse-shells]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[balulero]]", "[[nodeclimb]]"]
---

# Grooti

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/grooti.md)

Easy box chaining a MySQL route-leak → a numeric brute-force that returns a password ZIP → SSH brute-force → a writable root cron script.

## Path

1. **Recon** — `nmap -p- -sS -sV -sC` shows `22/tcp` (OpenSSH 9.6p1), `80/tcp` (Apache 2.4.58, "Grooti's Web"), and `3306/tcp` (MySQL 8.0.42).
2. **Web enum** — [[gobuster]] finds `secret/`, `imagenes/`, and `archives/`. `/secret/instrucciones.txt` hints the escalation path (`rocket` → `groot` → `naia`) and leaks `mysql -u rocket -p …`; `/imagenes/README.txt` leaks the password `password1` ([[source-code-disclosure]]).
3. **MySQL enum** — `mysql -u rocket -p` (`password1`) → database `files_secret`, table `rutas` maps a hidden route: `secret` → `/unprivate/secret` ([[mysql-enumeration]]).
4. **Value brute-force** — `/unprivate/secret/generate.php` echoes back whatever `content` you send, except for `number=16`, which returns a password-protected ZIP. Unzip with the *reused* `password1` → `password16.txt` (a 34-entry wordlist) ([[value-brute-force]], [[hardcoded-credentials]]).
5. **SSH brute-force** — `hydra -l grooti -P password16.txt ssh://172.17.0.2` → `YoSoYgRoOt` ([[ssh-bruteforce]]).
6. **Privesc** — `crontab -l` shows `* * * * * /opt/cleanup.sh`, which runs `bash /tmp/malicious.sh` — writable by `grooti`. Overwrite it with a [[reverse-shells|reverse shell]] → **root** ([[cron-job-abuse]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| rocket (MySQL) | `password1` |
| password16.zip | `password1` (reused) |
| grooti (SSH) | `YoSoYgRoOt` |

## Takeaways

- `password1` unlocked **both** MySQL and the ZIP — textbook credential reuse ([[hardcoded-credentials]]).
- A DB can map friendly names to filesystem paths — `rutas` leaked the hidden `/unprivate/secret` ([[mysql-enumeration]]).
- Watching `Content-Length` while brute-forcing a numeric param spots the one "odd" response ([[value-brute-force]]).
- A writable `/tmp/malicious.sh` invoked by root cron is instant root ([[cron-job-abuse]]).
