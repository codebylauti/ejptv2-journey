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

## Signals

- A `role` / `is_admin` / `type` field in a cookie, token, or response body.
- An endpoint that returns `access_denied` for `user` but is advertised/redirected for admins.
- The lesson encoded in the flag: "client-side role is no security."

## Seen in

[[trailpack]] (base64 `user_info` cookie `role:user → admin` unlocks `/accounting`)
