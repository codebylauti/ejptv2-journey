---
type: machine
platform: tryhackme
difficulty: easy
ip: 10.64.128.29
cves: []
tools: [nmap, gobuster, curl, sqlmap, hydra, john-the-ripper, gtfobins, ssh]
techniques: [information-gathering, directory-fuzzing, virtual-hosting, sql-injection, hash-cracking, smb-enumeration, sudo-abuse, suid-enumeration, path-hijacking]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: [[basic-pentesting]], [[wargames]]
---

# Madeye's Castle

**Writeup:** [raw writeup](../../writeups/tryhackme/madeyes-castle.md)

Harry Potter–themed box: vhost discovery → SQLi on a SQLite login → crack a SHA-512 hash → SSH → pico sudo escape → SUID binary PATH-hijack.

## Path

1. **Recon** — `nmap`: `22` SSH, `80` Apache, `139`/`445` SMB.
2. **Vhost** — source comment hints *"virtual hosting"* + `hogwartz-castle.thm` → add to `/etc/hosts` ([[virtual-hosting]]).
3. **SQLi** — login leaks data in a JSON error; `' OR '1'='1` reveals user "Lucas Washington" + *"keep digging"*. UNION-based on SQLite: `sqlite_master` → `users` table (`name, password, admin, notes`), `group_concat` dumps all 40 users ([[sql-injection]]).
4. **Crack** — Harry Turner's note: *"password uses best64"* → `john --rules=best64` → `wingardiumleviosa123` ([[hash-cracking]]).
5. **SMB** — `smbmap`/`smbclient` on `sambashare` → `spellnames.txt` + `.notes.txt` hints ([[smb-enumeration]]); hydra SMB finds `avadakedavra:123456`.
6. **Foothold** — SSH as `harry` → User1.
7. **harry → hermonine** — `sudo -l`: `(hermonine) /usr/bin/pico` → pico escape `^R` `^X` + `reset; sh 1>&0 2>&0` ([[sudo-abuse]]) → User2.
8. **hermonine → root** — `find / -perm -4000` → SUID `/srv/time-turner/swagger`; `strings` shows `system("uname -p")` + `srand(time)`. PATH-hijack (`/tmp/uname` + `export PATH=/tmp:$PATH`) + predict the time-seeded number → root ([[suid-enumeration]], [[path-hijacking]]).

## Credentials

| Item | Value |
|------|-------|
| SMB | `avadakedavra` / `123456` |
| SSH (harry) | `harry` / `wingardiumleviosa123` |
| hermonine | via `sudo -u hermonine pico` escape |

## Takeaways

- Default Apache page + "virtual hosting" comment = enumerate the vhost, not the IP ([[virtual-hosting]]).
- SQLite UNION: tables live in `sqlite_master`; `group_concat` dumps every row at once ([[sql-injection]]).
- "password uses best64" = John `--rules=best64` ([[hash-cracking]]).
- `pico` is the "historical text editor" → GTFOBins escape ([[sudo-abuse]]).
- SUID binary calling `system("uname -p")` (relative) = [[path-hijacking]]; `srand(time(NULL))` = reveal + re-run in the same second.
