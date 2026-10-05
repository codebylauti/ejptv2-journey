---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, dirb, curl]
techniques: [directory-fuzzing, source-code-disclosure, hardcoded-credentials]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[hannah-coffee]]", "[[los-3-hackers]]"]
---

# Balufood

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/balufood.md)

Easy box where the whole chain is **leaked credentials + reuse**: an HTML comment leaks the SSH user, the Flask `secret_key` is reused as another user's password, and a `.bashrc` alias stores the root password.

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` (OpenSSH 9.2p1) and `5000/tcp http` (Werkzeug 2.2.2 / Python 3.11.2, Flask).
2. **Dir fuzzing** — `dirb` finds `/admin` (302), `/console` (400), `/login`, `/logout`. The `400` (not `404`) on `/console` hints the Werkzeug debugger is enabled.
3. **Web auth bypass** — `/login` accepts `admin` / `admin` (hardcoded in `app.py`).
4. **Source disclosure** — the `/admin` HTML contains `<!-- Backup de acceso: sysadmin:backup123 -->` ([[source-code-disclosure]]).
5. **SSH foothold** — `ssh sysadmin@…` with `backup123`.
6. **Read source** — `app.py` is world-readable in the home dir: `app.secret_key = 'cuidaditocuidadin'` and `app.run(…, debug=True)`. `ps aux` shows it running as **root**.
7. **Lateral move** — the `secret_key` value is reused as the `balulero` user's password: `su balulero` → `cuidaditocuidadin` ([[hardcoded-credentials]]).
8. **Privesc** — `balulero`'s `.bash_history` reveals `.bashrc` was edited; `cat .bashrc` shows `alias ser-root='echo chocolate2 | su - root'`, leaking the root password.
9. **Root** — `su - root` with `chocolate2`.

## Credentials / secrets

| Item | Value |
|------|-------|
| web login (`/login`) | `admin` / `admin` |
| sysadmin (SSH) | `backup123` |
| Flask `secret_key` | `cuidaditocuidadin` |
| balulero | `cuidaditocuidadin` |
| root | `chocolate2` |

## Takeaways

- Always read HTML source for comments ([[source-code-disclosure]]).
- Reusing one secret across layers (web `secret_key` → OS password) collapses the whole box.
- `.bash_history` and `.bashrc` aliases are prime post-exploitation recon ([[hardcoded-credentials]]).
- Not required here, but present: `debug=True` + root process + `/console` (400) means a computed **Werkzeug debugger PIN** would also yield root RCE.
