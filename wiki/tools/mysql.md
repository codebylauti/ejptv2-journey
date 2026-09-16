---
type: tool
category: client
related: [[mysql-enumeration]]
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

## Seen in

[[grooti]]
