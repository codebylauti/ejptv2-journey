---
type: technique
tags: [ejpt:host-net-pentest]
tools: [gtfobins]
cves: []
related: [[sudo-abuse]], [[linux-capabilities]]
---

# SUID Enumeration & Abuse

Finding setuid binaries owned by root and turning them into privilege escalation.

## Find them

```sh
find / -user root -perm -4000 -print 2>/dev/null
```

- `-perm -4000` matches the setuid bit.
- `-perm -2000` matches the **setgid** bit instead — useful for spotting group-writable directories used by privileged services (e.g. a CI runner's `builds_dir` in [[pipepwned]]).
- Cross-reference unusual *known* binaries (`vim`, `ruby`, `pkexec`, `env`, …) against [[gtfobins]] — **editors are instant wins**: a SUID `nano`/`vim` can edit `/etc/passwd` directly ([[writable-etc-passwd]], [[domain]]).
- The same rule in general: **any SUID binary that writes files *where you say* is a write primitive** — not just editors. SUID `curl` does it with `file://` in and `-o` out ([[writable-etc-passwd]], [[chmod-4755]]); SUID `dos2unix` with `-f -n` ([[bruteshock]]). Read `--help` for the write flags.

## Custom SUID binaries — reverse-engineer the trigger

A box may ship its *own* SUID binary (not in GTFOBins). Reverse-engineer it:

```sh
file ./binary
strings ./binary        # hardcoded strings: password, banner, paths, error text
objdump -d ./binary     # disassembly — find the strcmp / setuid / system pattern
ltrace ./binary foo     # live library calls, e.g. strcmp("foo", "REALPASS")
```

The classic shape:

```c
setuid(0); setgid(0);
if (strcmp(argv[1], "KEY") == 0) system("/bin/bash");
```

## Seen in

[[trust]] (`sudo vim`), [[ignite]] (SUID scan), [[wargames]] (`godmode --wopr` → root shell), [[duque]] (`env /bin/sh -p` → root shell), [[walkingcms]] (`env /bin/sh -p` → root shell), [[trailpack]] (`env /bin/sh -p` → root shell), [[madeyes-castle]] (`/srv/time-turner/swagger` → `system("uname -p")` → [[path-hijacking]]), [[acme]] (`/usr/bin/bash -p` — a SUID *shell* itself, the fastest possible find), [[internal]] (`/usr/local/bin/vaultctl` — custom SUID that drops straight to root when the *right user* runs it, so pair the find with a credential hunt), [[domain]] (`/usr/bin/nano` → edit `/etc/passwd` → [[writable-etc-passwd]]), [[chmod-4755]] (`/usr/bin/curl` — a non-editor SUID *file writer*, the box's namesake `chmod 4755`), [[dark]] (`/usr/bin/curl` again — same platform, same primitive: you've already written the payload down, don't re-derive it)
