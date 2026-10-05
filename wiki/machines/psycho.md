---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, dirb, ffuf, curl]
techniques: [parameter-fuzzing, local-file-inclusion, sudo-abuse, python-library-hijacking]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[hannah-coffee]]", "[[nodeclimb]]"]
---

# Psycho

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/psycho.md)

Easy box that chains a hidden-parameter LFI → SSH key theft → two chained `sudo` escapes.

## Path

1. **Recon** — `nmap` shows `22/tcp ssh` (OpenSSH 9.6p1) and `80/tcp http` (Apache 2.4.58, "4You").
2. **Dir fuzzing** — `dirb` finds a listable `/assets/` directory and `index.php`.
3. **Parameter fuzzing** — `ffuf` discovers the hidden `secret` parameter ([[parameter-fuzzing]]).
4. **LFI** — `?secret=../../../../../etc/passwd` reads `/etc/passwd`, revealing `vaxei` (1001) and `luisillo` (1002) ([[local-file-inclusion]]).
5. **SSH key theft** — the LFI reads `/home/vaxei/.ssh/id_rsa` → `ssh vaxei@… -i id_rsa`.
6. **→ luisillo** — `sudo -l`: `(luisillo) NOPASSWD: /usr/bin/perl`; `sudo -u luisillo perl -e 'exec "/bin/sh"'` ([[sudo-abuse]]).
7. **→ root** — `sudo -l`: `(ALL) NOPASSWD: /usr/bin/python3 /opt/paw.py`. `/opt` is directory-writable, so `rm /opt/paw.py` and rewrite it with a shell spawn, then `sudo python3 /opt/paw.py` → root.

## Credentials / secrets

| Item | Value |
|------|-------|
| LFI parameter | `secret` |
| vaxei | `id_rsa` (read via LFI) |
| sudo (vaxei) | `(luisillo) NOPASSWD: /usr/bin/perl` |
| sudo (luisillo) | `(ALL) NOPASSWD: /usr/bin/python3 /opt/paw.py` |

## Takeaways

- Hidden parameters are found with `ffuf`, not `dirb` ([[parameter-fuzzing]]).
- An LFI can read SSH keys directly for a foothold ([[local-file-inclusion]]).
- `sudo perl -e 'exec "/bin/sh"'` is a clean shell escape ([[sudo-abuse]]).
- A root-owned script in a *writable directory* can be `rm`'d and replaced — directory write ≠ file write.
- Alternative: shadow the `subprocess` import (not `os`, which is pre-imported) — [[python-library-hijacking]].
