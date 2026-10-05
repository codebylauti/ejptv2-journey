---
type: technique
tags: [ejpt:host-net-pentest]
tools: [metasploit, nmap, ssh, chisel, proxychains, socat]
cves: []
related: [[port-forwarding]], [[metasploit-pivoting]], [[information-gathering]]
---

# Pivoting

Moving laterally through a network by using a compromised host as a stepping stone to reach otherwise-unreachable subnets.

## Core concept: one hop at a time

From your attacker box you can only see *your own* subnet. Inner subnets (behind a dual-homed host) are invisible until you compromise that host and read its interfaces.

```
[you] ─ 10.10.10.0/24 ─ [inclusion] ─ 20.20.20.0/24 ─ [trust] ─ 30.30.30.0/24 ─ [upload]
```

Each hop repeats the loop: **enumerate → discover the next subnet → exploit → route traffic through it → repeat.**

## The dual-homed host

A machine with two NICs on two *different* subnets, acting as a bridge/router between them. That machine is the pivot point. Note: `lo` (loopback) does **not** count as a "home" — dual-homing means two *real* interfaces on two networks.

## Discover the next subnet (local enumeration)

On the compromised host, **read the network before you scan it**:

- `ip a` / `hostname -I` — list interfaces and IPs; a second NIC reveals the next subnet.
- `ip route` / `cat /proc/net/route` — which networks are directly connected.
- `cat /etc/hosts` — may hardcode other internal hostnames/IPs.

> In minimal Docker containers `ip`/`ifconfig` are often missing — fall back to `hostname -I`, `cat /proc/net/route`, `cat /proc/net/fib_trie`, `cat /proc/net/arp`.

## Then scan the new subnet

- **Host discovery (ping sweep):** `nmap -sn <net>` or `for i in $(seq 254); do ping -c1 -W1 <net>.$i & done | grep from`.
- Through a tunnel, ICMP doesn't proxy — use **TCP connect scans** (`-sT -Pn`).

## Reaching the next subnet

- **Metasploit** — `route add <net> <mask> <session>` (auto-chains) + `portfwd` ([[metasploit-pivoting]]).
- **SSH** — `-D` dynamic SOCKS + [[proxychains]], or `-L`/`-R` static forwards ([[port-forwarding]], [[ssh]]).
- **Chisel** — reverse SOCKS over HTTP + [[proxychains]] ([[chisel]]) — no root needed, works from any login that can run a binary.
- **Relays back home** — when a hop can't reach you, chain [[socat]] listeners (`tcp-l:PORT,fork,reuseaddr tcp:<neighbor>:PORT`) so reverse shells/callbacks can walk out hop by hop.

## Two gotchas

- **Getting tools in** — the pivot host may have no route to your HTTP server *and* no `curl`/`nc` helper; serve binaries yourself (`python3 -m http.server`) and `wget` them, or copy them hop to hop from the previous machine.
- **Stacking hops** — each chisel client can register its own SOCKS port (`R:1080:socks`, `R:1081:socks`); list both in `proxychains4.conf` so one config reaches either subnet.

## Seen in

[[littlepivoting]] — twice: Metasploit `route`/`portfwd`, then a fully manual chisel + [[socat]] + [[proxychains]] re-run. [[dark]] — one hop, Metasploit only (`ping_sweep` → `portscan/tcp` → `portfwd`).
