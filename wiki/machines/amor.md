---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, curl, hydra, steghide, wget]
techniques: [information-gathering, source-code-disclosure, ssh-bruteforce, steganography, encoded-credentials, sudo-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[vacaciones]]", "[[file]]"]
---

# Amor

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/amor.md)

A "SecurSEC" news feed that narrates its own attack surface (two employees, one weak password), then a stego photo exfiltrated *in reverse* — the target hosted it, Kali downloaded it — and a one-line [[sudo-abuse|sudo ruby]] finish.

## Path

1. **Recon** — `ping` + `nmap -p- --open -sS --min-rate 5000` → `22` OpenSSH 9.6p1 Ubuntu + `80` Apache 2.4.58, title **SecurSEC S.L** ([[information-gathering]]).
2. **Web enum — read the story** — `curl http://172.17.0.2` returns six Spanish security bulletins. Nothing is hidden: the *body text* names the users. **Juan** was fired *"por enviar un correo con la contraseña a un compañero"*, **Carlota** signs from *"Departamento de ciberseguridad"*, and a third entry reports a **weak password** on an account — two candidate usernames plus an explicit mandate to brute-force ([[source-code-disclosure]]).
3. **Foothold** — `users.txt` = `juan`, `carlota` → `hydra -L users.txt -P rockyou.txt ssh://… -u -F -V -t 4` → **`carlota:babygirl`** → `ssh carlota@172.17.0.2` ([[ssh-bruteforce]]).
4. **User enum on-box** — `cat /etc/passwd | grep /bin/sh` → `carlota` (1001), **`oscar`** (1002) — the next door, same queue-not-list read as [[jenkhack]].
5. **Lateral: carlota → oscar — stego served by the target** — the carrier is sitting in plain sight: `~/Desktop/fotos/vacaciones/imagen.jpg`. To pull it, the writeup *reverses* the usual staging pair — the **target** hosts the directory (`python3 -m http.server 3000`) and Kali fetches it (`wget http://172.17.0.2:3000/imagen.jpg`). Then:

   ```sh
   steghide extract -sf imagen.jpg     # bare Enter accepted → secret.txt
   cat secret.txt                      # ZXNsYWNhc2FkZXBpbnlwb24=
   base64 -d secret.txt                # eslacasadepinypon
   ```

   → `su oscar` ([[steganography]], [[encoded-credentials]]).
6. **Root — ruby GTFOBins** — `Desktop/IMPORTANTE.txt` points at the desktop (*"Hola ROOT, acuérdate de mirar el documento de tu escritorio"*), then `sudo -l` → `(ALL) NOPASSWD: /usr/bin/ruby` → `sudo -u root /usr/bin/ruby -e 'exec "/bin/bash"'` → `whoami` = `root` → `/root/Desktop/THX.txt` (thanks to the DockerLabs community) ([[sudo-abuse]]).

## Credentials / secrets

| Item | Value | Where |
|------|-------|-------|
| carlota (SSH) | `babygirl` | rockyou against usernames read off the news feed |
| oscar | `eslacasadepinypon` | steghide (empty passphrase) → base64 decode of `secret.txt` |
| root | *no password* | `sudo`-allowed `ruby -e 'exec "/bin/bash"'` |

## Takeaways

- **Read the page like a story, not like a scanner.** The usernames were never in a comment or an attribute — they were *narrative*: a firing, a signature, a weak-password warning. [[vacaciones]] hid its pair in HTML comments; [[amor]] hid nothing, you just had to read ([[source-code-disclosure]]).
- **HTTP file transfer works in both directions.** The canonical pattern is attacker-hosts/target-pulls ([[wget]] staging during pivoting); here the target hosted the photo directory and Kali pulled it. `python3 -m http.server` + `wget` is a two-way tool — use whichever side can bind the port.
- **An empty Enter is a guess worth one second.** The steghide prompt was answered with bare `[[steghide|Enter]]` before ever reaching for a wordlist — the third empty-passphrase sighting in this vault ([[rutas]], [[file]]/[[stegseek]]).
- **Stego output arrived *encoded*, not hashed** — `ZXNsYWNhc2FkZXBpbnlwb24=` is base64 by eye (length ÷ 4, `=` padding): decode, don't crack. The decoded string then skipped brute-force entirely and went straight to `su` ([[encoded-credentials]]).
- **`sudo -l` after each hop** — the ruby rule belonged to oscar, not to the foothold you started with.

## Gaps in the writeup

- **`juan` was never tested.** The page practically accuses him (*"fired for sending the password by email"*) and warns the password is weak — the narrative's loudest hint pointed at an account hydra never reached once `carlota` fell first.
- **carlota's `sudo -l` is not on record.** The writeup jumps from `su oscar` to oscar's sudo rules — whatever carlota could (or couldn't) do was never captured.
- **The photo directory was treated as one file.** `imagen.jpg` was pulled and extracted; the rest of `vacaciones/` was never listed, and `steghide info` never run — a second carrier or an embedded-file list would go unread.
- **The desktop hint resolves to flavor text.** *"$ROOT, remember to look at the document on your desktop"* ends at `THX.txt` (a thank-you note) — the actual privesc (`sudo -l`) is unrelated to it, so the narrative promise and the exploit never meet.
- **No flags on record.** The chain ends at `whoami`/`ls /root` — no `user.txt` or `root.txt` capture.
