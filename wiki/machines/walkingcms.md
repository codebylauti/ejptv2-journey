---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, ffuf, gobuster, wpscan, netcat, gtfobins]
techniques: [directory-fuzzing, wordpress-enumeration, reverse-shells, suid-enumeration]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[duque]]", "[[simple-ctf]]"]
---

# WalkingCMS

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/walkingcms.md)

Easy box: discover a hidden WordPress → enumerate a user + brute-force `wp-login` with wpscan → edit a theme file for a PHP reverse shell → `env` SUID to root.

## Path

1. **Recon** — `nmap -p- -sS -sV -sC` shows only `80/tcp` (an Apache page titled "Apache2 Debian Default Page"). The box name hints a CMS is hidden behind it.
2. **Web enum** — [[ffuf]] on the root finds `wordpress/`; [[gobuster]] inside it confirms a standard WP layout (`wp-admin`, `wp-login.php`, `wp-config.php`, `xmlrpc.php`, …) ([[directory-fuzzing]]).
3. **WP user enumeration** — browsing the site reveals a username: `mario` ([[wordpress-enumeration]]).
4. **Brute-force login** — `wpscan --url http://TARGET/wordpress -U mario -P rockyou.txt` finds `mario` / `love` ([[wordpress-enumeration]]).
5. **Reverse shell** — logged in as admin, edit a theme file (`twentytwentytwo/index.php`) in the theme editor to drop a PHP reverse shell, then trigger it by visiting that file. Listener: `nc -lvnp 443`. Shell lands as `www-data` ([[reverse-shells]]).
6. **Privesc** — `find / -perm -4000` shows `/usr/bin/env` is SUID. `env /bin/sh -p` → **root** ([[suid-enumeration]]).

## Credentials / secrets

| Item | Value |
|------|-------|
| WordPress (`mario`) | `love` |

## Takeaways

- The box name pointed at a CMS; the CMS was a **WordPress buried behind the default Apache page** — always fuzz the web root, not just the obvious path ([[directory-fuzzing]]).
- **wpscan** is the one-stop WordPress tool: user enumeration, plugin/theme audit, and login brute-force in a single invocation ([[wordpress-enumeration]]).
- WordPress admin → **theme/plugin file editor** = arbitrary PHP execution = instant [[reverse-shells]] once you have admin creds.
- `env /bin/sh -p` on a SUID `/usr/bin/env` is the same GTFOBins privesc seen in [[duque]] ([[suid-enumeration]]).
