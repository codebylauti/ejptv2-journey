---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, dirb, ffuf, curl, netcat]
techniques: [directory-fuzzing, parameter-fuzzing, local-file-inclusion, log-poisoning, reverse-shells, sudo-abuse, linux-capabilities]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: [[los-3-hackers]], [[adopting]]
---

# Hannah Coffee

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/hannah-coffee.md)

Easy box that chains [[local-file-inclusion|LFI]] + [[log-poisoning]] for RCE, then a `debugfs` [[sudo-abuse]] and a `cap_setuid` [[linux-capabilities]] escalation.

## Path

1. **Recon** — `nmap` shows `21/tcp ftp` (vsftpd 3.0.5) and `80/tcp http` (Apache 2.4.68).
2. **Dir fuzzing** — `dirb` finds `index.php` and a listable `/pages/` directory; the site uses `?page=` for pages.
3. **Parameter fuzzing** — [[ffuf]] discovers a hidden `studio` parameter on `index.php`.
4. **LFI** — `?studio=../../../etc/passwd` reads `/etc/passwd`, revealing users `hannahftp` and `hannah`.
5. **Log poisoning** — inject `<?php system($_GET['cmd']); ?>` as the FTP username; include `/var/log/vsftpd.log` via the LFI → RCE.
6. **Reverse shell** — use the RCE to spawn a bash reverse shell as `www-data`.
7. **Escalation to hannah** — `sudo -l` shows `(hannah) NOPASSWD: /sbin/debugfs -w /opt/hannah_disk.img`; read `hannah_secret.txt` from the image, then `!/bin/bash` escapes to a shell as `hannah`.
8. **Escalation to root** — `getcap -r /` finds `/opt/priv-python cap_setuid=ep`; `os.setuid(0); os.execl("/bin/sh","sh")` → root.

## Credentials / secrets

| Item | Value |
|------|-------|
| hannah (secret in disk image) | `G'2'ZkcHsulI*vE+D,` |
| user.txt | `dl{user_eedfcf739a076a72412c89a1354a4119}` |

## Takeaways

- A `?page=` param is a strong hint to test for LFI, but the vulnerable parameter may be hidden — fuzz for it ([[parameter-fuzzing]]).
- FTP/vsftpd logs are a classic [[log-poisoning]] target when combined with LFI.
- `debugfs` (GTFOBins) turns a `sudo` entry into both file read and shell escape ([[sudo-abuse]]).
- `cap_setuid` on a Python interpreter is instant root ([[linux-capabilities]]).
