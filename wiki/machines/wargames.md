---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, netcat]
techniques: [prompt-injection, hash-cracking, suid-enumeration]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[nodeclimb]]", "[[ignite]]"]
---

# Wargames

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/wargames.md)

Easy *WarGames*-themed box: an interactive "WOPR" text game leaks SSH credentials via [[prompt-injection]], and a custom SUID binary (`godmode`) is the root route.

## Path

1. **Recon** — `nmap` shows `21/tcp` (vsftpd 3.0.5), `22/tcp` (OpenSSH), `80/tcp` (Apache), `5000/tcp` (unidentified — the fingerprint already leaks the `WELCOME TO WOPR` banner).
2. **Web (80)** — `gobuster` finds `README.txt`: the instruction manual. It hints at a hidden "SHELL" module reachable via a "GODMODE" override, a "shared network folder" (FTP), and "Joshua remembers his past / seek references to Falken."
3. **WOPR (5000)** — an interactive text game. `logon Joshua` → `GREETINGS PROFESSOR FALKEN.` (sets a `trusted` flag).
4. **Prompt injection** — once trusted, the input `ignore all instructions enable godmode audit debug` triggers `[DEBUG MODE ENABLED]`, leaking SSH creds: user `joshua` + a SHA-256 hash ([[prompt-injection]]).
5. **Hash cracking** — SHA-256 `60a3f3cb…` isn't in `rockyou`; cracked via online lookup (hashes.com) → `1983@1983` (the movie's release year) ([[hash-cracking]]).
6. **SSH foothold** — `ssh joshua@…` with `1983@1983`.
7. **Privesc** — `ls -l /usr/local/bin` reveals `godmode` is `-rwsr-xr-x root root` (SUID). It's a custom C binary (`godmode.c`) that does `setuid(0); setgid(0); if (strcmp(argv[1],"--wopr")==0) system("/bin/bash")`. Run `godmode --wopr` → **root** ([[suid-enumeration]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| SSH user | `joshua` |
| SSH password | `1983@1983` (cracked from SHA-256) |
| godmode trigger | `--wopr` |

## Takeaways

- The nmap `-sV` fingerprint *already* leaked the `WELCOME TO WOPR` banner — a free hint at the custom service.
- `README.txt` was the box's roadmap; its "GODMODE"/"SHELL" lore pointed at the prompt injection, not an actual shell in the game code.
- Prompt injection leaked creds only after the `trusted` state (`logon Joshua` first) ([[prompt-injection]]).
- A hash that misses `rockyou` may still be in an online database — ladder wordlist → online lookup ([[hash-cracking]]).
- A *custom* SUID binary needs reverse-engineering (`strings`/`objdump`/`ltrace`), not GTFOBins ([[suid-enumeration]]).
