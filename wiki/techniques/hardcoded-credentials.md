---
type: technique
tags: [ejpt:host-net-pentest, ejpt:assessment]
tools: []
cves: []
related: [[source-code-disclosure]]
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

## Commands

```sh
cat ~/.bash_history
cat ~/.bashrc
grep -RniE 'pass(word)?|secret|token|key|pwd' /home /opt /var/www 2>/dev/null
```

## Seen in

[[balufood]], [[grooti]], [[winfake]], [[duque]], [[injection]]
