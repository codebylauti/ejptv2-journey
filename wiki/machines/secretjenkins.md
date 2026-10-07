---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: [CVE-2024-23897]
tools: [nmap, gobuster, whatweb, hydra]
techniques: [information-gathering, directory-fuzzing, ssh-bruteforce, sudo-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[jenkhack]]", "[[dark]]"]
---

# Secretjenkins

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/secretjenkins.md)

Jenkins 2.441 box where the version number *is* the exploit: **CVE-2024-23897** turns the CLI into a file reader, the file read into a two-name user list, and the rest is a textbook brute-force plus a two-hop sudo chain.

## Path

1. **Recon** — `ping` + `nmap -p- --open -sS --min-rate 5000` → `22` OpenSSH 9.2p1 Debian + `8080` **Jetty 10.0.18**. `curl robots.txt` answers with a joke that also names the app's verb: *"we don't want robots to click **build** links"*, `Disallow: /` ([[information-gathering]]).
2. **Web enum** — `gobuster dir` (DirBuster medium, `-x php,html,txt`) maps the admin surface without logging in: `login` (200), `builds` (200, 35 KB), and a fence of 403s — `script`, `configure`, `log`, `me`, `cloud` ([[directory-fuzzing]]). Then `whatweb` drops the decisive flag: `Jenkins[2.441]` + `x-jenkins` headers — an exact weekly version, **one patch below the CVE fix** ([[cve-2024-23897]]).
3. **Foothold — file read, not RCE** — Maalfer's [CVE-2024-23897 PoC](https://github.com/Maalfer/CVE-2024-23897) against `/etc/passwd`: `connect-node @/etc/passwd` makes the args4j parser substitute the file, and every line comes back inside a `No such agent "…" exists.` error. Among the noise: **`jenkins` (1000)**, **`bobby` (1001)**, **`pinguinito` (1002)** — three accounts with `/bin/bash` handed over before touching the login form ([[cve-2024-23897]]).
4. **SSH brute** — `users.txt` = the shells from that file read (not a guess) → `hydra -L users.txt -P rockyou.txt ssh://… -u -F -t 64` → **`bobby:chocolate`** → `ssh bobby@172.17.0.2` ([[ssh-bruteforce]]).
5. **Lateral: bobby → pinguinito** — `sudo -l` → `(pinguinito) NOPASSWD: /usr/bin/python3`. The binary *is* the payload — no file to write:

   ```sh
   sudo -u pinguinito /usr/bin/python3 -c 'import os; os.execl("/bin/bash", "bash")'
   ```

6. **Root — pinned python, writable script** — `sudo -l` again as pinguinito → `(ALL) NOPASSWD: /usr/bin/python3 /opt/script.py`. This time the command line is pinned, so the payload moves *into the file*: `mv /opt/script.py /opt/script.py.bak`, write `import os; os.execl("/bin/bash", "bash")` to `/opt/script.py` → `sudo -u root /usr/bin/python3 /opt/script.py` → `whoami` = `root` ([[sudo-abuse]]).

## Credentials / secrets

| Item | Value | Where |
|------|-------|-------|
| bobby (SSH) | `chocolate` | rockyou against the CVE-read user list |
| pinguinito | *no password* | reached via `sudo -u … python3`, not `su` |
| root | *no password* | overwrite of pinned `/opt/script.py` |

## Takeaways

- **A version banner is an attack path.** `whatweb` printing `Jenkins[2.441]` was the whole box: exact version → advisory lookup → public PoC. Same reflex as `vsftpd 2.3.4` ([[cve-2011-2523]]) — fingerprint first, then CVE, not the other way around.
- **A file read buys you a wordlist.** The CVE's only job was turning "who do I brute-force?" into a two-entry list. Unauthenticated brute-force of unknown usernames vs. two derived candidates — same lesson as [[dark]]'s LFI'd `/etc/passwd` ([[ssh-bruteforce]]).
- **403s are a floor plan.** `script`/`configure`/`log` refusing you *pre-auth* proves an admin layer exists and names its exact URLs — the door you'll want after the exploit.
- **The same pinned-sudo shape, two hops, two payloads.** Hop 1 (`sudo -u pinguinito python3`) abuses the interpreter *itself* with `-c`; hop 2 pins a **file argument**, so the payload has to live in `/opt/script.py` — identical to [[file]]/[[psycho]], and the opposite door from [[library]], which shadowed the import instead of overwriting the script ([[sudo-abuse]]).
- **`sudo -l` after every hop** paid for both rungs of the chain — bobby's rule was pinguinito's, pinguinito's was root's.

## Gaps in the writeup

- **The CVE's crown jewels were skipped.** The advisory's whole point is reading `/var/jenkins_home/secrets/master.key`, `credentials.xml`, and `users/*/config.xml` → authenticate → Script Console RCE. The writeup read `/etc/passwd` and left Jenkins forever — no attempt to loot the secrets dir, even though the PoC was already in hand.
- **The harvested SSH creds were never replayed on :8080.** `bobby:chocolate` against `/login` is untested — a one-request check that would have told you whether the password is shared across services ([[jenkhack]]'s pair worked exactly that way).
- **`jenkins` (UID 1000) was enumerated and dropped** — the service account with the most interesting home directory never became a hydra candidate or an SSH target.
- **No flags on record.** The writeup ends at `whoami` — no `user.txt`/`root.txt` capture, and no `id`/`sudo -l` output shown as bobby before the first hop (the rule is only visible as its result).
