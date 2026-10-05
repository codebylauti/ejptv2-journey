---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: [CVE-2025-55182]
tools: [nmap, curl, netcat]
techniques: [node-inspector-rce, reverse-shells, prototype-pollution]
tags: [ejpt:assessment, ejpt:host-net-pentest, ejpt:web-pentest]
related: ["[[nodeclimb]]", "[[baluhome]]"]
---

# Autoescuela

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/autoescuela.md)

Easy box that chains an exposed Node.js Inspector (V8 debugger) for the foothold, then React2Shell ([[cve-2025-55182]]) against a root-owned Next.js app for the escalation.

## Path

1. **Recon** — `nmap -p- -sS -sV -sC` shows `8080/tcp` (Node.js Express) and `9229/tcp` (unidentified). The `-p-` full sweep is what reveals 9229 — a default top-1000 scan misses it.
2. **Web** — the Express app serves index / licenses / contact form; nothing exploitable there.
3. **Node.js Inspector** — 9229 is the V8 debugger (Chrome DevTools Protocol), exposed because the app runs with `--inspect=0.0.0.0:9229`. `curl http://IP:9229/json` lists the debug target and its `webSocketDebuggerUrl` ([[node-inspector-rce]]).
4. **RCE as `webuser`** — a Python `websockets` client sends CDP `Runtime.evaluate` with `process.mainModule.require('child_process').execSync(cmd).toString()` → uid 1001 ([[node-inspector-rce]]).
5. **Reverse shell** — switch `execSync` → async `exec()` (the sync form blocks the event loop) to spawn a bash shell back to the attacker ([[reverse-shells]]).
6. **User flag** — `cat user.txt`.
7. **Privesc recon** — `ps aux` reveals a **root**-owned `npm exec next dev -p 3000 -H 127.0.0.1` (Next.js 15.0.0-rc.1) bound to loopback — invisible externally, reachable only from the foothold.
8. **React2Shell** — the internal admin portal on `localhost:3000` is vulnerable to [[cve-2025-55182]]. `exploit-redirect.sh` sends a crafted multipart `Next-Action` POST and exfiltrates output base64-encoded in the `NEXT_REDIRECT` URL → RCE as **root** ([[prototype-pollution]]).
9. **Root flag** — `cat /root/root.txt`.

## Flags / targets

| Item | Location |
|------|----------|
| user flag | `user.txt` (webuser) |
| root flag | `/root/root.txt` |

## Takeaways

- Always run a full port sweep (`-p-`); the debug port lived outside nmap's default top-1000.
- Port 9229 = Node.js Inspector. `--inspect=0.0.0.0` exposes unauthenticated CDP → instant RCE ([[node-inspector-rce]]).
- `execSync` blocks the Node event loop; use async `exec()` for long-running jobs like reverse shells ([[reverse-shells]]).
- Services bound to `127.0.0.1` are invisible from outside but a prime escalation target once you have a foothold.
- React2Shell is a single crafted POST — the `Next-Action` header is the trigger, the multipart body is the exploit ([[cve-2025-55182]]).
