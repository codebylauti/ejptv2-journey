---
type: technique
tags: [ejpt:assessment]
tools: [mysql]
cves: []
related: [[sql-injection]], [[hardcoded-credentials]]
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

## Seen in

[[grooti]] (`files_secret.rutas` → `/unprivate/secret`)
