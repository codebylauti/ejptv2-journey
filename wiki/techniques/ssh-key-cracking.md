---
type: technique
tags: [ejpt:host-net-pentest]
tools: [john-the-ripper]
cves: []
related: [[ssh-bruteforce]]
---

# SSH Key Cracking

Cracking the passphrase of a discovered private SSH key.

## Workflow

1. Convert the key for john: `ssh2john id_rsa > hash.txt`.
2. Crack: `john hash.txt --wordlist=rockyou.txt`.
3. Use the recovered passphrase to authenticate.

## Seen in

[[basic-pentesting]] (`kay`'s key passphrase `beeswax`)
