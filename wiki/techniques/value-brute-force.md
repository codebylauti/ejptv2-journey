---
type: technique
tags: [ejpt:web-pentest]
tools: [burp-suite]
cves: []
related: [[parameter-fuzzing]]
---

# Value Brute Force

Brute-forcing the *value* of a known parameter (a numeric ID, a token range) and spotting the one response that differs — usually by `Content-Length` or status code.

## When to use

You know the parameter name but not the winning value. Send every candidate and flag the response that stands out: a different size, a different status, or a redirect.

## Python

```python
import requests
url = "http://TARGET/generate.php"
expected = len("test")            # the "normal" echo, used as baseline
for i in range(1, 101):
    r = requests.post(url, data={"content": "test", "number": i})
    if len(r.text) != expected:
        print(i, r.status_code, r.text[:100])
```

- Compare against the *baseline* (the echoed/same response) and flag deviations.
- **Binary responses** (e.g. a ZIP): save `r.content` in `"wb"` mode — `r.text` mangles non-UTF-8 bytes.

## Burp Intruder alternative

Set the payload position on the value, run a numeric (or wordlist) payload, then sort results by **response length** to find the outlier.

## Seen in

[[grooti]] (`generate.php?number=1..100` → number 16 returned a ZIP)
