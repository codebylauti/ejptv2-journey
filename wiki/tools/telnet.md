---
type: tool
category: networking
related: ["[[netcat]]", "[[vsftpd-backdoor]]"]
---

# Telnet

Classic TCP client for speaking plaintext protocols (FTP, SMTP, IRC) by hand — handy for banner grabs and for crafting raw commands a full client won't let you send.

## Common usage

```sh
telnet TARGET 21     # talk to FTP manually, send raw commands
telnet TARGET 6667   # IRC and other line-based protocols
```

- Use it when the attack is a *specific wire-level command* rather than a full workflow — e.g. the `USER anonymous:)` trigger of [[vsftpd-backdoor]].

## Seen in

[[first-hacking]] (vsftpd 2.3.4 backdoor trigger); see [[vsftpd-backdoor]].
