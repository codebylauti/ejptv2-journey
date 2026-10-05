---
type: tool
category: scanner
related: [[directory-fuzzing]]
---

# Gobuster

Directory/file brute-forcer for web applications.

## Command

```sh
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt
```

- `dir` mode enumerates paths; `-x` appends extensions; `--exclude-length` filters noise.
- **Through a SOCKS tunnel:** add `--proxy socks5://127.0.0.1:1080` (gobuster speaks SOCKS natively — no [[proxychains]] needed).

## Vhost mode

```sh
gobuster vhost -u http://TARGET/ -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain --xs 303
```

- `vhost` brute-forces `Host:` headers instead of paths ([[virtual-hosting]]).
- `--append-domain` appends the target's base domain to every wordlist entry.
- `--xs 303` drops the default vhost's redirect so only real `200` vhosts surface.

## Seen in

[[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[adopting]], [[baluhome]], [[simple-ctf]], [[ignite]], [[tproot]], [[wargames]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[walkingcms]], [[anonymous-pingu]], [[pipepwned]], [[trailpack]], [[bruteshock]], [[littlepivoting]], [[madeyes-castle]], [[internal]] (`vhost` mode → `backup.internal.dl`), [[cap]] (`capture` 302 → `/data/1` object-ID leak), [[dark]] (`info` + `process.php` + `server-status`)
