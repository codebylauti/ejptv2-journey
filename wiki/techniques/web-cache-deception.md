---
type: technique
tags: [ejpt:web-pentest]
tools: [burp-suite]
cves: []
related: ["[[xss-and-cookie-theft]]"]
---

# Web Cache Deception

Tricking a web cache into storing a sensitive page so an unprivileged user can retrieve the cached copy.

## Signals

- `X-Cache: HIT` / `X-Cache: BYPASS` headers in responses.
- Sensitive endpoints (e.g. `credentials-report.pdf`) that are normally admin-only.

## Flow

1. Confirm pages are cached (`X-Cache: HIT`).
2. Get an admin to request the target URL (e.g. via a link in a help-center form).
3. Once cached, fetch the page and retrieve the leaked content.

## Seen in

[[adopting]] (leaked `credentials-report.pdf` → SSH creds)
