---
type: tool
category: framework
related: [[guided-pentest]], [[reverse-shells]]
---

# Metasploit

Exploitation framework (`msfconsole`) for searching and running modules.

## Workflow

```sh
searchsploit <service>       # find known exploits
msfconsole
search <module>; use <module>; set RHOSTS ...; exploit
```

## Seen in

[[guided-pentest]] (UnrealIRCd backdoor module)
