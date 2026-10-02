---
type: technique
tags: [ejpt:web-pentest]
tools: [burp-suite, curl]
cves: []
related: [[session-and-cookie-abuse]]
---

# Broken Access Control

The app enforces authorization from data the *client* supplies — a role field, an ID, a cookie — without re-checking it server-side. Flip the value and you gain privileges.

## The client-side role pattern

A cookie (or JWT, or hidden form field) carries `role=user`. If the server trusts it for access decisions (rather than looking the role up from the session/DB), rewriting it to `role=admin` escalates you.

Common encodings to decode → edit → re-encode:

```sh
# decode
echo 'eyJyb2xlIjoidXNlciJ9' | base64 -d      # {"role":"user"}
# edit, then re-encode
echo -n '{"role":"admin"}' | base64
```

> In [[burp-suite]] this is a **Match & Replace**, but note: match-and-replace operates on the *raw* (encoded) request, so you must replace the whole encoded value, not the plaintext inside it.

## IDOR — insecure direct object reference

The other half of broken access control: a resource is addressed by a raw ID (`/data/3`, `/download/0`, `/api/jobs/42/trace`) and the server never checks that the ID belongs to *your* session. Own objects are just the low numbers — enumerate the ID space:

```sh
# sequential numeric IDs → fuzz the path segment, drop the "not found" redirect/404
ffuf -u http://TARGET/data/FUZZ -w /usr/share/seclists/Fuzzing/3-digits-000-999.txt -fc 302
```

- The ID *format* often leaks before you fuzz: a redirect to `/data/1`, a `?id=7` link, an incrementing API response.
- The payoff is other users' data — files, captures, orders, PII — and frequently credentials inside them ([[cap]]).

## Signals

- A `role` / `is_admin` / `type` field in a cookie, token, or response body.
- An endpoint that returns `access_denied` for `user` but is advertised/redirected for admins.
- Object IDs in URLs, form fields, or API paths — especially sequential ones.
- The lesson encoded in the flag: "client-side role is no security."

## Seen in

[[trailpack]] (base64 `user_info` cookie `role:user → admin` unlocks `/accounting`), [[cap]] (`/data/<id>` + `/download/<id>` IDOR → other users' pcaps → FTP/SSH credentials)
