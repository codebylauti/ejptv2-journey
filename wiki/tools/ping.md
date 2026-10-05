---
type: tool
category: networking
related: ["[[information-gathering]]"]
---

# Ping

ICMP reachability check — the first command of every engagement.

## Command

```sh
ping -c 2 TARGET
```

- Confirms the host is up and shows RTT — `2 packets transmitted, 2 received, 0% packet loss` before any port scan.
- The **TTL is an OS hint before nmap runs**: ~64 Linux, ~128 Windows. On [[winfake]] a `PS C:\>` prompt claimed Windows, but `ttl=64` told the truth ([[information-gathering]]).
- No reply ≠ host down: ICMP can be filtered — `nmap -Pn` skips the ping stage entirely when that happens.
- On DockerLabs everything shares a bridge network, so `ttl=64` and sub-millisecond RTT are the expected baseline.

## Seen in

Every box in this vault (37 writeups) — the opening step of [[information-gathering]].
