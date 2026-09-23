---
type: tool
category: scanner
related: [[directory-fuzzing]]
---

# Dirb

Classic web directory brute-forcer (alternative to [[gobuster]]).

## Command

```sh
dirb http://TARGET /usr/share/wordlists/dirb/common.txt
```

## Seen in

[[hannah-coffee]] (found `index.php` and listable `/pages/`), [[balufood]] (found `/admin`, `/console`, `/login`, `/logout`), [[balulero]] (found `index.html`), [[psycho]] (listable `/assets/`), [[pipepwned]] (found `/health`)
