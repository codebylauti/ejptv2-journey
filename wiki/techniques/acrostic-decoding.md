---
type: technique
tags: [ejpt:web-pentest, ejpt:assessment]
tools: [curl]
cves: []
related: ["[[source-code-disclosure]]", "[[encoded-credentials]]"]
---

# Acrostic Decoding

Recovering a hidden message (often a password) where the **first letter of each line/heading spells it out** — an "acrostic". The clue to look for it is usually itself hidden in the page source (`acrostico`, "initial letters", etc.).

## Workflow

1. **Spot the hint** — a page attribute or comment like `<article hidden="acrostico inicial">` ([[winfake]]) signals that headings/titles encode something.
2. **Extract the first letters** — pull each heading's first character in order:

   ```sh
   curl -s http://TARGET/ | grep h2 | tr '><' ' ' | awk '{print substr($2, 1, 1)}'
   ```

3. **Interpret** — the letter run `HWINSERVERROOTFAKENEWS` reads as `WinServerRootFakeNews`, reused as the **root password** (`su root`).

## Why it works

- The plaintext message is visible but **not obvious** — a mild form of steganography; anyone who reads only *content* misses it, while reading *structure* reveals it ([[steganography]] covers the stronger versions: data hidden *inside* a file, or written in another alphabet).
- It's a natural fit for "riddle"-style boxes where a [[source-code-disclosure]] clue points at the encoding instead of a raw secret. The sibling pattern — a poem whose *answer* is the password (`osopolar` from the polar-bear riddle on [[extraviado]]) — hands you the derivation function and asks you to supply the value.

## Seen in

[[winfake]]
