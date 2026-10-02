---
type: tool
category: framework
related: [[port-forwarding]], [[pivoting]]
---

# SSH

Secure shell — remote login, file transfer, and (critically) **tunneling** via port forwarding.

## Port forwarding flags

| Flag | Listener | Egress (where data emerges) |
|------|----------|----------------------------|
| `-L 8000:host:port` | our machine `:8000` | the SSH server |
| `-R 8000:host:port` | the SSH server `:8000` | our machine |
| `-D 1080` | our machine `:1080` (SOCKS) | the SSH server |

- `-L`/`-R` are **static** (fixed pipe to one host:port); `-D` is **dynamic** (SOCKS, target chosen per request).
- Through `-D`, `127.0.0.1` resolves on the *server's* side — see [[port-forwarding]].

## Banner / MOTD enumeration

Connect **before** you have credentials — with any username — and read everything printed above the password prompt:

```sh
ssh random_user@TARGET
```

Pre-auth MOTD/banner text sometimes contains working credentials ([[hardcoded-credentials]], [[acme]]) — or, when it's signed *by someone* (`by fuckit`), a **username** to feed into the next spray ([[chmod-4755]]). Same idea applies to telnet/FTP banners.

## scp (push files through a foothold)

```sh
scp tool user@TARGET:/tmp/
```

No route-back needed — the SSH pipe is two-way.

## authorized_keys (key persistence without the password)

You don't need a user's password if you can write their home directory — e.g. via a **READ,WRITE SMB share**:

```sh
ssh-keygen -t ed25519 -C "user"        # 1. generate a keypair
# 2. write the .pub line into .ssh/authorized_keys locally
# 3. upload .ssh/ over the writable share (smbclient: mput .ssh)
ssh -i ~/.ssh/id_ed25519 user@TARGET   # 4. log in, password never involved
```

Works the same way with any write primitive onto a home dir (FTP `put`, webshell, cron job) — and it survives even when you never learn the account's real password ([[dance-samba]], see [[smbclient]]).

## Seen in

[[littlepivoting]] (SSH login to `inclusion`/`trust`; `-D`/`-L`/`-R` discussion; manual re-run logged into `trust` with `proxychains ssh`), [[acme]] (pre-auth banner credential disclosure → foothold), [[cap]] (stolen `nathan` password replayed from FTP to SSH), [[flynn]] (default creds `flynn:flynn`, no brute-force), [[analyst]] (pcap-captured `pinguinito` password), [[chmod-4755]] (banner username hint → `rabol:share_secret_only` → `rbash`), [[dance-samba]] (`authorized_keys` uploaded over a writable SMB home → `ssh -i` with no password)
