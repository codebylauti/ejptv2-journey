---
type: tool
category: bruteforcer
related: ["[[smb-enumeration]]", "[[hydra]]"]
---

# nxc (NetExec)

`nxc` — NetExec, the maintained successor of **CrackMapExec** (`cme`). The SMB/AD swiss-army knife: enumerate, authenticate, execute. In this vault it's the reliable answer to SMB user enumeration and login spraying.

## Command

```sh
# Null-session user enumeration (falls back to SAMRPC if the DC-IP path is refused)
nxc smb TARGET --users

# Login spray / brute-force with a user list + password list
nxc smb TARGET -u users.txt -p /usr/share/wordlists/rockyou.txt --ignore-pw-decoding
```

- Success prints `[+] DOMAIN\user:password` — one line, one real hit.
- `--users` leaked `james`/`bob` on [[domain]] after `crackmapexec`'s DC-IP attempt errored out — the tool retries with another protocol.
- **Why not hydra?** the `smb2://` module false-positived five bogus passwords on the same box ([[hydra]]). Treat unauthenticated hydra SMB hits as unconfirmed until `nxc` (or a real login) repeats them.

## Seen in

- [[domain]] — null-session user enum (`james`, `bob`) and the rockyou spray that found `bob:star` after hydra's false positives.
- [[chmod-4755]] — sprayed `smbuser:fuckit`, then `fuckit:123456`; the second hit was **guest-mapped over SMB** (no SSH access) and `--users` *under-reported* the local users vs [[enum4linux]] — valid ≠ useful, and one enum tool is never enough.
- [[dance-samba]] — `--users` confirmed the FTP note's username (`macarena`); a single-user rockyou spray returned `macarena:donald`, then `--shares` flipped the home share to READ,WRITE.
