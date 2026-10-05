---
type: tool
category: cracker
related: ["[[ssh-key-cracking]]"]
---

# John the Ripper

Password/hash cracker — cracks SSH key passphrases, ZIP passwords, and OS hashes.

## Command

```sh
ssh2john id_rsa > hash.txt
john hash.txt --wordlist=/usr/share/wordlists/rockyou.txt

# ZIP archives
zip2john archive.zip > hash.txt
john hash.txt

# OS shadow hashes (crypt(3): $y$ yescrypt, $6$ SHA-512, ...)
echo 'user:$y$j9T$salt$hash:...' > hash.txt
john --format=crypt --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
john --show hash.txt

# bare hashes with no context — pick the format from the length (32 hex = MD5, 40 = SHA-1)
echo '53dd9c6005f3cdfc5a69c5c07388016d' > hash.txt
john --format=raw-MD5 hash.txt
john --format=raw-sha1 --wordlist=/usr/share/wordlists/rockyou.txt hash.txt

# mangling rules (best64) — catch word123 / Word! derived from a base word
john --format=raw-sha512 --wordlist=rockyou.txt --rules=best64 hash.txt
```

## Seen in

[[basic-pentesting]], [[nodeclimb]], [[bruteshock]] (yescrypt shadow hash, `--format=crypt`), [[madeyes-castle]] (SHA-512 + `--rules=best64` → `wingardiumleviosa123`), [[rutas]] (`zip2john` on `respeta.zip` → `greenday`), [[file]] (`--format=raw-MD5` on an FTP file → a *username*; `--format=raw-sha1` on a steghide output → the next user's password)
