---
type: tool
category: fuzzer
related: [[parameter-fuzzing]]
---

# ffuf

Fast web fuzzer for directories, parameters, virtual hosts, and more.

## Command

```sh
# hidden parameter discovery
ffuf -u "http://TARGET/index.php?FUZZ=test" -w /usr/share/seclists/Discovery/Web-Content/burp-parameter-names.txt -fw 198
# directory fuzzing
ffuf -u "http://TARGET/FUZZ" -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-small.txt -fw 3427
```

- `-fw` filters responses by word count (calibrate against a known 404 first).

## Seen in

[[hannah-coffee]] (hidden `studio` parameter discovery), [[psycho]] (hidden `secret` parameter), [[walkingcms]] (root directory fuzz → `wordpress/`), [[pipepwned]] (numeric job-ID fuzz `/api/jobs/FUZZ/trace` + endpoint fuzz `/api/FUZZ`), [[littlepivoting]] ([[local-file-inclusion]] fuzz with `LFI-Jhaddix.txt`, filtered by `-fs`/`-fw`), [[cap]] (IDOR ID-space sweep `/data/FUZZ` with `3-digits-000-999.txt`, `-fc 302`)
