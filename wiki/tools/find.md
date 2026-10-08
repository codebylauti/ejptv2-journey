---
type: tool
category: search
related: ["[[hardcoded-credentials]]", "[[suid-enumeration]]", "[[group-ownership-enumeration]]"]
---

# find

GNU find — the filesystem search workhorse: locate files by name, type, owner, permissions, size, or modification time. Behind most of this vault's local discovery.

## Command

```sh
find / -name '*.txt' 2>/dev/null           # by name/glob (stderr must be silenced)
find / -name '*<username>*' 2>/dev/null    # files planted for a specific user
find / -perm -4000 2>/dev/null             # SUID binaries (privesc hunting)
find / -group <group> -writable -ls        # group-writable files
find / -mtime -1 -type f 2>/dev/null       # files touched in the last day
```

- **`2>/dev/null` is mandatory** on a full-filesystem sweep — `/proc` and `/sys` spew errors that bury the results.
- **Quote the glob.** `find / -name *spencer*` lets *your shell* expand the pattern first against the local working directory — one matching file in the CWD silently replaces the search term with its literal name. `'…'` keeps find as the only process that sees the pattern. This exact latent bug has shipped in three vault writeups ([[extraviado]], [[pkgpoison]], [[pequeñas-mentirosas]]).
- **The filename is often the signal.** `hash_spencer.txt`, `passdiego`, `secret.cpython-38.pyc` — the name tells you what (and *who*) the file is for before you open it, which is why `find / -name *<username>*` is the default move right after reading `/etc/passwd` for names ([[hardcoded-credentials]]).
- Pairs with the privesc hunts: `-perm -4000` feeds [[suid-enumeration]], `-group`/`-writable` feeds [[group-ownership-enumeration]]; capabilities get their own sweep in [[getcap]].

## Seen in

[[extraviado]] (`*diego*` → `~/.secreto/passdiego`), [[pkgpoison]] (`*secret*` → the leaky `.pyc`), [[pequeñas-mentirosas]] (`*spencer*` → `/srv/ftp/hash_spencer.txt`), [[nexus]] (`-name .env` → the app's live on-disk credentials at `/var/www/krayin/.env`), plus routine full-filesystem sweeps across the vault's privesc paths ([[dark]], [[domain]], [[rutas]], [[trailpack]], [[walkingcms]] and more)
