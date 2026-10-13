---
type: technique
tags: [ejpt:host-net-pentest]
tools: [knock]
cves: []
related: ["[[ssh-bruteforce]]", "[[information-gathering]]", "[[directory-fuzzing]]"]
---

# Port Knocking

A firewall trick: a **sequence of connection attempts to closed ports** that, when it matches the expected order, tells the firewall to open a *hidden* port — one that never appeared in any scan.

## Why it defeats a naive scan

`nmap -p- --open` reports the truth *at scan time*: before the correct sequence arrives, the hidden port is simply **not open** — it looks filtered/closed like every other closed port. So an "empty" or near-empty full-scan result is not proof that the surface is exhausted; it may only mean nobody has knocked yet. The scan isn't wrong — it's incomplete *by design of the box*.

## Workflow

1. **Find the sequence** — it lives in web content: a tiny text file with three numbers, a note, a riddle. Read *every* small file fuzzing returns ([[directory-fuzzing]]).
2. **Knock**:

   ```sh
   knock <ip> <p1> <p2> <p3>
   ```

3. **Re-scan** — the identical `-p-` run now shows the newly exposed service (SSH in the canonical case).
4. **Attack what appeared** — the service needs no special treatment once open: brute-force or log in as usual ([[ssh-bruteforce]]).

## Why it matters

- **Stealth with a twist:** the port isn't firewalled forever, it's *conditional*. The condition (the sequence) is a secret sitting in readable content — so the "hidden" surface still leaks through enumeration ([[information-gathering]]).
- **Riddles can gate ports, not just credentials.** A hint that says "call before entering" alongside a name like `toctoc` (knock-knock) is simultaneously a username hint and a protocol hint: one file, two doors ([[ssh-bruteforce]]).
- **The knock only opens the port** — often just for your source IP or a time window. It authenticates nothing; you still need valid credentials for whatever appeared.

## Seen in

[[los40ladrones]] — `qdefense.txt` held the riddle (*"Recuerda llama antes de entrar…"*) plus the sequence `7000 8000 9000`; `knock 172.17.0.2 7000 8000 9000` flipped 22 from closed to open on the re-scan.
