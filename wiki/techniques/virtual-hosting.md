---
type: technique
tags: [ejpt:assessment, ejpt:web-pentest]
tools: [curl]
cves: []
related: ["[[directory-fuzzing]]", "[[information-gathering]]"]
---

# Virtual Hosting (vhost) Discovery

Finding a website served under a specific `Host` header/hostname, hidden behind the IP's default page.

## Detection

- The IP serves a **default page** (e.g. Apache "It works") — but source comments, hints, or DNS give away another hostname.
- Clues like *"virtual hosting is good"*, *"register for <domain>"* in HTML comments.
- **Candidate hostnames handed over as links** — an `<aside>` listing `vulndb.com`, `trackedvuln.dl/`, `dockerlabs.es` is a menu of vhosts; map the one the rest of the chain points at and re-fuzz *with* the credential you already hold ([[rutas]]).
- The server **actively redirects** to a hostname: a `303 See Other` with `Location: http://internal.dl/` names the vhost outright (`curl -s http://IP/` to see it) ([[internal]]). Even an *unfollowed* redirect counts — nmap's `http-title` note *"Did not follow redirect to http://nexus.htb/"* hands you the base domain before any fuzzing runs ([[nexus]]).

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
- **A redirect in the results is not automatically noise.** [[nexus]]'s default vhost threw a 302, so nothing was excluded — and the hits were a `200` (`git.nexus.htb`) plus a `302 → /admin/login` (`billing.nexus.htb`). A redirect that lands on an *application* is a find; only the default vhost's canned redirect is junk.

## Seen in

[[madeyes-castle]] (`hogwartz-castle.thm` behind the default Apache page), [[internal]] (303 → `internal.dl` → `gobuster vhost` → `backup.internal.dl`), [[rutas]] (`trackedvuln.dl` from an `<aside>` link → `/etc/hosts` → re-fuzz with `Authorization: Basic`), [[nexus]] (unfollowed 302 named the base domain → `gobuster vhost --append-domain` → `git.nexus.htb` 200 + `billing.nexus.htb` 302 → `/admin/login`)
