---
type: technique
tags: [ejpt:web-pentest, ejpt:assessment]
tools: [wpscan, gobuster, ffuf]
cves: []
related: ["[[directory-fuzzing]]", "[[reverse-shells]]"]
---

# WordPress Enumeration & Exploitation

WordPress is a high-value CMS target: once you find the instance, enumerate users/plugins, then exploit a weak login or a known plugin vuln to reach admin and turn it into code execution.

## Attack chain

1. **Discover the instance** — WP often hides behind a default page. Fuzz the root for `wordpress/`, `wp-admin/`, `wp-login.php` ([[directory-fuzzing]]).
2. **Enumerate users** — via author archives, `wp-json/wp/v2/users`, or just browsing the site; confirm with `wpscan --enumerate u`.
3. **Brute-force login** — `wpscan -U <user> -P rockyou.txt` against `wp-login.php`.
4. **Audit plugins/themes** — `wpscan --enumerate vp` for known-vulnerable components.
5. **RCE via admin** — with admin access, edit a theme/plugin PHP file in the editor (`Appearance → Theme Editor`) to drop a web/reverse shell, then trigger it by visiting the file ([[reverse-shells]]).

## Notes

- `xmlrpc.php` returning `405` still implies WP is present; `wp-config.php`/`wp-load.php` returning `200` with size 0 confirms it.
- The theme editor is the fastest admin→shell route: it writes arbitrary PHP directly to disk, which you then execute by URL.

## Seen in

[[walkingcms]]
