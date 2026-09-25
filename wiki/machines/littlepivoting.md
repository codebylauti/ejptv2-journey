---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 10.10.10.2
cves: []
tools: [nmap, gobuster, ffuf, hydra, curl, metasploit, gtfobins]
techniques: [information-gathering, directory-fuzzing, local-file-inclusion, ssh-bruteforce, su-brute-force, sudo-abuse, reverse-shells, web-shell-upload, pivoting, port-forwarding, metasploit-pivoting]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: [[metasploit-pivoting]], [[port-forwarding]], [[guided-pentest]]
---

# LittlePivoting

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/littlepivoting.md)

Intermediate **pivoting lab**: a 3-host chain across three subnets, reached one hop at a time.

```
Kali (10.10.10.1) ─ 10.10.10.0/24 ─ inclusion (10.10.10.2, 20.20.20.2)
                                   ─ 20.20.20.0/24 ─ trust (20.20.20.3, 30.30.30.2)
                                                    ─ 30.30.30.0/24 ─ upload (30.30.30.3)
```

Each host is **dual-homed** (two NICs) and bridges you to the next subnet. `auto_deploy.sh` creates three Docker bridge networks with Kali as the gateway on each.

## Path

1. **Recon** — `ip a` + `ip route` map the local interface (`10.10.10.1`); `nmap -sn` finds the entry host `10.10.10.2` ([[information-gathering]]).
2. **inclusion foothold** — `nmap` shows `22`/`80`; [[gobuster]] finds `shop/`; [[local-file-inclusion]] via `?archivo=` reads `/etc/passwd`; [[hydra]] [[ssh-bruteforce]]s `manchi:lovely`.
3. **inclusion privesc** — [[su-brute-force]] (`Linux-Su-Force.sh`) → `seller:qwerty`; `sudo -l` shows `NOPASSWD /usr/bin/php` → root ([[sudo-abuse]], [[gtfobins]]).
4. **Pivot to trust** — bash reverse shell + `shell_to_meterpreter`; `route add 20.20.20.0/24 2`; ping sweep + `portscan/tcp` find `20.20.20.3` (22/80); `portfwd` exposes the web app; [[gobuster]] finds `secret.php` → user `mario`; hydra `mario:chocolate`; `sudo -l` → `/usr/bin/vim` → root ([[metasploit-pivoting]], [[port-forwarding]]).
5. **Pivot to upload** — reverse shell + `shell_to_meterpreter` (set `LHOST` manually — pivot sessions read "Local Pipe"); `route add 30.30.30.0/24 4`; `portscan/tcp` finds `30.30.30.3:80`; `portfwd` + [[web-shell-upload]] of a PHP reverse shell → foothold on `30.30.30.3`; `sudo -l` → `NOPASSWD /usr/bin/env` → root.

## Credentials

| Host | User | Password |
|------|------|----------|
| inclusion | manchi | lovely |
| inclusion | seller | qwerty |
| trust | mario | chocolate |

## Takeaways

- Pivoting is **one hop at a time**: you can't see an inner subnet until you compromise the dual-homed host bridging it ([[pivoting]]).
- On the compromised host, read the network first (`ip a`, `ip route`, `hostname -I`) — that's how you discover the next subnet.
- Metasploit's `route`/`autoroute` chains hops automatically; `portfwd` relays a service ([[metasploit-pivoting]]).
- `shell_to_meterpreter` can't auto-detect `LHOST` on a pivoted ("Local Pipe") session — set it to an IP the target can reach back to.
- sudo `php`/`vim`/`env` are all GTFOBins one-liners for root ([[sudo-abuse]]).
