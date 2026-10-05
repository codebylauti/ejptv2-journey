---
type: tool
category: scanner
related: ["[[information-gathering]]", "[[pivoting]]"]
---

# Arp-scan

Layer-2 host discovery: sweeps the **directly connected** subnet with ARP requests. No route/gateway needed, so it works where ping/`nmap -sn` can't — and it sees hosts that ignore ICMP.

## Command

```sh
sudo arp-scan -I br-5b5a61d71b66 --localnet
Interface: br-5b5a61d71b66, type: EN10MB, MAC: de:86:d2:e5:35:66, IPv4: 10.10.10.1
10.10.10.2      9a:87:e3:58:11:9f       (Unknown: locally administered)
```

- `-I <iface>` picks the interface (find it with `ip a` / `ip link`).
- `--localnet` targets the subnet of that interface — no CIDR to type.
- Output pairs **IP ↔ MAC**, which also tells you which hosts are Docker/virtual (locally administered MACs).

## arp-scan vs nmap -sn

| | arp-scan | `nmap -sn` |
|---|---|---|
| Layer | ARP (L2) — same subnet only | ICMP/ARP via IP (needs a route) |
| Needs root | yes | usually |
| Beyond your subnet | no | yes (through a gateway/pivot) |

## Seen in

[[littlepivoting]] (manual re-run: mapped the `10.10.10.0/24` entry subnet from Kali's bridge interface)
