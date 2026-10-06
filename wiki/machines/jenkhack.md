---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, curl, netcat]
techniques: [information-gathering, source-code-disclosure, hardcoded-credentials, encoded-credentials, jenkins-script-console-rce, reverse-shells, sudo-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[autoescuela]]", "[[extraviado]]"]
---

# Jenkhack

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/jenkhack.md)

Easy three-port box where the credentials for the service on **8080** are planted in the page on **80**, the lateral password is **ASCII85**, and root hides behind a sudo'd wrapper script with a writable callee.

## Path

1. **Recon** — `nmap -p- --open -sS --min-rate 5000` → `80` Apache 2.4.58 (*Hacker Nexus - jenkhack.hl*), `443` + `8080` **Jetty 10.0.13** (both with `robots.txt` disallowing `/`) ([[information-gathering]]).
2. **Web enum (port 80)** — the page hides three tokens: `<span class="hidden">jenkins-admin</span>`, `<span class="hidden">cassandra</span>`, `<span class="hidden">jenkhack.hl</span>`, with the image `alt`s repeating the first two. A `mailto:contact@jenkhack.hl` prompts the `/etc/hosts` entry. The pair is a **username and password whose names point at the *other* port** ([[source-code-disclosure]], [[hardcoded-credentials]]).
3. **Jenkins (port 8080)** — login panel accepts **`jenkins-admin:cassandra`** → **Script Console** → Groovy `ProcessBuilder` reverse shell to `172.17.0.1:443`, caught with `sudo nc -lvnp 443` → **`jenkins`** ([[jenkins-script-console-rce]], [[reverse-shells]]).
4. **Target list** — `cat /etc/passwd | grep /bin/bash` → `root`, `jenkins`, `jenkhack` (a queue, not a list — same read as [[file]]).
5. **Lateral: jenkins → jenkhack** — `find / -regex .*jenkhack.*` → `/var/www/jenkhack/note.txt` holds `jenkhack:` followed by an **ASCII85** blob (it contains a backtick — mind your quoting when decoding):

   ```sh
   python3 -c "import base64; print(base64.a85decode(b\"C1V9uBl8!'Ci*\`uDfP\").decode('utf-8'))"
   ```

   → **`jenkelmejor`** → `su jenkhack` → `cat user.txt` ([[encoded-credentials]]).
6. **Root — pinned wrapper, writable callee** — `sudo -l` → `(ALL : ALL) NOPASSWD: /usr/local/bin/bash`, a custom wrapper printing *"Welcome to the bash application!"*. It executes **`/opt/bash.sh`**; `/opt` is writable on this box (confirmed by the user — the writeup never shows it) → `mv /opt/bash.sh /opt/bash.sh.bak`, replace with `chmod 4755 /bin/bash` → run the wrapper → `/bin/bash -p` → `whoami` = `root` ([[sudo-abuse]]).

## Credentials / secrets

| Item | Value | Where |
|------|-------|-------|
| jenkins-admin (Jenkins :8080) | `cassandra` | hidden spans in the port-80 page |
| jenkhack | `jenkelmejor` | `/var/www/jenkhack/note.txt` (password stored as ASCII85) |
| root | *no password* | SUID `/bin/bash -p` after the wrapper overwrite |

## Takeaways

- **The HTML is the credential store, and it tells you where to use it.** `class="hidden"` spans pair user+pass in the source, and the words themselves (`jenkins-admin`) name the service waiting on the other port — credentials are also *pointers* ([[source-code-disclosure]]).
- **Admin panels are features, not vulnerabilities.** The Script Console executes Groovy *by design* — the attack was "log in", not "exploit" ([[jenkins-script-console-rce]], cf. [[autoescuela]]'s inspector).
- **Encoding difficulty is escalating, alphabet-first.** base64 on [[extraviado]], ASCII85 here: 4-char groups gave way to `!`–`u` punctuation runs. Identify the alphabet, then decode — `a85decode` and `b85decode` are *different* alphabets ([[encoded-credentials]]).
- **When the sudo command is pinned, attack the file it calls.** `/usr/local/bin/bash` is a wrapper with an absolute-path chain — no [[path-hijacking]] involved — so the payload goes into `/opt/bash.sh`, the callee ([[sudo-abuse]]).
- **A root-owned script is only as safe as its directory.** The writeup `mv`s a root file without comment; the vulnerability is that `/opt` allowed it.

## Gaps in the writeup

- **`# IP` header is empty** — `172.17.0.2` is only recoverable from the ping output.
- **Port 443 was scanned and abandoned.** Its `robots.txt` (one disallowed entry, same as 8080's) was never fetched, and the 443-vs-8080 Jetty relationship never explored.
- **The vhost step is unused.** `jenkhack.hl` was added to `/etc/hosts`, but every subsequent request shown is by raw `IP:8080` — vhost-dependent access is never demonstrated.
- **`/opt` permissions are never shown** — the actual flaw behind step 6. Post-run, the user confirmed they had write perms on `/opt`.
- **Wrapper argument handling is opaque.** `bash -p` on the first invocation is swallowed by the wrapper (*"This is the bash script running."*) — how (or whether) it forwards args is never revealed.
