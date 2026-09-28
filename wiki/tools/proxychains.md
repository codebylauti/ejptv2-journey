---
type: tool
category: proxy
related: [[pivoting]], [[chisel]], [[port-forwarding]], [[socat]]
---

# Proxychains

Wraps any command so its traffic routes through a SOCKS proxy (an SSH `-D` tunnel, or a chisel reverse SOCKS).

## Config

`/etc/proxychains4.conf` — set the active line to the live SOCKS port:

```
socks5 127.0.0.1 1080
```

With a multi-hop pivot, keep one line per tunnel (`1081` inner hop, `1080` outer) in the same file so a single config covers both subnets. Comment out unused lines when you only need one path.

## Usage

```sh
proxychains nmap -sT -Pn -n TARGET     # -sT (TCP connect) — SYN/ICMP don't proxy
proxychains curl http://TARGET/path
proxychains hydra -l user -P rockyou.txt TARGET ssh
proxychains ssh user@TARGET
```

- `-sT` because SOCKS carries TCP streams, not raw packets.
- `-Pn` because ICMP ping doesn't tunnel through SOCKS.
- Tools that speak HTTP natively may take a proxy flag instead: `gobuster --proxy socks5://127.0.0.1:1080`.

## Seen in

[[littlepivoting]] (manual re-run: nmap/gobuster/hydra/ssh all through chisel SOCKS — replaced the per-service `portfwd` relays of the Metasploit run).
