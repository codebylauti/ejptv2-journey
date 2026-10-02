---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: [[reverse-shells]], [[suid-enumeration]]
---

# Restricted Shell Escape

`rbash` (restricted bash) limits what a logged-in user can do — no absolute paths, no redirection, no `su`, `PATH` pinned inside the user's home. It's a policy layer, not a security boundary: escape it and you get a normal shell to continue enumeration.

## Recognizing it

- Errors and prompts prefixed `-rbash:` (e.g. `-rbash: sudo: command not found`).
- `echo $PATH` shows only a directory inside the user's home (`/home/user/bin`).
- Commands fail with `command not found` unless they live on that path — even `whoami`.
- Redirection (`>`, `>>`) and absolute paths (`/bin/bash`) are refused.

## Escape (exercised on [[chmod-4755]])

`python3` spawns a full bash — but the restricted `PATH` survives the spawn, so it must be rebuilt:

```sh
python3
>>> import pty; pty.spawn("/bin/bash")
whoami                       # still fails: only /home/<user>/bin on PATH
export PATH=/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:$PATH
id
```

Both halves matter: the `pty.spawn` gets you a real shell, the `export` gives it real commands. From here the normal foothold workflow resumes (file enum, `find / -perm -4000`, [[suid-enumeration]]).

## Other standard vectors (documented, not yet exercised)

- `vim`/`vi` → `:set shell=/bin/bash` → `:shell`
- `less`/`more`/`man` → `!bash`
- `ssh <user>@localhost` from inside the session — a fresh login is a fresh (unrestricted) shell
- Any interpreter on the restricted path that can `exec` (`awk`, `perl`, `env`)

## Seen in

[[chmod-4755]] (python3 `pty.spawn` + PATH rebuild → `user.txt`, then SUID privesc to root)
