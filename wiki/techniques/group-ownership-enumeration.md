---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: [[cron-job-abuse]], [[suid-enumeration]]
---

# Group Ownership Enumeration

Finding files and directories your current groups can write, which may be executed or used by a privileged process.

## Commands

```sh
find / -group <group> -ls 2>/dev/null
# also useful:
find / -user <username> -ls 2>/dev/null
find / -writable -type f 2>/dev/null
```

- Compare results against your `id` groups.
- A file owned by a group you're in (and group-writable) is one you can overwrite.
- Cross-reference with `ps aux` / cron to see if a privileged process runs it → [[cron-job-abuse]].

## Seen in

[[balulero]] (`/opt/script.php` owned by the `chocolate` group, run as root)
