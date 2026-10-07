---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: ["[[sudo-abuse]]"]
---

# Python Library Hijacking

Abusing a `sudo python3 /path/script.py` entry when you can't write the script but *can* write a directory in Python's import path.

## Concept

- Python searches the script's own directory (`sys.path[0]`) **before** the standard library.
- Drop a module named after one the script imports, and Python imports **yours** — executing it as root.
- The script's file mode is a red herring: `-r-xr--r--` changes nothing, because the payload never opens the script for writing. The check that matters is `ls -la` on the **parent directory** — ownership and mode both ([[library]]).

## Critical caveat

- `os` and `sys` are **already imported at interpreter startup** (cached in `sys.modules`), so `import os` never touches the filesystem → can't be shadowed.
- Lazily-imported modules (`subprocess`, `time`, third-party libs) are fair game.

## Workflow

1. Read the script (`cat /opt/script.py`) and note its imports.
2. Pick a lazily-imported module (e.g. `subprocess`).
3. `echo 'import os; os.execl("/bin/sh", "sh")' > /opt/subprocess.py`.
4. `sudo python3 /opt/script.py` → your module runs as root.

## Seen in

[[psycho]] (shadow `subprocess`, not `os`), [[library]] (shadow `shutil` — script `-r-xr--r--`, but `/opt` is carlos-owned)
