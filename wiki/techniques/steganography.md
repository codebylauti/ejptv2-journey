---
type: technique
tags: [ejpt:assessment, ejpt:host-net-pentest]
tools: [steghide]
cves: []
related: ["[[zip-cracking]]", "[[source-code-disclosure]]", "[[hash-cracking]]"]
---

# Steganography

Hiding a secret *inside* a carrier file (image, audio, archive) so it is invisible to anyone who only opens the carrier. You don't break cryptography — you notice that something is being concealed, then decode it.

## Workflow

1. **Get told where the carrier is.** Boxes that use stego almost always hand you the filename and host in a hint first (*"Consigue la imagen crackpass.jpg — firstatack.github.io"*). Stego is the **second** step of a chain, never the entry point ([[ftp-anonymous-login]], [[source-code-disclosure]]).
2. **Pull the carrier** — `wget https://<host>/assets/<image>.jpg`. It may live on the *author's* domain, not on the target: the hint told you where to go, so going there is in-scope recon ([[wget]]).
3. **Extract** — `steghide` wants the carrier and the passphrase ([[steghide]]):

   ```sh
   steghide extract -sf carrier.jpg      # prompts for the passphrase
   unzip out.zip && cat <file>
   ```

4. **Passphrase you don't have?** An empty Enter is a valid guess (some carriers embed with none), and the real passphrase is nearly always a value **you already own** — the password you cracked one stage ago, a username, a hint string. Try your own loot before you guess ([[zip-cracking]]).

## Other shapes of the same idea

- **Concealment by alphabet** — the secret is written in another script (Braille, Morse, base-N) inside an otherwise readable file. You *decode* it, you don't crack it ([[hash-cracking]] on encoding vs hashing).
- **Metadata** — EXIF in an image can hold usernames or locations ([[borazuwara]]).
- **Structure over content** — first letters of headings spell the password ([[acrostic-decoding]]): the message is in *how* it's written, not *what* it says.

## Seen in

[[rutas]] (`respeta.zip` → `oculto.txt` → `crackpass.jpg` → `steghide` → `passwd.zip` → `pass` → `hackeada:denuevo`, which became the vhost's HTTP Basic-auth credential)
