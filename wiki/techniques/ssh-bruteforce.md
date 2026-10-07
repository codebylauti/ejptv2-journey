---
type: technique
tags: [ejpt:host-net-pentest]
tools: [hydra]
cves: []
related: ["[[sudo-abuse]]"]
---

# SSH Brute Force

Dictionary attack against SSH over a known username **or** a known password.

## Command

```sh
hydra -l <user> -P /usr/share/wordlists/rockyou.txt ssh://TARGET -t 4
# inverted: you hold the password, not the user
hydra -L /usr/share/seclists/Usernames/xato-net-10-million-usernames.txt -p <token> ssh://TARGET -t 4
```

- `-l` single user, `-L` user list; `-P` password list, `-p` single password.
- `-t 4` limits parallel tasks to avoid SSH throttling.

## Common targets

- Root with a weak password ([[breakmyssh]] → `estrella`).
- A username leaked from web source or SMB, paired with `rockyou.txt`.
- A username found on the box paired with a **password file found next to it** — always grep the filesystem for wordlists before reaching for rockyou (`/opt/.vault_pass.txt` cracked `vault` on the first hit in [[internal]]).
- A **lone password with no username** — a gibberish token sitting alone in a web page flips the flags: fuzz usernames (`-L`) against the one secret you hold (`-p`), because the unknown axis is the user, not the password ([[library]] → `carlos:JIFGHDS87GYDFIGD` via xato's 10-million list).

## Seen in

[[breakmyssh]], [[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[basic-pentesting]], [[simple-ctf]], [[grooti]], [[winfake]], [[littlepivoting]] (`manchi:lovely`, `mario:chocolate`), [[internal]] (`vault:Yk8$pZ5@cN4!` via a leaked password file), [[dark]] (`toni:banana` — username straight out of LFI'd `/etc/passwd`), [[library]] (inverted axis — token from `index.php` as the password, usernames fuzzed)
