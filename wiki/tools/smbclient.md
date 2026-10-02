---
type: tool
category: client
related: [[smb-enumeration]], [[smbmap]]
---

# Smbclient

Interactive SMB client with an FTP-like shell — browse, download, and upload files when [[smbmap]] shows the share is readable/writable.

## Command

```sh
smbclient //TARGET/share -U user --password=pass   # authenticated
smbclient //TARGET/share -N                        # null session
```

Inside the shell (FTP-style verbs):

```text
ls                       # list
get file.txt             # download
put payload.php          # upload — write access to a webshare = [[web-shell-upload]]
mput dir                 # upload a whole local dir (used for .ssh/ — see below)
recurse on / prompt off  # prepare a bulk pull
mget *                   # grab everything
```

- The machine page's `**Writeup:**`-level flow: list first, read what's there, *then* decide if upload is possible.
- An empty-looking recursive sweep is still a result: `print$`'s driver dirs were all empty on [[chmod-4755]] (negative result, documented).
- **`mput` for persistence** — when the writable share maps a user's home, upload a generated `.ssh/` (`authorized_keys` inside) and SSH in with your own key: no password needed ([[dance-samba]], see [[ssh]]).

## Seen in

[[domain]] (`put payload.php` → webshell on the `html` share), [[chmod-4755]] (`note.txt` hint + recursive `print$` sweep), [[madeyes-castle]] (`-N` null pull of `sambashare`), [[dance-samba]] (recursive `mget *` of the home share → `user.txt`, then `mput .ssh` for key-based access)
