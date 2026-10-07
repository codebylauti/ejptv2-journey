---
type: tool
category: forensics
related: ["[[source-code-disclosure]]", "[[hardcoded-credentials]]"]
---

# Strings

Dump the printable character runs out of *any* file — binaries, compiled bytecode, pcaps, firmware. When a file isn't text, this is how you read its text.

## Command

```sh
strings file                    # runs of ≥4 printable chars (the default)
strings -n 8 file               # raise the minimum — less noise
strings file | grep -iE 'pass|user|secret|token|key'
```

- `-n <len>` minimum run length; default 4 is greedy and will show you plenty of junk.
- Output is **candidates, not facts** — everything here is a string that *exists* in the file, not a string that is *used*.

## What it's good for

- **Compiled Python (`.pyc`)** — Python strips your source, not your secrets: every string literal lives on in the module's constant pool. `strings __pycache__/x.cpython-*.pyc` recovered a full `user:password` pair on [[pkgpoison]] ([[source-code-disclosure]]).
- **Captures and uploads** — `strings <pcap> | grep -E 'USER|PASS'` pulls FTP/HTTP-auth credentials in one shot ([[analyst]], [[cap]], see [[pcap-analysis]]).
- **Binaries** — usage text, hardcoded URLs, API keys, even *prompts* that hint at hidden commands.

## Gotchas

- **Trailing junk is normal.** Runs are cut by non-printable bytes, so a constant sitting next to a bytecode/marshal tag comes out glued: `strings` on a `.pyc` gave `adminz` and `p@$w0r8321N)` where the real strings were `admin` and `p@$w0r8321` — the `z`/`N)` are the *neighboring* object's bytes (CPython marshal tags), not part of the secret ([[pkgpoison]]). **Trim, then verify against a login** — never replay the raw run.
- **False confidence runs both ways.** A perfect-looking password may be dead code or an example; a truncated one may be the live secret cut short by an unlucky byte. The file tells you what's *stored*, the target tells you what *works*.

## Seen in

[[cap]] (pulled `USER`/`PASS` out of the downloaded pcap — folded into [[hardcoded-credentials]] at the time), [[pkgpoison]] (`strings` on `secret.cpython-38.pyc` → `admin:p@$$w0r8321`, the lateral-movement pivot)
