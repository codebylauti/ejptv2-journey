---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: ["[[command-injection]]", "[[sudo-abuse]]"]
---

# Arithmetic Injection (bash `-eq`)

A bash script that compares attacker-controlled input with an **arithmetic** operator (`-eq`, `-ne`, `-lt`, `-gt`, …) in `[[ ]]` evaluates the input as an *arithmetic expression* — and bash arithmetic performs **command substitution**.

## Why it works

```bash
read -rp "Adivina: " num
if [[ $num -eq 123123 ]]   # -eq → arithmetic, NOT string comparison
```

`-eq` forces arithmetic evaluation of `$num`. Bash arithmetic executes `$(...)`, so input like:

```
a[$(/bin/bash -p >&2)]+123123
```

runs `/bin/bash -p >&2` (an interactive shell). The `a[...]` (array subscript) + `+123123` wrapping keeps the expression syntactically valid and makes it equal the target, so the comparison resolves cleanly.

- `>&2` routes stdout to stderr to dodge command-substitution capture — otherwise the shell's output is swallowed.
- `==` (string) would be safe; `-eq` is the footgun.

## Seen in

[[bruteshock]] (`script.sh` → shell as `maci`)
