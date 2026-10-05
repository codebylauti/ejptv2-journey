---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, hydra]
techniques: [information-gathering, directory-fuzzing, source-code-disclosure, ssh-bruteforce, acrostic-decoding, hardcoded-credentials]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[balufood]]", "[[hedgehog]]"]
---

# Winfake

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/winfake.md)

Easy box built around a **misleading identity**: an Ubuntu box that drops you into a Windows `PowerShell` prompt, with the SSH user leaked from a CSS property and the root password hidden in an acrostic.

## Path

1. **Recon** — `ping -c 2` shows `ttl=64` (Linux). `nmap -p- -sS -sV -sC` finds `22/tcp` (OpenSSH 9.6p1 Ubuntu) and `80/tcp` (Apache 2.4.58, "TechWorld Noticias").
2. **Web enum** — [[gobuster]] returns only `index.html` + 403 noise (dead end). Reading the source instead reveals a weird CSS property `top: pipe;` → the SSH **username** `pipe`, and `<article hidden="acrostico inicial">` → a hint for later ([[source-code-disclosure]]).
3. **SSH brute-force** — `hydra -l pipe -P rockyou.txt ssh://172.17.0.2` → password `kisses` ([[ssh-bruteforce]]).
4. **Foothold** — `ssh pipe@…` lands in `PS C:\Users\pipe>` — a **fake Windows shell** (the box name). It's really Ubuntu 24.04. Read `user.txt`.
5. **Privesc (acrostic)** — the earlier `acrostico inicial` hint means "read the first letter of each title". Extract the first letter of every `<h2>` → `HWINSERVERROOTFAKENEWS` → **`WinServerRootFakeNews`** ([[acrostic-decoding]]).
6. **Root** — `su root` with that password ([[hardcoded-credentials]] weak root password). Read `root.txt`.

## Credentials / secrets

| Item | Value |
|------|-------|
| pipe (SSH) | `kisses` |
| root | `WinServerRootFakeNews` |

## Takeaways

- **Don't trust a single identity signal.** `ttl=64` already said Linux; the PowerShell banner was a red herring ([[information-gathering]]).
- When [[directory-fuzzing]] comes up empty, **read the HTML source** — the `pipe` username was a CSS property, not a comment ([[source-code-disclosure]]).
- The acrostic (first letters of headings spelling a password) is a common CTF "hidden message" trope ([[acrostic-decoding]]).
