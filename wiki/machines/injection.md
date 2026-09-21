---
type: machine
platform: dockerlabs
difficulty: easy
ip: 172.17.0.2
cves: []
tools: [nmap, gobuster, curl, sqlmap]
techniques: [directory-fuzzing, sql-injection, source-code-disclosure, hardcoded-credentials]
tags: [ejpt:assessment, ejpt:web-pentest]
related: [[duque]], [[grooti]]
---

# Injection

**Writeup:** [raw writeup](../../writeups/dockerlabs/easy/injection.md)

> **⚠️ INCOMPLETE** — foothold achieved (SSH as `dylan`), but privilege escalation was **not completed**. The MySQL `root` credential (`paso`) was recovered but not yet leveraged to reach root. Treat the path below as **partial**.

Easy box: error-based SQLi on a login → sqlmap dumps `register.users` → SSH as `dylan` → `config.php` leaks MySQL root creds (unused at time of writing).

## Path (partial)

1. **Recon** — `nmap -p- -sS -sV -sC` shows `22/tcp` (OpenSSH 8.9p1), `80/tcp` (Apache 2.4.52, "Iniciar Sesión"), and `3306/tcp` (MariaDB 10.3.23, unauthorized). Note: `PHPSESSID` has `httponly flag not set`.
2. **Web enum** — [[gobuster]] finds `config.php` (size 0 — a silent DB config) and `index.php` ([[directory-fuzzing]]).
3. **SQLi auth bypass** — the login concatenates raw. Sending `'` produces a **verbose `SQLSTATE[42000]` syntax error** leaking the query shape (`... AND passwd = '...'`). `name=' OR 1=1 '` bypasses auth ([[sql-injection]]).
4. **Data extraction** — [[sqlmap]] on the `name`/`password` POST params ([[curl]] to drive) dumps DB `register` → table `users` with one row: `dylan` / `KJSDFG789FGSDF78`.
5. **SSH login** — `ssh dylan@172.17.0.2` with the dumped password.
6. **Privesc (UNFINISHED)** — standard surfaces come up clean: SUID/SGID are stock Ubuntu, `sudo` and `cron` are **not installed**, no writable system files, `mariadbd` runs as `--user=mysql` (not root). `config.php` leaks `root`/`paso` ([[source-code-disclosure]], [[hardcoded-credentials]]), but this DB credential was **not yet** turned into root.

## Credentials / secrets

| Item | Value |
|------|-------|
| `register.users` (dylan) | `KJSDFG789FGSDF78` |
| MySQL `root` (`config.php`) | `paso` |

## Open leads (for when this box is revisited)

- `paso` is **not** reused as the OS root password (`su root` / `ssh root` fail).
- `mariadbd` runs as `mysql`, so UDF `sys_exec` would land as `mysql`, not root.
- **Untested at time of writing:** `SELECT LOAD_FILE('/etc/shadow')` (DB file read), `SHOW VARIABLES LIKE 'secure_file_priv'` (file write/UDF gate), and `/var/run/docker.sock` presence (instant container escape).

## Takeaways

- A verbose `SQLSTATE` error is a gift — it leaks the query structure and confirms SQLi instantly ([[sql-injection]]).
- `config.php` returning `200` with **size 0** is the signature of a silently-included DB config ([[directory-fuzzing]], [[source-code-disclosure]]).
- Verifying `mariadbd`'s OS user (`ps aux`) matters *before* chasing a UDF path — running as `mysql` changes what `sys_exec` buys you.
- Never conclude "no escalation" until you've checked the *themed* surface (here: the DB) — not just the generic SUID/sudo/cron checklist.
