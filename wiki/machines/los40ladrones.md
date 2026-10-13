---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, knock, hydra, ssh]
techniques: [information-gathering, directory-fuzzing, port-knocking, ssh-bruteforce, sudo-abuse]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: ["[[acme]]", "[[trust]]", "[[breakmyssh]]"]
---

# Los 40 Ladrones

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/los40ladrones.md)

A default Apache page and a single 111-byte text file: the file is a riddle that names both a **username** (`toctoc` — the Spanish "knock knock") and a **port-knocking sequence** (`7000 8000 9000`), and knocking on those ports is what makes SSH exist at all. Root then comes from the most generous `sudo -l` on record — a NOPASSWD **privileged copy of bash**.

## Path

1. **Recon** — `ping` + `nmap -p- --open -sS --min-rate 5000` → only **80** open, Apache 2.4.58 Ubuntu default page ([[information-gathering]], [[nmap]]).
2. **Dir fuzzing** — gobuster (DirBuster-medium, `-x php,html,txt`) → `index.html` (200, 10792), `qdefense.txt` (200, **111**), `server-status` (403) ([[directory-fuzzing]], [[gobuster]]).
3. **Read the 111 bytes** — `curl http://172.17.0.2/qdefense.txt`:

   ```
   Recuerda llama antes de entrar , no seas como toctoc el maleducado
   7000 8000 9000
   busca y llama +54 2933574639
   ```

   One riddle, two payloads: *"llama antes de entrar"* ("call/knock before entering") + *toctoc* → **port knocking** with the sequence on line 2, and `toctoc` as the candidate username ([[port-knocking]]).
4. **Knock** — `knock 172.17.0.2 7000 8000 9000`, then re-run the identical full scan → **22/tcp now open** next to 80 ([[knock]]).
5. **SSH brute** — the username came from the riddle, so only the password axis is unknown:

   ```sh
   hydra -l toctoc -P /usr/share/wordlists/rockyou.txt ssh://172.17.0.2 -F -t 64 -vV
   # → [22][ssh] host: 172.17.0.2   login: toctoc   password: kittycat
   ```

   Then `ssh toctoc@172.17.0.2` ([[ssh-bruteforce]], [[hydra]]).
6. **`sudo -l`** — two NOPASSWD entries:

   ```
   (ALL : NOPASSWD) /opt/bash
   (ALL : NOPASSWD) /ahora/noesta/function
   ```

   The second is a joke: *"ahora no está"* means *"not here right now"* — a decoy path the writeup never tests. The first is the real door ([[sudo-abuse]]).
7. **Root** — `sudo -u root /opt/bash` → `whoami` → `root`. `/opt/bash` is bash itself sitting at a custom path: a **pinned shell needs no payload** — running it *is* the exploit ([[gtfobins]]).

## Credentials / secrets

| Secret | Where it came from |
|--------|--------------------|
| `toctoc:kittycat` | username read out of the `qdefense.txt` riddle, password from rockyou |
| root shell | NOPASSWD `/opt/bash` — privileged bash copy, no payload required |

## Takeaways

- **A clean full-port scan is a claim, not a proof.** `-p- --open` showed exactly one port, and it was telling the truth — the other port was *conditional*. When the box hands you a tiny text file, re-read it before concluding the surface is exhausted ([[port-knocking]]).
- **Riddles can carry two payloads at once.** The same 111 bytes yielded the username *and* the knock sequence: a hint about "knocking" and a name that *is* a knock are the same clue seen from two angles. Read nouns as usernames and sounds as protocols ([[ssh-bruteforce]]).
- **A decoy sudo entry is still information.** `/ahora/noesta/function` was never run, but a path spelled "not here now" tells you the author writes jokes into `sudo -l` output — so weight the *other* entry higher, and don't let humor bury the payload. Entries cost one `sudo -l` to see and one command to disprove.
- **`/opt/bash` = the pinned-shell rule.** Same class as [[elevator]]'s `(vilma) NOPASSWD: /usr/bin/ash`: when the allowed binary *is* a shell, there is nothing to look up — the command is the payload. A bash copy under `/opt` is just a shell wearing a custom path, and `sudo -u root` supplies the privilege.

## Gaps in the writeup

- **The decoy was never tested.** Does `/ahora/noesta/function` exist? Error, joke, or a second usable path? The writeup picked `/opt/bash` on sight and never looked back.
- **`/opt/bash` itself was never inspected** — no `ls -l`, no `file`, no read of its contents. "It's bash" is inferred from the one `whoami`, not shown.
- **The phone number is unexplained.** `busca y llama +54 2933574639` ("search and call") was never dialed, searched, or otherwise pursued — flavor text, or a dropped second stage?
- **The knock mechanism was never confirmed from the inside.** Root was reached, but no `knockd` config or firewall rule was read to show *why* 7000-8000-9000 exposes 22.
- **No flags on record** — the transcript ends at `whoami` → `root`, with no flag path shown. `index.html` and `server-status` (403) were also never fetched.
