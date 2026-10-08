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
- **Weak/derived root password** — `su root` succeeds with a guessable password derived from a clue (`WinServerRootFakeNews` from an [[acrostic-decoding|acrostic]]) ([[winfake]]); or from a *riddle* whose answer you supply (`osopolar` = the polar bear in the poem) ([[extraviado]]).
- **Encoded password files found by `find`** — names are the signal (`*diego*`, `.*pass.*`), contents are base64: `~/.secreto/passdiego` → `ballenanegra` ([[extraviado]], [[encoded-credentials]]). **Decode before you trust**: `.passroot/.pass` decodes to `acatampocoesta` — *"aca tampoco esta"*, the box joking that it's not there either. A filename promising the secret is not the secret ([[dance-samba]]'s counter-example).
- **Hash file named for its target user** — the same `find / -name *<username>*` sweep, one format over: `/srv/ftp/hash_spencer.txt` holds a raw MD5, and the filename already answers *whose* it is — crack it and go straight to `su spencer` with no guessing about the account ([[pequeñas-mentirosas]], [[hash-cracking]]).
- **Source-embedded credentials** — a PHP `$database` array hardcoded with IDs, one commented `// ID vulnerable`, that a `panel.php?id=` lookup turns into working SSH creds ([[duque]]); plaintext creds dumped from a DB (`register.users`) that don't escalate ([[duque]]).
- **DB config credentials** — `config.php` holding MySQL `root`/`paso` ([[injection]]).
- **Git-history password + live `.env` reuse** — a `DB_PASSWORD` recovered from a repo's **commit history** (the tip commit had it blanked) authenticates to the web app, and a *second* `DB_PASSWORD` read post-exploit from the app's live on-disk `.env` (`/var/www/krayin/.env`, located with `find / -name .env`) becomes the local account's `su`/git password — one application, two credential stores, two footholds. Don't assume a secret found in one store covers only one service ([[nexus]], [[source-code-disclosure]]).
- **CI trace / env-file leak** — a debug `env` dump in a pipeline trace leaks `CI_RUNNER_TOKEN=glrt-…`, and a runner `environment_file` (`/opt/ci/.env`) leaks an SSH password for `devops` ([[pipepwned]]).
- **In-memory user table** — `main.py` holds a `USERS` dict with plaintext passwords written beside `hash_pw(...)` calls ([[trailpack]]).
- **Backup files leaking password hashes** — `/var/backups/darksblack/.darksblack.txt` holds a `/etc/shadow`-format yescrypt hash, cracked to a password ([[bruteshock]]).
- **Service banner / MOTD leak** — connecting to SSH with *any* username prints a pre-auth maintenance banner containing a working user/password pair ([[acme]]). Telnet/FTP banners are the same class of target — always open a connection and read the full banner before brute-forcing.
- **Banner *identity* hints** — a pre-auth banner signed by a name (`by fuckit`) leaks a **username** even when it holds no password. Banner text is a hint source for *accounts* too: feed it straight into the next login spray ([[chmod-4755]], cf. [[acme]]).
- **Password file left on disk** — a dedicated wordlist of 20 candidate passwords (`/opt/.vault_pass.txt`) ready to feed `hydra -P`. Found wordlists beat rockyou: the box curated them for you ([[internal]]).
- **Default / weak service credentials** — the username doubling as the password (`flynn:flynn`), no brute-force required. Try the box name, the username, and trivial variants **before** reaching for rockyou ([[flynn]]).
- **Cleartext protocol capture (pcap)** — a downloadable network capture containing FTP/HTTP-auth traffic in plain text: `strings <pcap> | grep -E 'USER|PASS'` → `USER nathan` / `PASS Buck3tH4TF0RM3!`. Credentials also hide in *operational messages* inside the capture — a password-reset line leaked `pinguinito:Tr0pic4l-Pingu_99!` ([[analyst]], see [[pcap-analysis]]). Any file the app lets you download may be someone's session ([[cap]]).
- **Credential pair planted in HTML** — `user` and `pass` sitting in two `class="hidden"` spans on the page, ready to replay against a *service on another port* (the pair's words tell you which: `jenkins-admin` → Jenkins on 8080). No brute-force, no file access — just the source ([[jenkhack]], [[source-code-disclosure]]).
- **Narrative hint files** — a loose note written as gossip (*"Macarena, she's obsessed with donald"*) is `macarena:donald` in prose: the subject is the username, the fixation is the password. Anything a box bothers to drop in an anonymous FTP root or a share is there for you to read ([[dance-samba]], cf. [[chmod-4755]]'s "read better"). A hint can also be a *pointer* instead of the secret itself — *"la clave está en `/root/clave.txt`, menos mal que nadie tiene permisos"* leads to a sudo'd `grep` that reads it anyway ([[dockerlabs-box]]).
- **Credential files in odd paths** — dot-directories hide them (`~/.-/.miscredenciales`), and the file tells you what it's *for* ("Usa mis pass para escalar"). The password may not even be Latin script: this one was Braille → [[steganography]]. A second file next door (`/home/maria/.mipass` written as `maria:asientiendesmejor`) is a credential pair handed over in `user:pass` form ([[rutas]]).
- **Steganographic credential** — a password that arrives from *inside* an image rather than from text: `steghide` → `passwd.zip` → `hackeada:denuevo`, then replayed as an `Authorization: Basic` header. Whatever you pull out of a carrier is a credential until proven otherwise ([[rutas]], [[steganography]]).
- **Lone token with no username** — a random 14-char string served as a whole page (`<h1>JIFGHDS87GYDFIGD</h1>` in `index.php`, hidden behind the default `index.html`): no `user:` label, no context, just a secret shaped like a password. It's half a credential pair — hand the *password* to hydra and fuzz the username axis instead ([[library]], [[ssh-bruteforce]]).
- **Stale planted pair** — a note hands you `dev:developer123` *while literally asking for it to be changed*; the replay fails, but failure splits the pair: the password is dead, the **username is certified** (the box wrote it down itself — it's real). Feed the surviving half to rockyou instead of discarding the find ([[pkgpoison]], [[ssh-bruteforce]]).

## Commands

```sh
cat ~/.bash_history
cat ~/.bashrc
grep -RniE 'pass(word)?|secret|token|key|pwd' /home /opt /var/www 2>/dev/null
```

## Seen in

[[balufood]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[pipepwned]], [[trailpack]], [[bruteshock]], [[acme]], [[internal]], [[cap]], [[flynn]], [[analyst]], [[chmod-4755]], [[dance-samba]], [[rutas]], [[extraviado]], [[jenkhack]], [[dockerlabs-box]], [[library]], [[pkgpoison]], [[pequeñas-mentirosas]], [[nexus]]
