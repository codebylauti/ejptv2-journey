---
type: technique
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
tools: [curl]
cves: []
related: ["[[source-code-disclosure]]", "[[hardcoded-credentials]]", "[[steganography]]", "[[acrostic-decoding]]"]
---

# Encoded Credentials

Secrets that are **visible but transformed** — base64 (and its cousins) sitting in plain sight in a page body, an HTTP response, or a file on disk. Encoding is not encryption: no key, fully reversible with a one-liner.

## Spotting it

- **base64** — alphabet `A–Za–z0–9+/`, length a multiple of 4, `=` padding. A string that reads as printable nonsense but has those two traits is a candidate, not a hash.
- **ASCII85 (base85)** — the high-bit-safe cousin: alphabet runs `!`–`u` with **no padding**, so punctuation-heavy runs are the tell (``C1V9uBl8!'Ci*`uDfP``). Decode with `base64.a85decode` — **not** `b85decode`: a85 (Adobe/ASCII85) and b85 (RFC 4648) are different alphabets, and the wrong one yields mojibake ([[jenkhack]]).
- **Pairs** — once decoded, credentials often arrive as `user : pass` or `user:pass`. Decode *both* halves of a pair; either side can be the username ([[extraviado]]).
- **A file that claims to hold a secret** may hold an *encoding* instead — check before feeding it to john ([[hash-cracking]]'s "Encoding ≠ hashing": a `hash` file that survived `base32 -d | base64 -d` on [[dance-samba]]).

## Workflow

1. **Find the blob** — read the whole response, not just what renders. `curl -s http://TARGET/ | tail -1` caught a default Apache page whose *last line* was the payload ([[extraviado]]); on-box, `find` by name (`*diego*`, `.*pass.*`) surfaces the files holding one.
2. **Decode**:

   ```sh
   echo 'ZGFuaWVsYQ==' | base64 -d     # → daniela
   echo 'JBSWY3DPEB3W64TMMQ=======' | base32 -d
   python3 -c "import base64; print(base64.a85decode(b'...').decode())"   # ASCII85
   ```

3. **Replay** — the decoded pair is a credential until proven otherwise: `ssh user@TARGET` directly. A password you *decoded* needs no brute-force ([[hardcoded-credentials]]).

## Why it works

- Encoding exists for **transport safety**, not secrecy — but box authors (and developers) reach for it when they want something that isn't "plain text" in the source. A casual reader sees noise; a reader who decodes sees `daniela:focaroja`.
- It's the mildest member of the hidden-secret family: [[steganography]] hides data *inside* a carrier, [[acrostic-decoding]] hides it in *structure*, and here the data is fully in the open — only the alphabet is wrong.
- **Decoding beats guessing every time.** Before `john`, before rockyou: ask whether the string is merely *formatted*, not *hashed* ([[hash-cracking]]).

## Seen in

[[extraviado]] (base64 `user : pass` in the default page body + base64 password files), [[dance-samba]] (on-disk "hash" was stacked base32+base64 — decoded, never cracked), [[jenkhack]] (ASCII85 password in `note.txt`), [[amor]] (the *output of a steghide extraction* was base64 — `ZXNsYWNhc2FkZXBpbnlwb24=` → `eslacasadepinypon` → `su oscar`; the blob wore the alphabet, not a hash)
