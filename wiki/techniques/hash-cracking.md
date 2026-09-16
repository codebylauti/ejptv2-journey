---
type: technique
tags: [ejpt:host-net-pentest]
tools: [john-the-ripper]
cves: []
related: [[ssh-key-cracking]], [[zip-cracking]]
---

# Hash Cracking

Recovering the plaintext behind a raw password hash (MD5, SHA-1, SHA-256, …).

## Workflow

1. **Identify the type** — length + alphabet (`hashid`). 32 hex = MD5, 40 = SHA-1, 64 = SHA-256.
2. **Local wordlist** — `john --format=raw-sha256 --wordlist=rockyou.txt hash.txt`, or `hashcat -m 1400 -a 0 hash.txt rockyou.txt`.
3. **Online lookup** — if wordlists miss, submit to a pre-computed database (hashes.com, crackstation.net); breach dumps often contain what `rockyou` does not.
4. **Brute force / masks** — last resort for short or pattern-based passwords.

## Verify a candidate instantly

```sh
printf '%s' "candidate" | sha256sum   # compare against the target hash
```

## Example

[[wargames]]: SHA-256 `60a3f3cb…` → `1983@1983` via hashes.com (not in rockyou).

## Seen in

[[wargames]]
