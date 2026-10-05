---
type: tool
category: client
related: ["[[ftp-anonymous-login]]", "[[hardcoded-credentials]]"]
---

# FTP (client)

Interactive File Transfer Protocol client — connect, read the banner, list, download, upload.

## Command

```sh
ftp TARGET
# Name (anonymous): anonymous
# Password: (blank)
ls / get file / put file / bye
```

- The login prompt doubles as recon: the **banner is served before authentication** — read it fully, it occasionally leaks working credentials ([[hardcoded-credentials]]).
- Anonymous servers accept `anonymous`/`anonymous` (or `anonymous`/any email) — the first thing to try on any FTP port ([[ftp-anonymous-login]]).
- `put` from an anonymous session onto a web-readable directory is the classic upload-to-RCE chain ([[anonymous-pingu]]).

## Seen in

[[obsession]], [[tproot]], [[hannah-coffee]], [[nodeclimb]], [[anonymous-pingu]], [[dance-samba]]
