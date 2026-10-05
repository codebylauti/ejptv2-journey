---
type: technique
tags: [ejpt:host-net-pentest, ejpt:assessment]
tools: [tshark]
cves: []
related: ["[[source-code-disclosure]]", "[[pcap-analysis]]"]
---

# Hardcoded Credentials

Finding credentials that were left hardcoded or reused across accounts — in source, config files, shell history, and shell aliases.

## Vectors

- **Shell history** — `.bash_history` reveals prior commands (`nano ~/.bashrc`, `su root`) ([[balufood]]).
- **Shell config & aliases** — `.bashrc`/`.bash_profile` aliases or exports that embed a password (`alias ser-root='echo chocolate2 | su - root'`) ([[balufood]]).
- **Reused secrets** — a web app `secret_key` doubling as an OS user's password ([[balufood]]); a single `password1` reused across MySQL and a downloaded ZIP ([[grooti]]).
- **Hardcoded app creds** — `admin`/`admin` in `app.py` ([[balufood]]).
- **Weak/derived root password** — `su root` succeeds with a guessable password derived from a clue (`WinServerRootFakeNews` from an [[acrostic-decoding|acrostic]]) ([[winfake]]).
- **Source-embedded credentials** — a PHP `$database` array hardcoded with IDs, one commented `// ID vulnerable`, that a `panel.php?id=` lookup turns into working SSH creds ([[duque]]); plaintext creds dumped from a DB (`register.users`) that don't escalate ([[duque]]).
- **DB config credentials** — `config.php` holding MySQL `root`/`paso` ([[injection]]).
- **CI trace / env-file leak** — a debug `env` dump in a pipeline trace leaks `CI_RUNNER_TOKEN=glrt-…`, and a runner `environment_file` (`/opt/ci/.env`) leaks an SSH password for `devops` ([[pipepwned]]).
- **In-memory user table** — `main.py` holds a `USERS` dict with plaintext passwords written beside `hash_pw(...)` calls ([[trailpack]]).
- **Backup files leaking password hashes** — `/var/backups/darksblack/.darksblack.txt` holds a `/etc/shadow`-format yescrypt hash, cracked to a password ([[bruteshock]]).
- **Service banner / MOTD leak** — connecting to SSH with *any* username prints a pre-auth maintenance banner containing a working user/password pair ([[acme]]). Telnet/FTP banners are the same class of target — always open a connection and read the full banner before brute-forcing.
- **Banner *identity* hints** — a pre-auth banner signed by a name (`by fuckit`) leaks a **username** even when it holds no password. Banner text is a hint source for *accounts* too: feed it straight into the next login spray ([[chmod-4755]], cf. [[acme]]).
- **Password file left on disk** — a dedicated wordlist of 20 candidate passwords (`/opt/.vault_pass.txt`) ready to feed `hydra -P`. Found wordlists beat rockyou: the box curated them for you ([[internal]]).
- **Default / weak service credentials** — the username doubling as the password (`flynn:flynn`), no brute-force required. Try the box name, the username, and trivial variants **before** reaching for rockyou ([[flynn]]).
- **Cleartext protocol capture (pcap)** — a downloadable network capture containing FTP/HTTP-auth traffic in plain text: `strings <pcap> | grep -E 'USER|PASS'` → `USER nathan` / `PASS Buck3tH4TF0RM3!`. Credentials also hide in *operational messages* inside the capture — a password-reset line leaked `pinguinito:Tr0pic4l-Pingu_99!` ([[analyst]], see [[pcap-analysis]]). Any file the app lets you download may be someone's session ([[cap]]).
- **Narrative hint files** — a loose note written as gossip (*"Macarena, she's obsessed with donald"*) is `macarena:donald` in prose: the subject is the username, the fixation is the password. Anything a box bothers to drop in an anonymous FTP root or a share is there for you to read ([[dance-samba]], cf. [[chmod-4755]]'s "read better").
- **Credential files in odd paths** — dot-directories hide them (`~/.-/.miscredenciales`), and the file tells you what it's *for* ("Usa mis pass para escalar"). The password may not even be Latin script: this one was Braille → [[steganography]]. A second file next door (`/home/maria/.mipass` written as `maria:asientiendesmejor`) is a credential pair handed over in `user:pass` form ([[rutas]]).
- **Steganographic credential** — a password that arrives from *inside* an image rather than from text: `steghide` → `passwd.zip` → `hackeada:denuevo`, then replayed as an `Authorization: Basic` header. Whatever you pull out of a carrier is a credential until proven otherwise ([[rutas]], [[steganography]]).

## Commands

```sh
cat ~/.bash_history
cat ~/.bashrc
grep -RniE 'pass(word)?|secret|token|key|pwd' /home /opt /var/www 2>/dev/null
```

## Seen in

[[balufood]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[pipepwned]], [[trailpack]], [[bruteshock]], [[acme]], [[internal]], [[cap]], [[flynn]], [[analyst]], [[chmod-4755]], [[dance-samba]], [[rutas]]
