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
- The server **actively redirects** to a hostname: a `303 See Other` with `Location: http://internal.dl/` names the vhost outright (`curl -s http://IP/` to see it) ([[internal]]).

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

With [[gobuster]], fuzz `*.domain` subdomains directly and discard the default site's redirect:

```sh
gobuster vhost -u http://target.thm/ -w <subdomains-wordlist> --append-domain --xs 303
```

- `--append-domain` appends the base domain to every word (`word.target.thm`).
- `--xs 303` excludes the 303 the default vhost throws, leaving the `200`s.

## Seen in

[[madeyes-castle]] (`hogwartz-castle.thm` behind the default Apache page), [[internal]] (303 → `internal.dl` → `gobuster vhost` → `backup.internal.dl`)
