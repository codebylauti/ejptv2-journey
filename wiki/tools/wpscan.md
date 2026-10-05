---
type: tool
category: scanner
related: ["[[wordpress-enumeration]]"]
---

# wpscan

WordPress-specific security scanner — detects the WP version, enumerates users/plugins/themes, flags known vulnerabilities (via the WPVulnDB), and brute-forces `wp-login.php`.

## Command

```sh
wpscan --url http://TARGET/wordpress --enumerate u        # enumerate users
wpscan --url http://TARGET/wordpress --enumerate vp       # vulnerable plugins
wpscan --url http://TARGET/wordpress -U user -P rockyou.txt   # login brute-force
```

## Key flags

- `--url` target · `--enumerate u|p|t|vp` (users / plugins / themes / vulnerable plugins) · `-U`/`-P` user/password lists · `--api-token` for live WPVulnDB lookups.

## Notes

- `--enumerate u` can often find usernames without brute-force via author archives or REST API (`/wp-json/wp/v2/users`).
- A weak `wp-login` password is the fastest route to admin → theme editor → RCE (see [[wordpress-enumeration]]).

## Seen in

[[walkingcms]] (user `mario` brute-forced to `love`)
