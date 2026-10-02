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

Pre-auth MOTD/banner text sometimes contains working credentials ([[hardcoded-credentials]], [[acme]]). Same idea applies to telnet/FTP banners.

## scp (push files through a foothold)

```sh
scp tool user@TARGET:/tmp/
```

No route-back needed — the SSH pipe is two-way.

## Seen in

[[littlepivoting]] (SSH login to `inclusion`/`trust`; `-D`/`-L`/`-R` discussion; manual re-run logged into `trust` with `proxychains ssh`), [[acme]] (pre-auth banner credential disclosure → foothold), [[cap]] (stolen `nathan` password replayed from FTP to SSH)
