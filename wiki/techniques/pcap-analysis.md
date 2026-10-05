---
type: technique
tags: [ejpt:assessment, ejpt:host-net-pentest]
tools: [tshark]
cves: []
related: ["[[hardcoded-credentials]]", "[[source-code-disclosure]]"]
---

# PCAP Analysis

Reconstructing an attack — and often harvesting credentials — from a packet capture. Two entry points: a **pcap the target offers you for download** (incident/forensics labs, dashboard exports), or one you capture yourself.

## Workflow

1. Get the capture (`curl`/`wget` from the target, or export from a proxy/dashboard) and open it with `tshark -r file.pcap`.
2. **Orient** — which hosts talk to each other, which protocols matter. Start broad: `-Y 'http.request'`, `-Y 'tcp.flags.syn==1 && tcp.flags.ack==0'` for connection attempts.
3. **Attribute** — filter on the suspect IP and extract unique values with `-T fields -e <field> | sort -u` (User-Agent, URI, method).
4. **Read conversations** — map `tcp.stream` indexes (`uniq`), then dump the interesting one: `-q -z follow,tcp,ascii,<stream>`.
5. **Harvest** — grep followed streams for credential material: `USER|PASS`, `password`, `contrasena`, `reset`.
6. **Cross-reference** — match IPs/hosts against any accompanying artifact (threat-intel feeds, logs) to complete attribution.

## Filters that repeatedly pay off

| Goal | Display filter |
|------|----------------|
| HTTP methods | `http.request.method==POST` |
| One host's traffic | `ip.src==<suspect> \|\| ip.dst==<suspect>` |
| Outbound callbacks (reverse shells) | `ip.src==<victim> && tcp.flags.syn==1 && tcp.flags.ack==0` |
| Extract fields | `-Y … -T fields -e ip.src -e http.user_agent \| sort -u` |
| Read a whole stream | `-q -z follow,tcp,ascii,<stream>` |

## Takeaways

- **Downloadable captures are an attack artifact, not just homework** — any pcap a box lets you fetch may contain someone's session in cleartext ([[hardcoded-credentials]]).
- Status codes inside a capture narrate the attack (a 403 followed by a 200 on the next upload shows which bypass worked) — you can reconstruct server-side filters without sending a single payload.
- `strings <pcap> | grep -E 'USER|PASS'` is the zero-learning-curve fallback when you just want credentials fast ([[cap]]).

## Seen in

- [[analyst]] — full incident reconstruction: 9 quiz answers pulled from one pcap with `tshark`, ending in an SSH password.
- [[cap]] — `strings` on a downloaded capture leaked FTP credentials (the lazy but effective variant).
