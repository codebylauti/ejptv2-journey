---
type: tool
category: networking
related: [[reverse-shells]], [[vsftpd-backdoor]]
---

# Netcat

Swiss-army network utility. In this vault it's primarily the reverse-shell **listener**, plus quick port checks and file transfer.

## Common usage

```sh
# Reverse-shell listener
nc -lvnp 443

# Port scan / banner grab
nc -zv TARGET 1-1000
nc TARGET 80

# File transfer
nc -lvnp 443 > out.bin    # receiver
nc TARGET 443 < in.bin    # sender
```

- `-l` listen · `-v` verbose · `-n` no DNS lookup · `-p` local port.
- Listening on a **port below 1024** needs root — hence `sudo nc -lvnp 433` on [[domain]]. Pick an unprivileged port to avoid it.

## Seen in

Listener for reverse shells in [[hannah-coffee]], [[baluhome]], [[ignite]], [[balulero]], [[autoescuela]], [[grooti]], [[anonymous-pingu]], [[trailpack]], [[bruteshock]], [[domain]] (privileged port `433`, run with `sudo`); used to trigger [[vsftpd-backdoor]] in [[first-hacking]] and [[tproot]]; raw TCP client for the [[wargames]] WOPR text game.
