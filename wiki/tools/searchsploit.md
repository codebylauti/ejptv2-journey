---
type: tool
category: reference
related: ["[[metasploit]]", "[[sql-injection]]"]
---

# SearchSploit

Command-line frontend for Exploit-DB: look up known exploits by service, version, or CMS name.

## Common usage

```sh
searchsploit vsftpd 2.3.4
searchsploit "CMS Made Simple"
searchsploit -m <EDB-ID>      # mirror (download) the exploit to disk
```

- Pair with an `nmap -sV` version banner: the banner is the search term, searchsploit returns the candidate exploit — often a ready-made PoC or a [[metasploit]] module name.

## Seen in

[[guided-pentest]] (UnrealIRCd backdoor), [[simple-ctf]] (CMS Made Simple); see [[sql-injection]] for the version-banner → exploit loop.
