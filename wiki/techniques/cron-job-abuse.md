---
type: technique
tags: [ejpt:host-net-pentest]
tools: [netcat]
cves: []
related: [[reverse-shells]], [[linux-capabilities]]
---

# Cron Job Abuse

Exploiting cron jobs or automated scripts that run with elevated privileges and are writable by a lower-privileged user.

## Workflow

1. Inspect `/etc/cron.d/`, `crontab -l`, and `/opt` for scheduled scripts; `ps aux` can also reveal a privileged process running a script you can write.
2. Check ownership/permissions — if your group can write the script, overwrite it.
3. Replace the script with a reverse shell or privilege-granting command; wait for the next run.

## Seen in

- [[los-3-hackers]] — writable `/opt/maintenance/m.sh` run as `blackhacker`.
- [[baluhome]] — group-writable `/opt/balutube-backup/backup.sh` run as root.
- [[balulero]] — group-owned `/opt/script.php` run as root; discovered via `ps aux`.
- [[grooti]] — writable `/tmp/malicious.sh` run as root by `/opt/cleanup.sh`.

## See also

- [[linux-capabilities]] (alternative privesc route)
