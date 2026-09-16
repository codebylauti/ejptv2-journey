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
```

## Seen in

[[basic-pentesting]], [[nodeclimb]]
