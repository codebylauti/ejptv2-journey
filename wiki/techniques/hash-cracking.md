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

## Mangling rules (best64)

When the plaintext isn't a raw dictionary word, apply John's built-in `best64` rule — ~64 common mutations (capitalize, append `123`/`!`, etc.):

```sh
john --format=raw-sha512 --wordlist=rockyou.txt --rules=best64 hash.txt
```

- `--rules=best64` catches `Password1`, `word123`, … derived from a base word + a common twist.
- A target's own note may literally hint it: *"password uses best64"* ([[madeyes-castle]] → `wingardiumleviosa123`).

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

[[wargames]], [[bruteshock]], [[madeyes-castle]] (SHA-512 + `--rules=best64`)
