---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, curl, tshark, ssh]
techniques: [information-gathering, pcap-analysis, hardcoded-credentials, sudo-abuse]
tags: [ejpt:assessment, ejpt:host-net-pentest]
related: ["[[cap]]", "[[internal]]"]
---

# Analyst

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/analyst.md)

Blue-team flavored easy box: instead of exploiting a service, you **reconstruct an attack from a downloadable pcap** to answer a 9-question incident quiz — and the capture happens to contain the SSH password.

## Path

1. **Recon** — `ping -c 2` then `sudo nmap -sS -sC -sV -p- --open -Pn -n --min-rate 5000` → `22/tcp` (OpenSSH 10.0p2 Debian) and `80/tcp` (Gunicorn, title *El caso de Pinguinito — Lab Blue Team*) ([[information-gathering]]).
2. **Artifacts** — `curl http://IP/descargas/threat_intel_feed.json > hint.json` and `curl http://IP/descargas/incidente_pinguino.pcap > hint.pcap`. The threat-intel feed lists `198.51.100.23` (Vietnam) and `203.0.113.99` (Germany) — both RFC 5737 documentation IPs, lab-synthetic ([[curl]]).
3. **PCAP triage** — the web quiz asks 9 questions about the incident; every answer comes from `tshark` on the capture ([[pcap-analysis]]):
   - `tshark -r hint.pcap -Y 'http.request.method==POST'` → `198.51.100.23 → 10.10.2.15 POST /reviews/upload.php` → cross-referencing the feed attributes the attacker (Vietnam).
   - `-Y 'ip.src==198.51.100.23 && http.request' -T fields -e http.user_agent | sort -u` → `ReconBot/1.0`.
   - URI sweep shows the recon path (`/uploads/`, `/images/uploads/`, … → `/reviews/upload.php`).
   - `-q -z follow,tcp,ascii,<stream>` on the two upload streams: `shell.php` → **403**, `image.jpg.php` → **200** — the double extension slipped through.
   - Outbound SYN `10.10.2.15 → 198.51.100.23` (reverse shell, port **8080**); following that stream shows `cat /etc/passwd` and a password-reset line leaking `pinguinito:Tr0pic4l-Pingu_99!`.
4. **SSH** — `ssh pinguinito@172.17.0.2` with the captured password ([[hardcoded-credentials]]).
5. **Privesc** — `sudo -l` → `(ALL) NOPASSWD: ALL` → `sudo -u root /bin/bash -p` → **root** ([[sudo-abuse]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| `pinguinito` (SSH) | `Tr0pic4l-Pingu_99!` (from the pcap's password-reset message) |

## Takeaways

- **Not every box is exploited — some are *read*.** When the deliverable is an incident report, the pcap *is* the attack surface ([[pcap-analysis]]).
- **Correlate artifacts before digging:** the feed gave the suspect IPs, the pcap gave the traffic — `ip.src == <suspect>` is the filter that ties attribution together.
- `sort -u` on `-T fields` output and `uniq` on `tcp.stream` are the two "shrink the noise" moves; then `-z follow,tcp,ascii,<n>` reads the whole conversation ([[pcap-analysis]]).
- **Status codes narrate the attack:** 403 on `shell.php` vs 200 on `image.jpg.php` tells you the filter's rule without touching the server again.
- Credentials leak in *operational messages* too — grep streams for `contrasena|password|reset`, not just `USER`/`PASS` ([[hardcoded-credentials]]).
