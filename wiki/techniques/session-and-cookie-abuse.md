---
type: technique
tags: [ejpt:web-pentest]
tools: [curl]
cves: []
related: ["[[xss-and-cookie-theft]]", "[[sql-injection]]"]
---

# Session and Cookie Abuse

Using leaked, forged, or stolen session cookies to access protected resources or impersonate a user.

## Vectors

- **Stolen cookies** via [[xss-and-cookie-theft]].
- **Decoding/forging** session tokens — e.g. a Flask session cookie whose `role` field can be tampered with.
- **Base64 cookie tampering** — a cookie like `user_info` is just `btoa({user, role, email})`; decode, flip `role` to `admin`, re-encode ([[trailpack]]).
- **Reusing** an authenticated session to download protected files (e.g. `wow.zip` in [[los-3-hackers]]).

## Seen in

[[los-3-hackers]] (admin session cookie → download protected zip), [[baluhome]] (admin cookie theft), [[trailpack]] (base64 role cookie → admin)
