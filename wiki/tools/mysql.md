---
type: tool
category: client
related: ["[[mysql-enumeration]]"]
---

# MySQL Client

Command-line client for MySQL/MariaDB servers.

## Common usage

```sh
mysql -u user -p -h TARGET          # prompt for password
mysql -u user -pPASSWORD -h TARGET  # inline password
mysql -u user -p -h TARGET --ssl=0  # disable TLS
```

- `--ssl=0` for plaintext or when TLS negotiation fails.
- Once connected, enumerate with `SHOW DATABASES;`, `USE db;`, `SHOW TABLES;`, `DESCRIBE t;`, `SELECT …`.

## Pre-LPE recon (right after any successful login)

```sql
SHOW GRANTS;            -- EXECUTE/FILE present?
SELECT @@plugin_dir;    -- where .so files load from
CREATE FUNCTION sys_eval RETURNS STRING SONAME 'lib.so';   -- needs EXECUTE + a writable plugin_dir
```

- Pair with `ls -la <plugin_dir>` on the OS side: grants + writable dir = [[mysql-udf-lpe]] exists; either missing = it doesn't.

## Seen in

[[grooti]], [[gitea]] (placeholder `admin` login → grants/plugin_dir/perm checks → `CREATE FUNCTION … SONAME` → [[mysql-udf-lpe]])
