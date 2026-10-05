---
type: tool
category: analyzer
related: ["[[pcap-analysis]]"]
---

# tshark

Command-line packet analyzer — the terminal sibling of Wireshark. Reads captures (`-r`) or live interfaces, filters with **display filters** (`-Y`), and can extract structured fields instead of dumping whole packets.

## Core usage

```sh
tshark -r capture.pcap                          # read a capture
  -Y 'http.request.method==POST'                # display filter (read the capture first)
  -T fields -e ip.src -e http.user_agent        # extract specific fields
  -q -z follow,tcp,ascii,10                     # dump TCP stream 10 as ASCII
```

- `-Y` filters **packets**; `-R`/`-e` field extraction needs `-T fields`.
- Find a stream index first: `-Y '<filter>' -T fields -e tcp.stream | uniq`.
- Field extraction + `sort -u` = instant unique-value lists (URIs, UAs, methods).

## Seen in

- [[analyst]] — every incident answer: POST filter, IP attribution, UA/URI extraction, `follow,tcp,ascii` on the upload and reverse-shell streams, credential grep on the reset message.
