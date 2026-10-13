---
type: tool
category: networking
related: ["[[port-knocking]]"]
---

# knock

Client that sends a **port-knock sequence**: touches a list of ports on a host, one connection attempt per port, in the order given.

## Command

```sh
knock <host> <port> <port> ...        # e.g. knock 172.17.0.2 7000 8000 9000
```

- Each argument is hit **in order** — the firewall watches the sequence, not the payload; nothing needs to be *listening* on those ports.
- **Find the sequence first:** it usually sits in a web file, note, or riddle right next to the hint that told you to knock ([[port-knocking]]).
- Server-side counterparts exist (`knockd` + `/etc/knockd.conf` on the target, iptables `recent` modules). Once you have root, reading the config confirms the sequence and the port it exposes.

## Seen in

[[los40ladrones]] — `knock 172.17.0.2 7000 8000 9000` opened SSH after the sequence was read from `qdefense.txt`.
