---
type: technique
tags: [ejpt:host-net-pentest]
tools: [metasploit]
cves: []
related: ["[[pivoting]]", "[[port-forwarding]]", "[[reverse-shells]]"]
---

# Metasploit Pivoting

Using Metasploit's routing engine to traverse multiple hops automatically.

## Workflow (one hop)

1. Catch a shell with `exploit/multi/handler`.
2. Upgrade it: `post/multi/manage/shell_to_meterpreter`.
   - **Gotcha:** on a *pivoted* shell the connection reads "Local Pipe", so the module can't auto-detect `LHOST`. Set `LHOST` manually to an IP the target can reach back to (e.g. the gateway on its own subnet).
3. Route the new subnet: `route add <net> <mask> <session>`.
   - Or automate: `post/multi/manage/autoroute`.
4. Scan through the pivot: `auxiliary/scanner/portscan/tcp`.
5. Forward a service: `portfwd add -l <local> -p <remote> -r <rhost>`.

## Why it chains automatically

`route add 30.30.30.0 255.255.255.0 4` says *"30.30.30.0/24 is behind session 4"*. Metasploit already knows session 4's host lives in `20.20.20.0/24` (routed via session 2), so it chains the path automatically:

```
you → session 2 (inclusion) → session 4 (trust) → 30.30.30.3
```

No manual per-hop port forwards needed — just one `route add` per newly-compromised host.

## Seen in

[[littlepivoting]] (multi-hop: `shell_to_meterpreter` → `route add` → chained scans), [[dark]] (single hop: `post/multi/gather/ping_sweep` on `20.20.20.0/24` → `auxiliary/scanner/portscan/tcp` → two `portfwd` relays)
