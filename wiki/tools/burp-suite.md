---
type: tool
category: proxy
related: [[web-cache-deception]], [[xss-and-cookie-theft]]
---

# Burp Suite

Intercepting proxy for web app testing: request tampering, match-and-replace, repeater.

## Uses seen

- **Match & Replace** — swap `role=user` → `role=admin` in responses ([[adopting]]).
- **Content-Type spoofing** — change upload MIME to `image/png` to pass filters ([[baluhome]]).

## Seen in

[[adopting]], [[baluhome]]
