---
type: technique
tags: [ejpt:host-net-pentest]
tools: [john-the-ripper]
cves: []
related: ["[[ftp-anonymous-login]]", "[[ssh-key-cracking]]"]
---

# Zip Cracking

Recovering the password of an encrypted ZIP archive.

## Workflow

1. Convert the archive to a john hash: `zip2john archive.zip > hash.txt`.
2. Crack: `john hash.txt`.
3. Extract: `unzip archive.zip` with the recovered password.

**Reuse what comes out.** The recovered password is usually the passphrase for the *next* container in the chain (a `steghide` image, another archive) — and if the archive's own hint names the next file, you're being handed a route, not just a file ([[steganography]]).

## Seen in

[[nodeclimb]] (`secretitopicaron.zip` → `password1`), [[rutas]] (`respeta.zip` → `greenday` → `oculto.txt` naming the image to go steal next)
