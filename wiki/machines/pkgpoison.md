---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, hydra, strings]
techniques: [information-gathering, directory-fuzzing, hardcoded-credentials, source-code-disclosure, ssh-bruteforce, sudo-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[hedgehog]]", "[[library]]"]
---

# Pkgpoison

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/pkgpoison.md)

A planted password that *fails* still tells the truth: it certifies the username. From there — compiled Python leaking its constants through `strings`, and a sudo rule where the **wildcard is the vulnerability** (`pip3 install *`).

## Path

1. **Recon** — `ping` + `nmap -p- --open -sS --min-rate 5000` → `22` OpenSSH 8.2p1 Ubuntu + `80` Apache 2.4.41 with `http-title: **404 Not Found**` — the root path answers 404 ([[information-gathering]]).
2. **Dir fuzzing** — `gobuster dir` (DirBuster medium, `-x php,html,txt`) → `index.html` (200, 589 — the document exists even though `/` 404s), `notes/` (301), `server-status` (403) ([[directory-fuzzing]]).
3. **Planted pair** — `curl http://172.17.0.2/notes/note.txt`: an admin *asking* dev to change the password that is sitting right there in the note — `dev:developer123` ([[source-code-disclosure]], [[hardcoded-credentials]]).
4. **The replay that fails usefully** — `ssh dev@172.17.0.2` with `developer123` is refused: the warning was heeded, the password changed. But the note's *identity* survived — `dev` is a real account, so the failed login just promoted a guess to a candidate ([[hardcoded-credentials]]).
5. **Foothold** — `hydra -l dev -P rockyou.txt ssh://… -vV -t 64` → **`dev:computer`** → `ssh dev@172.17.0.2` ([[ssh-bruteforce]]).
6. **User enum** — `cat /etc/passwd | grep /bin/bash` → `root`, `dev` (1000), **`admin`** (1001) — the queue-not-list read ([[jenkhack]]).
7. **Lateral: dev → admin — the compiler ratted** — `find / -name *secret*` (mind the unquoted glob — it survives only because nothing in the cwd matched) → `/opt/scripts/__pycache__/secret.cpython-38.pyc`. Python caches compiled modules, and the constant pool keeps every string literal verbatim:

   ```sh
   strings secret.cpython-38.pyc
   # adminz
   # p@$$w0r8321z
   ```

   The trailing `z` is **not part of the secret** — `strings` glues on the *next* marshal object's tag byte (reproduced locally: `adminz`, `p@$w0r8321N)`). Trim → `su admin` with **`admin:p@$$w0r8321`** ([[source-code-disclosure]], [[strings]]).
8. **Root — the wildcard is the payload** — `sudo -l` → `(ALL) NOPASSWD: /usr/bin/pip3 install *`. Nothing is pinned: *you* choose the directory, so you bring your own code:

   ```sh
   echo 'import os; os.system("exec /bin/sh </dev/tty >/dev/tty 2>/dev/tty")' > /tmp/setup.py
   cd /tmp && sudo -u root /usr/bin/pip3 install .
   ```

   pip executes `setup.py` during install — as root → `whoami` = `root` ([[sudo-abuse]], [[gtfobins]]).

## Credentials / secrets

| Item | Value | Where |
|------|-------|-------|
| dev (SSH) | `computer` | rockyou — the planted `developer123` had already been changed |
| admin | `p@$$w0r8321` | `strings` on `__pycache__/secret.cpython-38.pyc` (trailing `z` = marshal tag artifact) |
| root | *no password* | `sudo pip3 install *` + malicious `setup.py` |

## Takeaways

- **A leaked password that fails is still intel.** `dev:developer123` died as a credential but lived on as *proof*: the admin's note named a real account and even predicted the rotation. Failed replay ≠ dead end — it converts a guess into a guaranteed-valid username for hydra ([[hardcoded-credentials]]).
- **`/` is not the site.** nmap's title said `404 Not Found` while `/index.html` was a live 200 — never write off a host because the root path is empty; fuzz first ([[directory-fuzzing]]).
- **Compilation strips whitespace, not secrets.** A `.pyc` holds no source *text*, but every string literal rides along in the constant pool — `strings` reads them back. And the output is raw: trailing `z`/`Z`/`N)` bytes are neighboring marshal/code-object fragments, so trim, then verify against the login ([[strings]]).
- **A sudo wildcard on a package manager is a shell.** Contrast the *pinned* shapes elsewhere in this vault ([[secretjenkins]], [[file]]: payload into the file the command reads) — `pip3 install *` pins nothing, so the payload is a directory you own. `install` means *run this project's code*; pip is an interpreter with extra steps ([[sudo-abuse]]).
- **`sudo -l` after the hop** — the pip rule belonged to `admin`, not to the `dev` foothold where the chain started.

## Gaps in the writeup

- **No `sudo -l` on record as `dev`.** The chain jumps from foothold to file-hunting; whatever `dev` could do directly (if anything) is unstated.
- **Which string variant authenticated is unshown.** The prose says `p@$$w0r8321`, `strings` prints `p@$$w0r8321z`, and the `su admin` transcript (prompt + input) is absent — marshal analysis says trim the `z`, but the box never proves it.
- **`notes/` was entered, not enumerated.** `note.txt` was fetched straight from gobuster's result — no listing, no check for sibling files.
- **pip's environment is unspecified.** No `pip3 --version`, no behavior notes — the legacy `setup.py` execution path this exploit rides has been shrinking under PEP 517, so the payload's portability to a current pip is asserted by one run, not argued.
- **`server-status` 403 left at the status code**, and no flags on record — the writeup ends at `whoami`.
