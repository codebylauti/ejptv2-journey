---
type: tool
category: scanner
related: [[information-gathering]]
---

# Nmap

Network mapper for host discovery, port scanning, and service/version detection.

## Common flags

```sh
nmap -sV -sC -p- TARGET      # version + default scripts, all ports
nmap -sS -sV TARGET          # SYN scan + version
nmap -sn 10.10.10.0/24       # host discovery / ping sweep (who's alive)
nmap -Pn -n -vv -p- TARGET   # no ping, no DNS, verbose, all ports
```

- `-sV` service/version detection — critical for mapping banners to CVEs (e.g. `vsftpd 2.3.4`).
- `-p-` scans all 65535 ports. The *default* scan only covers the top ~1000, so uncommon services (e.g. the Node.js Inspector on 9229 in [[autoescuela]]) are invisible without it.
- Services bound to `127.0.0.1` (loopback) never show up in *any* external scan — they're only discoverable from a foothold inside the host.
- `--script` (NSE) isn't only for scanning — a custom `.nse` running `os.execute` can double as a `sudo` escape to drop a shell ([[anonymous-pingu]]).

## Seen in

Nearly every machine in this vault ([[breakmyssh]], [[ignite]], [[adopting]], [[autoescuela]], …).
