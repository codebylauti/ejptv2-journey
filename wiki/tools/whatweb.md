---
type: tool
category: scanner
related: [[information-gathering]], [[directory-fuzzing]]
---

# Whatweb

Web fingerprinting one-shot: identifies the CMS, frameworks, JS libraries, server headers, and page title in a single request.

## Command

```sh
whatweb TARGET                 # e.g. whatweb 10.129.148.255:80
```

- Run it **before directory fuzzing** so you know which wordlist and extensions make sense ([[information-gathering]] step 3, [[directory-fuzzing]]).
- One line of output beats manually chaining `curl -sI` for a first read on an unknown stack.

## Seen in

[[cap]] (Gunicorn "Security Dashboard" fingerprint on port 80)
