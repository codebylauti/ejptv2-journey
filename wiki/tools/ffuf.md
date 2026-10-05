---
type: tool
category: fuzzer
related: ["[[parameter-fuzzing]]"]
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

**Calibrate against a boundary, not just a 404.** Fuzzing the *same* URL before and after you send a credential shows the size delta (`901` vs `1116`), which is both proof the credential is real and the value you then filter with `-fs` ([[rutas]]).

## Fuzzing inside a multipart body

Some sinks only fire for a `multipart/form-data` upload — PHP fills `$_FILES` **only** for that shape, so a urlencoded `-d "archivo=x.php"` silently touches nothing. Put the keyword in the body and declare the boundary yourself:

```sh
ffuf -u http://TARGET/subir_archivo.php -X POST \
  -H "Content-Type: multipart/form-data; boundary=----b" \
  -d $'----b\r\nContent-Disposition: form-data; name="archivo"; filename="probe.FUZZ"\r\n\r\n...\r\n----b--' \
  -w extensions.txt -fs 33
```

- `$'…'` is required so bash turns `\r\n` into real CRLF — without it the boundary never closes and every request 400s.
- **Calibrate on the rejection.** `-fs 33` here is the size of a *refused* upload, not a 404: when every answer is `200`, length is the only signal left, and the one entry that disagrees is the answer ([[file]] → `phar`).
- `-e .php,.phtml` appends extensions to the keyword instead of writing a wordlist — handy when `FUZZ` is a basename.

## Seen in

[[hannah-coffee]] (hidden `studio` parameter discovery), [[psycho]] (hidden `secret` parameter), [[walkingcms]] (root directory fuzz → `wordpress/`), [[pipepwned]] (numeric job-ID fuzz `/api/jobs/FUZZ/trace` + endpoint fuzz `/api/FUZZ`), [[littlepivoting]] ([[local-file-inclusion]] fuzz with `LFI-Jhaddix.txt`, filtered by `-fs`/`-fw`), [[cap]] (IDOR ID-space sweep `/data/FUZZ` with `3-digits-000-999.txt`, `-fc 302`), [[rutas]] (parameter-name fuzz → `love`, `-fs 901`; then an LFI wordlist that found nothing because the sink wanted a URL), [[file]] (multipart extension fuzz → `phar`, `-fs 33` rejection baseline)
