---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, whatweb, hydra, john-the-ripper, find]
techniques: [information-gathering, directory-fuzzing, ssh-bruteforce, hash-cracking, sudo-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[winfake]]", "[[library]]", "[[file]]", "[[secretjenkins]]"]
---

# Pequeñas Mentirosas

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/pequeñas-mentirosas.md)

A box that *tells you what to do* — the whole site is a one-line hint ("*find the key for A in the files*") — and then pays off in three small moves: the hint's `A` becomes a hydra username, a `find` by username surfaces a planted MD5, and a single `sudo python3 -c` ends it.

## Path

1. **Recon** — `ping` + `nmap -p- --open -sS --min-rate 5000` → **22** (OpenSSH 9.2p1 Debian) + **80** (Apache 2.4.62 Debian, titleless) ([[information-gathering]]).
2. **The site is the hint** — `curl` the root: `<h1>Pista: Encuentra la clave para A en los archivos.</h1>` (85 bytes, the entire `index.html`). Gobuster over DirBuster-medium + 7 extensions (**1.66 M requests**) returns exactly two things: `index.html` (200, 85) and `server-status` (403). `whatweb` adds nothing. The web surface is exhausted — nothing is *hidden*, the page is *pointing* ([[directory-fuzzing]]).
3. **Read the direction instead of fighting it** — "the key for **A**" → treat `A` as a system user → `hydra -l a -P rockyou.txt ssh://172.17.0.2 -vV -t 64` → **`a:secret`** → `ssh a@172.17.0.2` ([[ssh-bruteforce]]).
4. **User enum** — `grep /bin/bash /etc/passwd` → `root`, `spencer` (1000), `a` (1001).
5. **Lateral: a → spencer** — `find / -name *spencer*` → **`/srv/ftp/hash_spencer.txt`** holding `7c6a180b36896a0a8c02787eeafb0e4c` (32 hex = MD5) → `john --format=raw-MD5 --wordlist=rockyou.txt` → **`password1`** → `su spencer` ([[find]], [[hash-cracking]], [[hardcoded-credentials]]).
6. **Lateral: spencer → root** — `sudo -l` → `(ALL) NOPASSWD: /usr/bin/python3` → the payload rides in the flag:

   ```sh
   sudo -u root /usr/bin/python3 -c 'import os; os.execl("/bin/bash", "bash")'
   ```

   `whoami` → **`root`** ([[sudo-abuse]], [[gtfobins]]).

## Credentials / secrets

| Account | Secret | Where it came from |
|---------|--------|--------------------|
| `a` | `secret` | hydra + rockyou, username derived from the page hint |
| `spencer` | `password1` | raw MD5 in `/srv/ftp/hash_spencer.txt` → john |

## Takeaways

- **A page that talks is enumeration too.** Gobuster burned 1.66 M requests for two hits while the answer was sitting in the 85 bytes you already read: a hint naming the *username axis*. When fuzzing a surface returns almost nothing, re-read what the surface *says* before assuming it's hiding more ([[ssh-bruteforce]], cf. [[library]]'s inverted axis).
- **The filename identifies the hash.** `hash_spencer.txt` answers two questions before you open it: *what* this is (a hash) and *who* it's for (spencer) — so you already know the `su` target before john even starts. Identification from the filename is the cheapest of the hash-cracking steps ([[hash-cracking]]).
- **`find / -name *<username>*` is the planted-credential sweep.** Once `/etc/passwd` gives you names, searching the filesystem for files *named after those users* hits what the box planted for them — third sighting of the pattern: `*diego*` ([[extraviado]]), `*secret*` (the `.pyc` on [[pkgpoison]]), now `*spencer*` ([[find]]). Quote the glob — `'…'` — or *your shell* eats the pattern first.
- **One python3 payload, three boxes.** `-c 'import os; os.execl("/bin/bash", "bash")'` under a sudo'd interpreter has now popped up as a capability escape ([[cap]]), a lateral pivot ([[secretjenkins]]), and here as the root rule itself. No pinned file, no GTFOBins hunt — an interpreter with `NOPASSWD` is already a shell ([[gtfobins]]).
- **Hints are a first-class source.** The vault has seen hints as riddles ([[extraviado]]), acrostics ([[winfake]]), gossip ([[dance-samba]]) — this one is a straight *instruction*. Whatever form they arrive in, treat box-authored prose as data: usernames, paths, and now "go attack SSH".

## Gaps in the writeup

- **The hinted files were never found.** "Find the key for A *in the files*" promises a file, and gobuster's two hits don't contain one — yet the writeup goes straight from hint to brute-force without ever showing which file held `a:secret` (if any did). The intended path is unreconstructed: either the key file sits below the wordlist/extension combo, or the hint was satisfied by assumption alone.
- **`server-status` (403) was never probed** — recurring blind spot across the vault's boxes.
- **`/srv/ftp` is FTP-shaped but port 21 is closed.** Whether that directory is served over HTTP (gobuster never tried `/ftp` or `/srv`) or reachable some other way was never tested — it only appears from the inside via `find`.
- **The `find` glob is unquoted** — `find / -name *spencer*` survives only because the writer's CWD had no matching file (same latent bug as [[extraviado]] and [[pkgpoison]]): the reproducible form is `find / -name '*spencer*'`.
- **No flags on record** — the chain ends at `whoami`, no `user.txt`/`root.txt`.
