---
type: tool
category: scanner
related: ["[[smb-enumeration]]", "[[smbclient]]"]
---

# Smbmap

Samba share enumerator: lists shares and permissions as a null session or authenticated, and can pull/push files when the session allows it.

## Command

```sh
smbmap -H TARGET                      # null session: shares + permissions
smbmap -H TARGET -p 445               # explicit port
smbmap -H TARGET -u user -p pass      # authenticated: NO ACCESS → READ ONLY / READ, WRITE
```

- The signal is the **permission delta** between null and authenticated runs — `NO ACCESS → READ, WRITE` is the entry point of the box ([[smb-enumeration]]).
- It answers "what's accessible?"; pair it with `nxc smb --users` / `enum4linux` for "who exists?" before spraying.
- Share *names* are content too: `share_secret_only` turned out to be the next password on [[chmod-4755]].

## Seen in

[[domain]] (`html` NO ACCESS → READ, WRITE after the spray), [[chmod-4755]] (`share_secret_only` + `print$` unlock with `smbuser`), [[madeyes-castle]] (anon `sambashare` listing)
