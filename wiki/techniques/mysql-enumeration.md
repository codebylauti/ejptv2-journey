---
type: technique
tags: [ejpt:assessment]
tools: [mysql]
cves: []
related: ["[[sql-injection]]", "[[hardcoded-credentials]]"]
---

# MySQL Enumeration

Connecting to a MySQL/MariaDB server with leaked credentials and enumerating databases, tables, columns, and data.

## Connect

```sh
mysql -u <user> -p -h TARGET --ssl=0
```

- `--ssl=0` disables TLS — needed when the server speaks plaintext or the client's TLS negotiation hangs (MySQL 8 defaults to `caching_sha2_password`).

## Enumerate

```sql
SHOW DATABASES;
USE <db>;
SHOW TABLES;
DESCRIBE <table>;        -- columns & types
SELECT * FROM <table>;   -- dump rows
```

## What to look for

- Route/path mappings (a `rutas` table mapping names → filesystem paths, as in [[grooti]]).
- Stored credentials, tokens, or hashes to reuse or crack.

## Pre-LPE checks (turn a login into a privesc path)

The moment a login works, three commands decide whether privilege escalation exists:

```sql
SHOW GRANTS;            -- EXECUTE (or FILE) present?
SELECT @@plugin_dir;    -- where MySQL loads .so files from
```
```sh
ls -la /usr/lib/mysql/plugin/    # drwxr-xrwx = world-writable write primitive
```

- Grants + plugin-dir permissions are the entire precondition set for [[mysql-udf-lpe]] — run them *before* hunting for more passwords: a login with `EXECUTE` over a writable `plugin_dir` is already a root path.
- **Dead config-file creds are data too.** Pairs cloned from a compose file may fail outright (`ERROR 1045` for both `root` and `designer` on [[gitea]]) — record the failure so nobody retries them; the service's existence is proven by its port, not by the stale password ([[hardcoded-credentials]]).

## Seen in

[[grooti]] (`files_secret.rutas` → `/unprivate/secret`), [[gitea]] (stale `root`/`designer` logins fail → placeholder-leaked `admin` connects → `SHOW GRANTS` / `@@plugin_dir` / `ls -la` pre-LPE sequence → [[mysql-udf-lpe]])
