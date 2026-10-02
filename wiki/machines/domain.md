---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, nxc, netcat]
techniques: [information-gathering, smb-enumeration, web-shell-upload, suid-enumeration, writable-etc-passwd]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: [[basic-pentesting]], [[madeyes-castle]]
---

# Domain

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/domain.md)

Easy, SMB-focused box: null-session user enum → share brute-force (with a **hydra false-positive detour**) → writable web share → PHP shell → SUID `nano` blanking root's password.

## Path

1. **Recon** — `ping -c 2` (ttl=64) then `sudo nmap -p- --open -sS -sCV --min-rate 5000 -n -Pn` → `80/tcp` (Apache 2.4.52, title *¿QuÉ es Samba?*), `139/tcp` + `445/tcp` (Samba smbd 4). The NSE `smb2-security-mode` script flags **message signing enabled but not required** — a relay-attack surface worth noting even though it's unused here ([[information-gathering]]).
2. **Web enum** — port 80 is just a Samba explainer page; recognized as lab training content and skipped — the box's attack surface is SMB ([[directory-fuzzing]] negative result).
3. **SMB user enum (null session)** — `crackmapexec smb TARGET --users` fails with a DC-IP socket error, then falls back to the SAMRPC protocol and returns domain users **`james`** and **`bob`** ([[smb-enumeration]], [[nxc]]).
4. **Share enum** — `smbmap -H TARGET` as null session → `print$`, `html`, `IPC$` all **NO ACCESS** ([[smb-enumeration]]).
5. **Brute-force** — `hydra -L users.txt -P rockyou.txt smb2://TARGET` reports `bob:123456`, `james:123456`, `12345`… but they're **false positives** (`[WARNING] might accept any credential`). Switch to `nxc smb TARGET -u users.txt -p rockyou.txt --ignore-pw-decoding` → valid **`bob:star`** ([[hydra]] gotcha, [[nxc]]).
6. **Foothold (share abuse)** — `smbmap -H TARGET -u bob -p star` → `html` is **READ, WRITE** (web-accessible) → `smbclient //TARGET/html -U bob --password=star` → `put payload.php` → reverse shell → `www-data` ([[web-shell-upload]], [[reverse-shells]]). Listener: `sudo nc -lvnp 433` — `sudo` because the port is below 1024 ([[netcat]]).
7. **Privesc** — `find / -perm -4000 2>/dev/null` → `/usr/bin/nano` is SUID → `nano /etc/passwd` and blank root's field (`root:x:` → `root::`) → `su -` → **root** ([[suid-enumeration]], [[writable-etc-passwd]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| `bob` (SMB) | `star` (rockyou via nxc) |

## Takeaways

- **SMB null sessions answer two questions:** *who exists?* (`nxc smb --users`) and *what's accessible?* (`smbmap -H`) — users first, so you have a target list for the brute-force ([[smb-enumeration]]).
- **Verify every hydra `smb2://` hit.** This Samba accepted garbage credentials and hydra happily reported them; `nxc` found the single real password (`bob:star`). Confirm with an authenticated command before pivoting ([[hydra]], [[nxc]]).
- **A writable share can be the webroot.** The upload vector here wasn't an HTTP form — it was SMB write access to the site's `html` directory: no HTTP attack needed to get RCE ([[web-shell-upload]]).
- **Read the signing flag.** `Message signing enabled but not required` is the classic precondition for an SMB relay attack — flag it even when the box doesn't require it ([[smb-enumeration]]).
- **SUID editors are instant privesc:** any editor that can *write* `/etc/passwd` as root makes `find / -perm -4000` output your whole exploit ([[suid-enumeration]], [[writable-etc-passwd]]).
