---
type: tool
category: scanner
related: ["[[linux-capabilities]]", "[[suid-enumeration]]"]
---

# Getcap

Prints POSIX file capabilities — Linux's alternative to the SUID bit for granting specific privileged operations to a binary.

## Command

```sh
getcap -r / 2>/dev/null        # recursive sweep from a foothold
```

- The `2>/dev/null` silences permission-denied noise across the filesystem.
- Watch for `cap_setuid` (→ spawn root shells, the [[gtfobins]] of capabilities), `cap_dac_override` (→ read anything), `cap_net_bind_service` (→ bind ports < 1024).
- **Sweep it right after `find / -perm -4000`** — the two privesc hunts are complementary: capabilities are the non-SUID half of the same question ([[suid-enumeration]], [[linux-capabilities]]).

## Seen in

[[hannah-coffee]], [[los-3-hackers]], [[cap]] (`/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip` → `os.setuid(0)`)
