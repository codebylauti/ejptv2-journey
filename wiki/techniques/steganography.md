---
type: technique
tags: [ejpt:assessment, ejpt:host-net-pentest]
tools: [steghide, stegseek]
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

4. **Passphrase you don't have?** Three options, in order of how much you should trust them:
   - **Reuse a value you already own** — the password you cracked one stage ago, a username, a hint string. Try your loot before you guess ([[zip-cracking]]).
   - **An empty Enter** is a valid guess (some carriers embed with none).
   - **Crack it instead of guessing** — hand the carrier to [[stegseek]], which runs rockyou against the steghide passphrase and extracts in one shot. You never had to think of `secret` on [[file]]; you just had to know the cracker existed.
5. **Read what came out.** The payload is almost never the end — on [[file]] it was a bare 40-hex string (SHA-1) that became the *next* user's password ([[hash-cracking]]). Stego is a link in a chain, not a destination.

## Other shapes of the same idea

- **Concealment by alphabet** — the secret is written in another script (Braille, Morse, base-N) inside an otherwise readable file. You *decode* it, you don't crack it ([[hash-cracking]] on encoding vs hashing).
- **Metadata** — EXIF in an image can hold usernames or locations ([[borazuwara]]).
- **Structure over content** — first letters of headings spell the password ([[acrostic-decoding]]): the message is in *how* it's written, not *what* it says.
- **You don't always need to be *told* where the carrier is.** [[rutas]] handed you the filename in a hint; [[file]] just left `dragon-medieval.jpeg` sitting in a user's home directory after a `su`. Any image or audio file that arrived during enumeration is a candidate — `file`, then [[stegseek]].

## Seen in

[[rutas]] (`respeta.zip` → `oculto.txt` → `crackpass.jpg` → `steghide` → `passwd.zip` → `pass` → `hackeada:denuevo`, which became the vhost's HTTP Basic-auth credential), [[file]] (`dragon-medieval.jpeg` in fernando's home → `stegseek` brute-forced passphrase `secret` → `pass.txt` → raw-SHA1 → `password123`, mario's password)
