---
type: tool
category: cracker
related: [[ssh-key-cracking]]
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
```

## Seen in

[[basic-pentesting]], [[nodeclimb]], [[bruteshock]] (yescrypt shadow hash, `--format=crypt`)
