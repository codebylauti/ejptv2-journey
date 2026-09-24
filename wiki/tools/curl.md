---
type: tool
category: http-client
related: [[information-gathering]], [[node-inspector-rce]], [[prototype-pollution]]
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

## Seen in

[[autoescuela]] (Node inspector `/json` + React2Shell exploit), [[los-3-hackers]], [[psycho]], [[balufood]], [[balulero]], [[hannah-coffee]], [[wargames]], [[grooti]], [[winfake]], [[duque]], [[injection]], [[pipepwned]] (SSTI payloads via `-d name=`/`-d ref=` POST), [[trailpack]] (crafted `user_info` cookie against `/api/me` + `/accounting`), [[bruteshock]] (Shellshock `User-Agent` payload)
