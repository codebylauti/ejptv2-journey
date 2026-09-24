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

## OS password hashes (`/etc/shadow`)

Shadow entries use `crypt(3)` formats, identified by their `$id$` prefix:

- `$y$` — **yescrypt** (Debian 11+/12 default), `$6$` — SHA-512, `$5$` — SHA-256, `$1$` — MD5, `$2a/b/y$` — bcrypt.

Crack with john's `crypt` format (a `libcrypt` wrapper that handles all of the above):

```sh
echo 'user:$y$j9T$salt$hash:...' > hash.txt
john --format=crypt --wordlist=/usr/share/wordlists/rockyou.txt hash.txt
```

yescrypt is memory-hard → wordlist (+ rules), not brute force.

## Example

[[wargames]]: SHA-256 `60a3f3cb…` → `1983@1983` via hashes.com (not in rockyou). [[bruteshock]]: yescrypt `$y$` shadow hash → `salvador1` via `john --format=crypt`.

## Seen in

[[wargames]], [[bruteshock]]
