---
type: technique
tags: [ejpt:assessment, ejpt:web-pentest]
tools: [curl]
cves: []
related: [[directory-fuzzing]], [[information-gathering]]
---

# Virtual Hosting (vhost) Discovery

Finding a website served under a specific `Host` header/hostname, hidden behind the IP's default page.

## Detection

- The IP serves a **default page** (e.g. Apache "It works") — but source comments, hints, or DNS give away another hostname.
- Clues like *"virtual hosting is good"*, *"register for <domain>"* in HTML comments.

## Exploit

1. Map the hostname to the IP in `/etc/hosts`:

   ```
   10.10.10.2   target.thm
   ```

2. Browse `http://target.thm/` (or `curl -H "Host: target.thm" http://IP/`).

The web server routes on the `Host` header, so the same IP serves a *different* app for that hostname.

## Fuzzing unknown vhosts

```sh
ffuf -u http://TARGET -H "Host: FUZZ.target.thm" -w <wordlist> -fw <size>
```

- Filter with `-fw`/`-fs` against the default page's response to find live vhosts.

## Seen in

[[madeyes-castle]] (`hogwartz-castle.thm` behind the default Apache page)
