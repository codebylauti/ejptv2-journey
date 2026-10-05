---
type: tool
category: scanner
related: ["[[smb-enumeration]]"]
---

# Enum4linux

SMB/CIFS enumeration tool to list shares and users.

## Command

```sh
enum4linux TARGET
enum4linux TARGET | grep 'Local User'    # SID-walk output: S-1-22-1-<uid> Unix User\<name>
```

- The SID walk (`S-1-22-1-*` are local UIDs) can see accounts the RPC `--users` path misses — cross-check with [[nxc]] ([[smb-enumeration]]).

## Seen in

[[basic-pentesting]] (extracted users `jan`, `kay`), [[chmod-4755]] (SID walk found `rabol` where `nxc --users` only reported `smbuser`)
