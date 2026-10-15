---
type: technique
tags: [ejpt:web-pentest]
tools: [curl]
cves: []
related: ["[[local-file-inclusion]]", "[[source-code-disclosure]]", "[[gitea]]", "[[directory-fuzzing]]"]
---

# Path Traversal (arbitrary file read)

Reading arbitrary files when a request parameter becomes a filesystem path with no normalization or validation — any `filename`/`file`/`page`/`template` input that is joined onto a base directory and served back.

## Variants

- **Relative traversal** — `?filename=../../../etc/passwd` escapes the intended directory.
- **Absolute path** — some sinks accept `/etc/passwd` outright, with no `../` at all. Python's `os.path.join(base, filename)` *discards the base* when the second argument is absolute, so a naive join plus `os.path.exists` + open is a complete arbitrary read ([[gitea]]'s `/download` endpoint did exactly this).

```sh
curl -s "http://TARGET/download?filename=/etc/passwd"
```

## Aim, don't fuzz

Fuzzing finds the *endpoint*; source intelligence aims it:

1. **Find** the parameterized route (directory fuzzing → `/download` 302 → the parameter name arrives from reading the app's own source/history, not from a parameter wordlist).
2. **Read files that change your next step** — a two-step pattern, not a one-shot:
   - `/etc/passwd` → **user enumeration** (names feed [[ssh-bruteforce]]'s `-l`),
   - a config/wordlist file → credentials for the *next* service.

On [[gitea]] one endpoint yielded both halves: `user.txt`-class user enum from `/etc/passwd`, then a 50-pair wordlist from `/opt/info.txt` — the file itself targeted because a *cloned repo's* volume entry (`/opt/"INFO_FILE"`) pointed at it ([[source-code-disclosure]]).

## Serve ≠ include (how this differs from LFI)

[[local-file-inclusion]] is an **include** sink: PHP (`include`/`require`) executes or renders the file, which is why LFI chains to RCE ([[log-poisoning]]). A download endpoint is a **serve** sink: nothing runs, the server just returns bytes. Same `../` payload, different class — decide by what the response *does*, not by the parameter name. The payoff of serve-only traversal is data (credentials, configs, hashes), which is usually all you need.

## The recon lesson

On [[gitea]] the vulnerability was never *tested* into existence — it was **read**: the app's own git history carried the comment `# **Vulnerabilidad**: No se valida el path, permitiendo Path Traversal` above the unsanitized `os.path.join`. Diff history is a disclosure channel for *bugs*, not just secrets ([[source-code-disclosure]], cf. [[nexus]]'s git-history password).

## Seen in

[[gitea]] (`/download?filename=` accepted absolute paths — `/etc/passwd` for user enum, `/opt/info.txt` for the SSH wordlist; vulnerability pre-confirmed by the repo's `git diff`)
