---
type: technique
tags: [ejpt:host-net-pentest]
tools: [metasploit, ssh, chisel, socat]
cves: []
related: [[pivoting]], [[metasploit-pivoting]]
---

# Port Forwarding / Tunneling

Making a port on one machine reachable from another by relaying traffic, when no direct route exists.

## Static vs dynamic forwarding

| | Specifies | Nature |
|---|---|---|
| **Static** (`ssh -L`/`-R`, `portfwd`) | our port **+** target host **+** target port | fixed pipe to ONE host:port |
| **Dynamic** (`ssh -D`, chisel SOCKS) | only our port | SOCKS proxy — target chosen per-request |

## SSH flags ([[ssh]])

| Flag | Listener (port opens here) | Egress (data emerges here) |
|------|---------------------------|---------------------------|
| `-L 8000:host:port` | our machine `:8000` | the SSH server |
| `-R 8000:host:port` | the SSH server `:8000` | our machine |
| `-D 1080` | our machine `:1080` (SOCKS) | the SSH server |

Key insight: through a `-D` tunnel, **`127.0.0.1` is resolved from the SSH server's perspective** — so `http://127.0.0.1:8000` typed on your box reaches the *server's* loopback, not your own.

## Metasploit

`portfwd add -l <local> -p <remote> -r <rhost>` is the static `-L` equivalent — see [[metasploit-pivoting]].

## Chisel

Reverse SOCKS/port forwarding over HTTP/WebSocket — see [[chisel]].

## Socat relays

`socat tcp-l:PORT,fork,reuseaddr tcp:NEXT-HOP:PORT` is the manual "static pipe" — chain one per hop to carry a listener (or a reverse shell path) back through the network. See [[socat]].

## Debugging a tunnel chain

- **"Connection refused"** = host reachable, but the port is closed (nothing listening).
- **"Connection timed out"** = host unreachable / firewall silently dropping.
- Isolate each hop with `curl --socks5-hostname` before blaming the browser/Burp chain.

## Seen in

[[littlepivoting]] — Metasploit `portfwd` in the first run; chisel reverse SOCKS + [[socat]] relays in the manual re-run. [[dark]] — two `portfwd` relays from one pivot (`8080→80`, `2002→22`), one per service. SSH `-D`/`-L`/`-R` discussed but not yet used on a box.
