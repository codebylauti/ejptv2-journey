---
type: tool
category: forensics
related: ["[[steganography]]", "[[steghide]]"]
---

# Stegseek

Brute-force cracker for **steghide** passphrases — runs a wordlist against the carrier instead of making you guess.

## Command

```sh
stegseek carrier.jpg wordlist.txt    # cracks and extracts in one shot
stegseek carrier.jpg                 # uses the default rockyou wordlist
```

- On success it prints the recovered passphrase, the **original embedded filename**, and writes the payload out next to the carrier (`carrier.jpg.out`, or the original name).
- This is the difference between [[steghide]] and StegSeek: steghide **prompts** for a passphrase you must supply; StegSeek **derives** it from a wordlist. Reach for the prompt when the passphrase is a value you already own (a password you cracked one stage ago, a username); reach for the cracker when you have nothing to try.
- The extracted file is rarely the end: it usually holds a hash or yet another password — keep going down the chain ([[hash-cracking]], [[steganography]]).

## Seen in

[[file]] (`dragon-medieval.jpeg` in fernando's home → passphrase `secret` → `pass.txt` → raw-SHA1 → `password123`, mario's password)
