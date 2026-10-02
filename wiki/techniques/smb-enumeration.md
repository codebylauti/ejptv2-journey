---
type: technique
tags: [ejpt:assessment, ejpt:auditing, ejpt:host-net-pentest]
tools: [enum4linux, nxc, smbmap, smbclient]
cves: []
related: [[ssh-bruteforce]], [[web-shell-upload]], [[nxc]], [[smbmap]], [[smbclient]]
---

# SMB Enumeration

Enumerating SMB shares, users, and login validity — a rich source of account names for later brute-force, and sometimes a direct path to the webroot.

## Workflow

1. **Users (null session)** — does an unauthenticated session reveal accounts?
   ```sh
   nxc smb TARGET --users          # NetExec; falls back to SAMRPC if the DC path is refused
   enum4linux -U TARGET            # classic alternative — walks SAM RPC SIDs
   ```
   **Run both.** On [[chmod-4755]] they disagreed: `nxc --users` reported only `smbuser`, while enum4linux's SID walk also found `rabol` (UID 1001) — the account the entire hint chain pointed at.
2. **Shares (null session)** — what's readable without credentials?
   ```sh
   smbmap -H TARGET
   smbclient //TARGET/share -N
   ```
3. **Brute-force logins** with the user list — see the hydra gotcha below.
   ```sh
   nxc smb TARGET -u users.txt -p rockyou.txt --ignore-pw-decoding
   ```
4. **Re-check shares authenticated** — permissions always change with a valid session:
   ```sh
   smbmap -H TARGET -u bob -p star   # NO ACCESS → READ, WRITE unlocks the target share
   smbclient //TARGET/html -U bob --password=star
   put payload.php                    # if the share maps to the webroot → [[web-shell-upload]]
   ```

## What to extract

- Valid usernames (e.g. `jan`, `kay` in [[basic-pentesting]]; `james`, `bob` via null session in [[domain]]).
- Share names **and permission deltas between null vs authenticated sessions** — `html NO ACCESS → READ, WRITE` is the entry point ([[domain]]); `share_secret_only NO ACCESS → READ ONLY` unlocked the hint on [[chmod-4755]].
- Share **names as hints** — `share_secret_only` was literally the next account's password. Read names, comments, and filenames as content, not labels ([[chmod-4755]]).
- Files inside readable shares — including **hidden dotfiles** (`.notes.txt`) that hold hints for later steps ([[madeyes-castle]]).
- The NSE `smb2-security-mode` line: *signing enabled but not required* = SMB-relay precondition — flag it even when the box never demands a relay ([[information-gathering]]).

## Hydra `smb2://` false positives

`hydra -L users.txt -P rockyou.txt smb2://TARGET` can report **bogus hits** — on [[domain]] it "found" `bob:123456`, `james:123456`, `12345`… while printing `[WARNING] might accept any credential`. `nxc` on the same lists returned the one real password (`bob:star`).

- **Rule:** never pivot on a hydra SMB hit alone — confirm with an authenticated command (`nxc smb TARGET -u <user> -p <pass> --shares`) before using the credential.
- Same gotcha applies to other connectionless modules; the authenticated re-check is the ground truth ([[hydra]], [[nxc]]).

## Seen in

[[basic-pentesting]], [[madeyes-castle]] (anon `sambashare` → `spellnames.txt` + `.notes.txt`), [[domain]] (null-session users → hydra false positives → `nxc` spray → writable `html` share → SUID `nano`), [[chmod-4755]] (tool divergence: `nxc --users` under-reported, `enum4linux` SID walk found `rabol`; authenticated `smbmap` delta → `smbclient` note.txt → share-name password → SSH)
