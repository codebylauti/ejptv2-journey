---
type: technique
tags: [ejpt:host-net-pentest]
tools: [netcat]
cves: []
related: ["[[reverse-shells]]", "[[linux-capabilities]]"]
---

# Cron Job Abuse

Exploiting cron jobs or automated scripts that run with elevated privileges and are writable by a lower-privileged user.

## Workflow

1. Inspect `/etc/cron.d/`, `crontab -l`, and `/opt` for scheduled scripts; `ps aux`/`ps -ef` can also reveal a privileged process running a script you can write — **the runner need not be cron at all**: PID 1's `while true; do /bin/bash /usr/local/bin/echo.sh; done` loop runs its target *continuously*, which collapses step 3's "wait" to milliseconds ([[vulnvault]]).
2. Check ownership/permissions — if your group can write the script, overwrite it. Check the **`o+w` bit** too: `-rwxrw-rw-` is world-writable, no group membership required ([[vulnvault]] — every earlier sighting needed the right group).
3. Replace the script with a reverse shell or a **privilege-granting command**; wait for the next run (or ~instantly, on a loop). The grant form pairs with a SUID-shell endgame: write `chmod u+s /bin/bash`, then `/bin/bash -p` (preserve euid) ([[acme]], [[suid-enumeration]]).

## Seen in

- [[los-3-hackers]] — writable `/opt/maintenance/m.sh` run as `blackhacker`.
- [[baluhome]] — group-writable `/opt/balutube-backup/backup.sh` run as root.
- [[balulero]] — group-owned `/opt/script.php` run as root; discovered via `ps aux`.
- [[grooti]] — writable `/tmp/malicious.sh` run as root by `/opt/cleanup.sh`.
- [[vulnvault]] — world-writable `/usr/local/bin/echo.sh` hammered by PID 1's while-loop; found via `ps -ef`, consumed as `/bin/bash -p` (the payload write itself is missing from the writeup).

## See also

- [[linux-capabilities]] (alternative privesc route)
