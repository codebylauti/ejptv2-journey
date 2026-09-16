---
type: technique
tags: [ejpt:host-net-pentest]
tools: [john-the-ripper]
cves: []
related: [[ftp-anonymous-login]], [[ssh-key-cracking]]
---

# Zip Cracking

Recovering the password of an encrypted ZIP archive.

## Workflow

1. Convert the archive to a john hash: `zip2john archive.zip > hash.txt`.
2. Crack: `john hash.txt`.
3. Extract: `unzip archive.zip` with the recovered password.

## Seen in

[[nodeclimb]] (`secretitopicaron.zip` → `password1`)
