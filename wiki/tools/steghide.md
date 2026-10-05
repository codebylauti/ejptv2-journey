---
type: tool
category: forensics
related: ["[[steganography]]"]
---

# Steghide

Embed and extract data hidden inside JPEG, BMP, WAV, and AU files.

## Command

```sh
steghide extract -sf carrier.jpg     # prompts for the passphrase → writes the hidden file
steghide info carrier.jpg            # what's embedded (still asks for the passphrase)
steghide embed -cf cover.jpg -ef secret.txt -p 'pass'   # the other direction
```

- `-sf` the carrier file · `-p` the passphrase (omit it to be prompted) · `-cf`/`-ef` cover/hidden file when embedding.
- **An empty Enter is a valid guess** — try your own loot (a password you cracked one stage ago, a username, a hint string) before you start guessing blind.
- **Nothing to try?** Hand the carrier to [[stegseek]], which brute-forces the passphrase from a wordlist instead of prompting. steghide *asks*; StegSeek *derives*.
- The output is just *a file*: `unzip` it, `cat` it, and keep following the chain — steghide is one link, never the end.

## Seen in

[[rutas]] (`crackpass.jpg` → `passwd.zip` → `pass` → `hackeada:denuevo`, the vhost's Basic-auth credential)
