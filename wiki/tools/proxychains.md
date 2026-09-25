---
type: tool
category: proxy
related: [[pivoting]], [[chisel]], [[port-forwarding]]
---

# Proxychains

Wraps any command so its traffic routes through a SOCKS proxy (an SSH `-D` tunnel, or a chisel reverse SOCKS).

## Config

`/etc/proxychains4.conf` — set the active line to:

```
socks5 127.0.0.1 1080
```

(comment out any other proxy lines so only this one is used).

## Usage

```sh
proxychains nmap -sT -Pn TARGET     # -sT (TCP connect) — SYN/ICMP don't proxy
proxychains curl http://TARGET
```

- `-sT` because SOCKS carries TCP streams, not raw packets.
- `-Pn` because ICMP ping doesn't tunnel through SOCKS.

> Not yet exercised on a completed box — see [[pivoting]].
