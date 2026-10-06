---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, curl, ssh]
techniques: [information-gathering, source-code-disclosure, encoded-credentials, hardcoded-credentials]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[winfake]]", "[[vacaciones]]"]
---

# Extraviado

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/extraviado.md)

Easy box — *extraviado* = **lost/misplaced** — where every secret is **encoded, not encrypted**: a base64 `user : pass` pair on the last line of the default Apache page, base64 password files found with `find`, and a root password that is the answer to a riddle. Zero exploits, zero brute-force — pure read-and-decode discipline.

## Path

1. **Recon** — `ping -c 2` (`ttl=64`, Linux). `nmap -p- --open -sS --min-rate 5000 -n -Pn` → `22/tcp` OpenSSH 9.6p1 Ubuntu + `80/tcp` Apache 2.4.58 serving the **default Ubuntu page** ("It works") ([[information-gathering]]).
2. **Web enum** — the page renders as empty, but `curl -s http://172.17.0.2 | tail -1` shows a long dotted line ending in `ZGFuaWVsYQ== : Zm9jYXJvamE=` — a `user : pass` pair in **base64** (`echo … | base64 -d` → `daniela` / `focaroja`). Nothing to fuzz: the secret was in the page body itself ([[source-code-disclosure]], [[encoded-credentials]]).
3. **SSH** — `ssh daniela@172.17.0.2` logs straight in with the decoded pair — no hydra, no rockyou ([[hardcoded-credentials]]).
4. **Lateral: daniela → diego** — `cat Desktop/nota`: *"no recuerdo donde guarde la password de root"* — the box's theme, stated in-world. `find / -name *diego*` → `~/.secreto/passdiego` holding `YmFsbGVuYW5lZ3Jh` → base64 → **`ballenanegra`** → `su diego`.
5. **Lateral: diego → root (the decoy)** — `find / -regex .*pass.* | grep .passroot` → `~/.passroot/.pass` = `YWNhdGFtcG9jb2VzdGE=` → base64 → `acatampocoesta`, which reads as *"aca tampoco esta"* — **"it's not here either"**. The file named like the root password is a joke.
6. **Root (the riddle)** — `cat .local/share/.-` is headed *"password de root"* followed by a Spanish riddle: faithful friend of children in dream stories, not a king, lives in the cold, colored like sky and sea → a **polar bear in a blue coat** → **`osopolar`** → `su root` → `whoami` = `root` ([[acrostic-decoding]]'s cousin: the password is a hidden *answer*, and the file hands you the derivation.

## Credentials / secrets

| Item | Value | Where |
|------|-------|-------|
| daniela (SSH) | `focaroja` | base64 pair, last line of `/` |
| diego | `ballenanegra` | `~/.secreto/passdiego` (base64) |
| root (decoy) | `acatampocoesta` | `~/.passroot/.pass` (base64) — *"it's not here either"* |
| root | `osopolar` | riddle in `~/.local/share/.-` |

## Takeaways

- **A default page is not an empty page.** `http-title: Apache2 Ubuntu Default Page` invites you to leave — but `curl -s … | tail -1` reads the response byte-for-byte, and the payload was on the very last line ([[source-code-disclosure]]).
- **Encoding is a formatting, not a defense.** base64 announces itself (4-char groups, `=` padding, printable-but-nonsense). Decode before you crack; a "hash-looking" string may just be an encoding ([[encoded-credentials]], [[hash-cracking]]).
- **Known credentials skip the brute-force entirely.** One decoded pair → direct SSH login. Ask *do I already have the password?* before reaching for rockyou ([[hardcoded-credentials]]).
- **`find` is the credential enumerator once you're on-box.** Names are the signal: `*diego*` finds the user's secret, `.*pass.*` finds the next one — then decode what they hold.
- **A file that looks like the answer can be the joke.** `.passroot/.pass` decodes to *"it's not here either"*. Read what the secret **says**, not what its filename promises — the same discipline as checking whether a cracked hash was ever a hash ([[dance-samba]]).
- **Riddle passwords are derived passwords.** The box gives you the derivation function (the poem) and you supply the answer (`osopolar`) — same pattern as the acrostic in [[winfake]], one alphabet over.

## Gaps in the writeup

- **The decoy was never *shown* to fail.** `acatampocoesta` is decoded and then dropped without an `su root` attempt on record — the "pun/decy" reading (*aca tampoco esta*) is inferred, not demonstrated. A re-run should try it explicitly before dismissing it.
- **The winning password is asserted, not observed.** The writeup concludes the password *"must be something like `osopolar`"*, then cuts to `su root` → `root`; the value actually typed is never displayed.
- **`find / -name *diego*` relies on an unquoted glob.** The shell expands `*diego*` against the *local* working directory before `find` ever runs — it worked here only because nothing matched locally. The reproducible form is `find / -name '*diego*'`.
