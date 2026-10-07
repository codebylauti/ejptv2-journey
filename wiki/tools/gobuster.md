---
type: tool
category: scanner
related: ["[[directory-fuzzing]]"]
---

# Gobuster

Directory/file brute-forcer for web applications.

## Command

```sh
gobuster dir -u http://TARGET -w /usr/share/wordlists/dirb/common.txt -x php,html,conf,sh,txt
```

- `dir` mode enumerates paths; `-x` appends extensions; `--exclude-length` filters noise.
- **Through a SOCKS tunnel:** add `--proxy socks5://127.0.0.1:1080` (gobuster speaks SOCKS natively — no [[proxychains]] needed).
- **With a credential:** pass `-H "Authorization: Basic $(echo -n 'user:pass' | base64)"` and cut the noise with `--xl <length>` — the authenticated response usually has its own distinct size ([[rutas]]).

## Vhost mode

```sh
gobuster vhost -u http://TARGET/ -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt --append-domain --xs 303
```

- `vhost` brute-forces `Host:` headers instead of paths ([[virtual-hosting]]).
- `--append-domain` appends the target's base domain to every wordlist entry.
- `--xs 303` drops the default vhost's redirect so only real `200` vhosts surface.

## Seen in

[[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[los-3-hackers]], [[adopting]], [[baluhome]], [[simple-ctf]], [[ignite]], [[tproot]], [[wargames]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[walkingcms]], [[anonymous-pingu]], [[pipepwned]], [[trailpack]], [[bruteshock]], [[littlepivoting]], [[madeyes-castle]], [[internal]] (`vhost` mode → `backup.internal.dl`), [[cap]] (`capture` 302 → `/data/1` object-ID leak), [[dark]] (`info` + `process.php` + `server-status`), [[rutas]] (`index.php`/`index.html` on the default vhost, re-fuzzed against `trackedvuln.dl` with Basic auth), [[file]] (`uploads/` + `file_upload.php`, the form page whose `action=` is the real endpoint), [[secretjenkins]] (DirBuster medium + `-x php,html,txt` → the Jenkins endpoint map: `login`, `builds`, and the 403 admin fence)
