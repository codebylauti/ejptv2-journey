# Log

Append-only chronological record. Parseable prefix: `## [YYYY-MM-DD] action | Subject`.

## [2026-09-14] roadmap | Vault bootstrap

Created the LLM Wiki vault: schema (`AGENTS.md`), directory layout, `index.md`, `log.md`, `roadmap.md`, and the full `wiki/` tree.

## [2026-09-14] ingest | DockerLabs super-easy batch

Ingested 8 super-easy boxes: [[breakmyssh]], [[first-hacking]], [[hedgehog]], [[trust]], [[tproot]], [[obsession]], [[vacaciones]], [[borazuwara]].

## [2026-09-14] ingest | DockerLabs easy/intermediate/hard batch

Ingested [[los-3-hackers]] (easy), [[adopting]] (intermediate), [[baluhome]] (hard).

## [2026-09-14] ingest | TryHackMe batch

Ingested 4 rooms: [[basic-pentesting]], [[simple-ctf]], [[ignite]], [[guided-pentest]].

## [2026-09-14] ingest | Cross-cutting pages

Created 18 technique pages, 8 tool pages, 4 CVE pages, and 2 platform pages; populated `index.md` and wrote [[overview]].

## [2026-09-14] ingest | DockerLabs easy — Hannah Coffee

Ingested [[hannah-coffee]] (easy). Added technique pages [[local-file-inclusion]], [[log-poisoning]], [[parameter-fuzzing]] and tool pages [[ffuf]], [[dirb]]. Updated [[sudo-abuse]], [[gtfobins]], [[linux-capabilities]], [[reverse-shells]], [[directory-fuzzing]], [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-14] ingest | DockerLabs easy — Balufood

Ingested [[balufood]] (easy). Added technique page [[hardcoded-credentials]]. Updated [[source-code-disclosure]], [[directory-fuzzing]], [[dirb]], [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-14] ingest | DockerLabs easy — Balulero

Ingested [[balulero]] (easy). Added technique page [[group-ownership-enumeration]]. Updated [[source-code-disclosure]], [[sudo-abuse]], [[cron-job-abuse]], [[reverse-shells]], [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-14] ingest | DockerLabs easy — Nodeclimb

Ingested [[nodeclimb]] (easy). Added technique page [[zip-cracking]]. Updated [[ftp-anonymous-login]], [[sudo-abuse]], [[john-the-ripper]], [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-15] ingest | DockerLabs easy — Psycho

Ingested [[psycho]] (easy). Added technique page [[python-library-hijacking]]. Updated [[local-file-inclusion]], [[parameter-fuzzing]], [[sudo-abuse]], [[directory-fuzzing]], [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-15] lint | Vault lint pass

No broken wikilinks, no orphan pages. Fixed stale eJPT domain coverage in `roadmap.md` and `overview.md`, added `ejpt:assessment` tag to [[parameter-fuzzing]], refreshed the password-cracking gap note. Flagged missing tool pages ([[netcat]], searchsploit, telnet) and writeup filename typos (`hegdgehog`, `break-my-ssh`, `borazuwara-ctf`).

## [2026-09-15] update | Add netcat tool page

Created [[netcat]] tool page (reverse-shell listener) and added it to `index.md`.

## [2026-09-15] ingest | DockerLabs easy — Autoescuela

Ingested [[autoescuela]] (easy). Added technique pages [[node-inspector-rce]] and [[prototype-pollution]], CVE page [[cve-2025-55182]], and tool page [[curl]]. Updated [[reverse-shells]], [[nmap]], [[netcat]], [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-15] ingest | DockerLabs easy — Wargames

Ingested [[wargames]] (easy). Added technique pages [[prompt-injection]] and [[hash-cracking]]; expanded [[suid-enumeration]] with custom-SUID-binary reverse-engineering. Updated [[netcat]], [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-16] lint | Vault lint pass

No broken wikilinks or orphan pages among `wiki/` pages (all 29 techniques, 12 tools, 5 CVEs, 22 machines, 2 platforms are indexed). Fixed two issues in [[overview]]: stale "only SSH keys and ZIP archives" password-cracking gap (now [[hash-cracking]] via [[wargames]] is covered, `/etc/shadow`/NTLM still untried) and removed the mis-categorized [[log-poisoning]] from the Host & Network row. Flagged, for review: (1) `tools:` frontmatter lists 12 entries with no page — `telnet`/`searchsploit` (previously flagged, still uncreated) plus interpreter/utility binaries `ftp`, `php`, `node`, `perl`, `python3`, `strings`, `objdump`; (2) [[source-code-disclosure]] "Seen in" omits [[guided-pentest]] and lists non-referencing [[los-3-hackers]]/[[simple-ctf]]; (3) writeup filename typos persist (`hegdgehog`, `break-my-ssh`, `borazuwara-ctf`, `balu-home`, `guided-pentest-infraestructure`) and malformed `[[https://…]]`/`[[IP]]` links in writeups — all immutable raw sources.

## [2026-09-16] update | Lint fixes

Created tool pages [[telnet]] and [[searchsploit]] (previously flagged missing) and added them to `index.md`. Adopted the convention that `tools:` frontmatter only lists entries with a `wiki/tools/` page: removed the abused interpreters/utilities (`ftp`, `php`, `node`, `perl`, `python3`, `strings`, `objdump`, `ltrace`) from the `tools:` field of [[tproot]], [[obsession]], [[balulero]], [[nodeclimb]], [[psycho]], [[autoescuela]], [[wargames]], [[ftp-anonymous-login]], [[log-poisoning]], [[node-inspector-rce]], and [[suid-enumeration]] (their usage remains documented in the technique bodies). Reconciled [[source-code-disclosure]] cross-references: added it to the `techniques:` of [[los-3-hackers]] and [[simple-ctf]], and added [[guided-pentest]] to its "Seen in" list. Backfilled incomplete "Seen in" lists on the [[gobuster]], [[ffuf]], [[dirb]], and [[curl]] tool pages.

## [2026-09-16] update | Link machine pages to raw writeups

Added a `**Writeup:** [raw writeup](<relative path>)` link to all 22 machine pages, pointing each to its corresponding raw writeup in `writeups/`. Documented the convention in `AGENTS.md` (wiki↔wiki links use wikilinks; links to raw sources use relative Markdown paths).

## [2026-09-16] ingest | DockerLabs easy — Grooti

Ingested [[grooti]] (easy). Added technique pages [[mysql-enumeration]] and [[value-brute-force]], and tool page [[mysql]]. Updated [[source-code-disclosure]], [[hardcoded-credentials]], [[directory-fuzzing]], [[ssh-bruteforce]], [[cron-job-abuse]], [[reverse-shells]], [[gobuster]], [[curl]], [[hydra]], [[netcat]], [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-16] ingest | DockerLabs easy — Winfake

Ingested [[winfake]] (easy). Added technique page [[acrostic-decoding]]. Updated [[source-code-disclosure]] (CSS-property/hidden-attribute vector), [[hardcoded-credentials]] (weak root password), [[ssh-bruteforce]], [[information-gathering]] (banner-spoofing correlation note), and tool pages [[hydra]], [[curl]], [[gobuster]]. Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-16] lint | Vault lint pass

Cross-reference scan (mechanical + semantic) after [[winfake]]: 903 `[[...]]` occurrences across 80 distinct targets → **0 broken wikilinks, 0 orphan pages** (all 79 wiki pages indexed + inbound-linked). Frontmatter: all `tools:`/`techniques:` values map to a real page, all `type:` values valid. All 24 machine `**Writeup:**` links resolve (typo'd raw filenames `hegdgehog`, `break-my-ssh`, `borazuwara-ctf`, `balu-home`, `guided-pentest-infraestructure` are correctly mirrored). Fixed two stale `roadmap.md` "Covered" lists — added [[mysql-enumeration]] (Assessment) and [[value-brute-force]] (Web Pentest) to match [[overview]]. Noted, no fix (immutable/raw): 1 malformed `[[#IP]]` link in `writeups/tryhackme/basic-pentesting.md`; 2 unreferenced images in `assets/` (`…231453.png`, `…231520.png`).

## [2026-09-16] update | Ignore .obsidian

Expanded `.gitignore` to ignore `.obsidian/` wholesale and untracked its 7 files (`app.json`, `appearance.json`, `core-plugins.json`, plus Catppuccin & Omarchy `manifest.json`/`theme.css`) so per-machine Obsidian state stops polluting commits.

## [2026-09-18] ingest | DockerLabs easy — Duque

Ingested [[duque]] (easy). Added tool page [[sqlmap]]. Updated [[sql-injection]] (time-based blind + file-read variants), [[source-code-disclosure]] (SQLi file-read vector), [[suid-enumeration]] + [[gtfobins]] (`env /bin/sh -p`), [[hardcoded-credentials]] (source-embedded creds), [[directory-fuzzing]], and tool pages [[gobuster]], [[curl]]. Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-18] ingest | DockerLabs easy — Injection (INCOMPLETE)

Ingested [[injection]] (easy) as **incomplete** — foothold reached (SSH as `dylan`) but privesc not solved. Marked the machine page, [[dockerlabs]], and `index.md` entries as ⚠️ incomplete. Updated [[sql-injection]] (error-based + verbose `SQLSTATE` variant), [[directory-fuzzing]] (`config.php` size-0 find), [[source-code-disclosure]] + [[hardcoded-credentials]] (MySQL `root:paso` in `config.php`), and tool pages [[sqlmap]], [[gobuster]], [[curl]]. Not counted toward the completed-box total in [[overview]].

## [2026-09-18] ingest | DockerLabs easy — WalkingCMS

Ingested [[walkingcms]] (easy). Added technique page [[wordpress-enumeration]] and tool page [[wpscan]]. Updated [[directory-fuzzing]] (`wordpress/` behind default page), [[reverse-shells]] (theme-editor PHP shell), [[suid-enumeration]] + [[gtfobins]] (`env /bin/sh -p`), and tool pages [[ffuf]] (directory fuzz usage), [[gobuster]]. Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-18] lint | Vault lint pass

Cross-reference scan after [[walkingcms]]: **0 broken wikilinks, 0 orphan pages** — all new pages ([[walkingcms]], [[wpscan]], [[wordpress-enumeration]]) are inbound-linked from `index.md`, [[dockerlabs]], and their parent pages. Frontmatter valid: `tools:`/`techniques:` values all map to real pages, `type:` values valid. Noted, no fix (immutable/raw): `writeups/dockerlabs/easy/walkingcms.md` references `![[Pasted image 20260918145030.png]]` (the "user mario" screenshot) which is **not** in `assets/` — same class of unreferenced-image issue as the Duque writeup.

## [2026-09-20] ingest | DockerLabs easy — Anonymous Pingu

Ingested [[anonymous-pingu]] (easy). Added technique page [[web-shell-upload]]. Updated [[sudo-abuse]] (man/nmap/chown payloads), [[writable-etc-passwd]] (`sudo chown` vector + blank-root method), [[ftp-anonymous-login]] (write/upload), [[reverse-shells]], [[directory-fuzzing]] (`upload/` find), and tool pages [[nmap]] (NSE `--script` escape), [[gobuster]], [[netcat]], [[gtfobins]] (man/nmap/chown payloads). Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-22] ingest | DockerLabs intermediate — PipePwned

Ingested [[pipepwned]] (intermediate). Added technique pages [[server-side-template-injection]] and [[ci-cd-pipeline-abuse]]. Updated [[source-code-disclosure]] (SSTI file-read vector), [[hardcoded-credentials]] (CI trace + `.env` leak), [[directory-fuzzing]] (`/api/jobs/{id}/trace` + `/api/pipelines`), [[suid-enumeration]] (setgid `-2000` note), and tool pages [[curl]], [[ffuf]], [[gobuster]], [[dirb]]. Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-23] ingest | DockerLabs intermediate — TrailPack

Ingested [[trailpack]] (intermediate). Added technique pages [[mfa-bruteforce]], [[broken-access-control]], and [[command-injection]]. Updated [[session-and-cookie-abuse]] (base64 role-cookie vector), [[source-code-disclosure]] (post-exploit `main.py` read), [[hardcoded-credentials]] (in-memory `USERS` table), [[reverse-shells]] (base64 `sh -i` via command injection), [[suid-enumeration]] + [[gtfobins]] (`env /bin/sh -p`), and tool pages [[burp-suite]], [[curl]], [[gobuster]], [[netcat]]. Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-23] ingest | DockerLabs intermediate — BruteShock

Ingested [[bruteshock]] (intermediate). Added technique pages [[shellshock]], [[http-login-bruteforce]], [[arithmetic-injection]], and [[exim-lpe]], plus CVE page [[cve-2014-6271]]. Updated [[hash-cracking]] (crypt(3) yescrypt `$y$` + `--format=crypt`), [[writable-etc-passwd]] (sudo `dos2unix -f -n` overwrite), [[sudo-abuse]] (arithmetic-injection/exim/dos2unix payloads), [[reverse-shells]] (`nohup` detach note), [[hardcoded-credentials]] (backup shadow-hash leak), and tool pages [[john-the-ripper]], [[hydra]], [[gtfobins]], [[curl]], [[gobuster]], [[netcat]]. Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-25] ingest | DockerLabs intermediate — LittlePivoting

Ingested [[littlepivoting]] (intermediate) — the vault's first multi-host pivoting lab. Added technique pages [[pivoting]], [[port-forwarding]], [[su-brute-force]], and [[metasploit-pivoting]], plus tool pages [[chisel]], [[proxychains]], and [[ssh]]. Updated [[metasploit]] (pivoting workflow: `route`/`autoroute`/`portfwd`/`shell_to_meterpreter`), [[local-file-inclusion]] (`?archivo=` vector), [[ssh-bruteforce]], [[sudo-abuse]] (php/vim/env payloads), [[reverse-shells]] (bash over pivot + pentestmonkey PHP), [[web-shell-upload]], [[directory-fuzzing]] (`shop/`, `secret.php`), and [[information-gathering]] (host/network discovery via `ip a`/`ip route`/`nmap -sn`), plus tool pages [[nmap]] (`-sn`), [[gobuster]], [[ffuf]], [[hydra]], [[curl]], [[gtfobins]] (php/vim/env). Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]] (pivoting gap now covered; manual chisel/proxychains flagged as next).

## [2026-09-26] ingest | TryHackMe — Madeye's Castle

Ingested [[madeyes-castle]] (easy). Added technique pages [[virtual-hosting]] and [[path-hijacking]]. Updated [[sql-injection]] (SQLite UNION: `sqlite_master` + `group_concat` via JSON error reflection), [[hash-cracking]] (`--rules=best64` mangling), [[smb-enumeration]] (smbmap/smbclient anon share + hidden `.notes.txt`), [[sudo-abuse]] (`pico` `^R^X` escape), [[suid-enumeration]] (custom SUID `swagger` → PATH hijack), [[directory-fuzzing]], and tool pages [[sqlmap]] (why it failed on SQLite UNION: NULL/JSON reflection/DBMS pin), [[gobuster]], [[hydra]] (`smb2`), [[john-the-ripper]] (`--rules=best64`). Updated [[tryhackme]], `index.md`, `roadmap.md`, and [[overview]].

## [2026-09-28] ingest | DockerLabs intermediate — LittlePivoting (manual re-run)

Ingested `writeups/dockerlabs/intermediate/little-pivoting-manual.md` — a second run of the already-ingested [[littlepivoting]], this time fully manual (chisel reverse SOCKS + socat relays + proxychains, no Metasploit, no root at any hop). Per schema, one page per box: extended [[littlepivoting]] with the second writeup link, a "manual re-run" path, and new takeaways. Added tool page [[socat]]. Updated [[pivoting]] (socat relay back-path, tool-drop-in + stacked-SOCKS gotchas), [[port-forwarding]] (socat static relay), [[chisel]] and [[proxychains]] (both no longer "not yet exercised" — real commands + stacking from the run), [[reverse-shells]] (hop-by-hop socat callback chain), [[information-gathering]] (`arp-scan`, ping-sweep one-liner), and tool pages [[nmap]] (`-sT` via SOCKS), [[gobuster]] (`--proxy`), [[hydra]]/[[ssh]] (`proxychains` wrapping). Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]] (manual chisel/proxychains gap closed; SSH `-D`/`-L`/`-R` remains).

## [2026-09-28] lint | Vault lint pass

Cross-reference scan after the [[littlepivoting]] manual re-run (code-stripped, so bash `[[ $num -eq ]]` examples don't false-positive): **0 broken wikilinks, 0 orphan pages** — 112 wiki pages, all indexed in `index.md` and inbound-linked; all `tools:`/`techniques:` frontmatter values map to real pages; all 34 machine `**Writeup:**` links resolve (including the new dual-writeup line). Stale claims fixed in the ingest pass: [[overview]]/[[roadmap]]/[[port-forwarding]] no longer say chisel/proxychains are "not yet exercised" — remaining gap is SSH `-D`/`-L`/`-R`. Flagged, no fix (immutable/raw): `![[Pasted image 20260925151635.png]]` referenced by both littlepivoting writeups is not in `assets/` (27 images stored); typos in the new writeup (`sockat`, `Porsts scanning`). Flagged for review: `arp-scan` now used on a box ([[information-gathering]]) but has no `wiki/tools/` page.

## [2026-09-28] update | Add arp-scan tool page; fix raw writeup typos

Created [[arp-scan]] tool page (L2 same-subnet sweep vs `nmap -sn` comparison) and indexed it; linked it from [[information-gathering]] and added it to the `tools:` frontmatter of [[littlepivoting]] — closes the flag raised in the previous lint pass. Also fixed two typos in the raw source `writeups/dockerlabs/intermediate/little-pivoting-manual.md` (`sockat` → `socat`, `Porsts` → `Ports`): first deliberate edit to an immutable source, made on request — the two `![[Pasted image …]]`/image gap remains untouched.

## [2026-09-28] lint | Correction — false-positive image gap

Retracting the "missing image" flag from the [[littlepivoting]] manual-run ingest and lint entries: `![[Pasted image 20260925151635.png]]` **does** exist in `assets/` — the check grepped file *contents* instead of filenames, so the binary PNG never matched. Verified properly: 27 unique image references across `writeups/` ↔ 27 files in `assets/`, **0 missing**. Real (minor) finding instead: 3 **unreferenced** assets — `Pasted image 20260910231453.png`, `Pasted image 20260910231520.png`, `Pasted image 20260922171335.png`. Takes the place of the earlier "2 unreferenced images" note from 2026-09-16.

## [2026-09-28] ingest | TryHackMe — Madeye's Castle (root flag confirmed)

Re-ingested `writeups/tryhackme/madeyes-castle.md` after the raw source's `Root.txt` objective was ticked `[x]` — the wiki already documented the full path to root ([[madeyes-castle]] step 8), so this reconciles source and wiki rather than adding a new stage. Incremental captures missed on 2026-09-26: [[sqlmap]] `--code=403` (custom "injection worked" status) + `--technique=B`; a dead-end **login-form user enumeration** oracle (script waiting for 403, every username returned 200) noted on [[sql-injection]] and as a machine takeaway; `authorized_keys` persistence noted via [[ssh]].

## [2026-09-28] lint | Vault lint pass

After the [[madeyes-castle]] re-ingest: **0 broken wikilinks, 0 orphan pages, 0 frontmatter issues, 0 broken writeup links**, all 113 wiki pages indexed. Image audit re-run by filename (not contents): 27 refs ↔ 27 assets, 0 missing, 3 unreferenced (see correction entry above).

## [2026-09-29] ingest | DockerLabs super-easy — ACME

Ingested [[acme]] (super-easy): ping + `nmap -sS -sC -sV -p-` (22/80, `http-robots.txt` → `/migration_notes.txt`) → SSH **pre-auth MOTD credential disclosure** (`usuario` / `P@ssw0rd2026_CTF!`, no brute-force) → SUID `/usr/bin/bash -p` → root. Updated technique pages [[hardcoded-credentials]] (banner/MOTD vector) and [[suid-enumeration]] (SUID shell find), plus tool pages [[nmap]] (`http-robots.txt` in `-sC`) and [[ssh]] (banner/MOTD enumeration). Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]] (33 boxes / 28 DockerLabs). Flags: (1) `![[Pasted image 20260929155414.png]]` referenced by the raw writeup has no matching file in `assets/` (27 images checked by filename) — immutable source, not touched; (2) per user decision, the root flag's `wp2shell_cve_2026_63030` string is deliberately **not** documented (the writeup never exploits it) — do not re-flag as a missing CVE page.

## [2026-09-29] ingest | DockerLabs easy — Internal

Ingested [[internal]] (easy): 303 `Location:` leak → `internal.dl` → `gobuster vhost` → `backup.internal.dl` → blacklist-WAF directory inspector → split-string command injection (`\whoam\i`, `ba's'h`) → bash reverse shell → `/opt/.vault_pass.txt` wordlist + hydra `vault:Yk8$pZ5@cN4!` → SUID `vaultctl` → root. Added technique page [[waf-bypass]] (exact-string blacklist detection + quote/backslash splitting). Updated [[command-injection]] (WAF section + seen-in), [[virtual-hosting]] (303 hostname leak, `gobuster vhost --append-domain --xs 303`), [[information-gathering]] (status-line recon), [[suid-enumeration]] (custom `vaultctl`), [[hardcoded-credentials]] (on-box password file), [[ssh-bruteforce]] (found wordlist beats rockyou), [[reverse-shells]] (quote-split bash payload), and tool pages [[gobuster]] (vhost mode), [[hydra]], [[curl]]. Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]] (34 boxes / 29 DockerLabs). Note: `![[Pasted image 20260929170245.png]]` exists in `assets/` (checked by filename).

## [2026-09-29] lint | Vault lint pass

After the [[internal]] ingest (code + inline-code stripped to avoid bash `[[ $num -eq ]]` false positives): **0 broken wikilinks, 0 frontmatter issues** (`tools:`/`techniques:`/`related:` all resolve; `cves:` values map to `wiki/cves/` pages), **0 orphan pages** (116 wiki pages, all indexed in `index.md` and inbound-linked), **0 machine registry gaps** — 35 machine pages ↔ 34 roadmap `[x]` + 1 `[ ]` ([[injection]]), headline **34 boxes / 29 DockerLabs** matches per-difficulty ticks (super-easy 9, easy 14+1 open, intermediate 5, hard 1, THM 5). All 35 machine `**Writeup:**` links resolve (incl. [[littlepivoting]]'s plural `**Writeups:**` dual-link). Image audit by filename: 26 refs ↔ 29 assets, **0 missing**, 3 unreferenced (unchanged: `Pasted image 20260910231453.png`, `20260910231520.png`, `20260922171335.png`). Stale-claim scan: only intentional remaining-gap notes (SSH `-D`/`-L`/`-R`, SSRF/CSRF, OS-hash cracking) — still accurate.

## [2026-09-30] ingest | Hack The Box — Cap

First Hack The Box box: created platform page [[hack-the-box]] and machine page [[cap]] (easy, 10.129.148.255) — ping/TTL recon → `nmap -sS -p- --open` (21/22/80, vsftpd 3.0.3 + OpenSSH 8.2p1 + Gunicorn "Security Dashboard") → `whatweb` + `gobuster` (`capture` 302 → `/data/1` object-ID leak) → IDOR on `/data/<id>`/`/download/<id>` (ffuf `3-digits-000-999.txt`, `-fc 302`) → `strings` on downloaded pcap `0` → FTP/SSH `nathan:Buck3tH4TF0RM3!` → `user.txt` → `getcap -r /` finds `/usr/bin/python3.8 = cap_setuid,cap_net_bind_service+eip` → `os.setuid(0)` one-liner → root. No new technique/tool/CVE pages (per user decision: pcap extraction folded into [[hardcoded-credentials]] as a cleartext-capture vector; `whatweb` noted in [[information-gathering]] only, no tool page). Updates: [[broken-access-control]] (new **IDOR** section — fixes a stale roadmap claim that IDOR was already covered), [[linux-capabilities]] (system-Python one-liner + seen-in), [[hardcoded-credentials]] (pcap vector), [[directory-fuzzing]] (key finds + seen-in), [[information-gathering]] (whatweb fingerprint step), tool pages [[gobuster]], [[ffuf]] (ID-space sweep), [[ssh]] (cred replay). Updated [[index]] platform/machine/technique entries, `roadmap.md` (new **Hack The Box** checklist, 35 boxes / 3 platforms, whatweb gap partially closed), and [[overview]].

## [2026-10-02] ingest | DockerLabs easy — Flynn

Ingested [[flynn]] (easy): `nmap -p- --open -sS -sCV --min-rate 5000` (22 OpenSSH 10.2p1 / 80 Apache 2.4.66) → SSH **default credentials** `flynn:flynn` (username = password, no brute-force) → `sudo -l` → `(ALL) NOPASSWD: /usr/bin/env` → `sudo /usr/bin/env /bin/sh -p` → root. Updated [[hardcoded-credentials]] (new **default/weak service credentials** vector — try username-as-password before rockyou), [[sudo-abuse]] (`env` payload variant + seen-in), and tool pages [[nmap]], [[ssh]]. Updated [[dockerlabs]], `index.md`, `roadmap.md`, and [[overview]] (36 boxes / 30 DockerLabs).

## [2026-10-02] ingest | DockerLabs easy — Analyst

Ingested [[analyst]] (easy), a blue-team/forensics box: `nmap` (22 OpenSSH 10.0p2 Debian / 80 Gunicorn "El caso de Pinguinito — Lab Blue Team") → `curl` the incident artifacts (`threat_intel_feed.json` + `incidente_pinguino.pcap` from `/descargas/`) → **9-question incident quiz answered entirely from the pcap with `tshark`** (`http.request.method==POST` filter → attacker `198.51.100.23` correlated with the threat-intel feed → Vietnam; UA/URI extraction via `-T fields … | sort -u`; `-z follow,tcp,ascii` on the upload streams showing `shell.php` 403 vs `image.jpg.php` 200; reverse-shell SYN to port 8080 + `cat /etc/passwd`; password-reset line leaking `pinguinito:Tr0pic4l-Pingu_99!`) → SSH with the captured password → `(ALL) NOPASSWD: ALL` → `sudo -u root /bin/bash -p` → root. **New pages:** technique [[pcap-analysis]] and tool [[tshark]] — unlike [[cap]], where pcap use was incidental (folded into [[hardcoded-credentials]]), here traffic analysis *is* the box's entire attack path, so it earns its own page; `tshark` likewise (vs. `whatweb`, which stayed out of `wiki/tools/`). Updated [[hardcoded-credentials]] (pcap bullet now includes the operational-message/reset-vector + seen-in), [[sudo-abuse]] (unrestricted-sudo bullet + seen-in), tool pages [[curl]] and [[ssh]], and [[cap]] (cross-linked [[pcap-analysis]]). Updated [[dockerlabs]], `index.md`, `roadmap.md` (37 boxes / 31 DockerLabs, `pcap-analysis` in Assessment coverage, auditing gap partially closed — CLI capture analysis done, `tcpdump`/Wireshark GUI still open), and [[overview]].

## [2026-10-02] lint | Vault lint pass

After the [[flynn]] + [[analyst]] ingests (fenced/inline code stripped to avoid bash `[[ $num -eq ]]` false positives): **0 broken wikilinks, 0 frontmatter issues** (`tools:`/`techniques:`/`related:` all resolve; `cves:`/`platform:` map to real pages), **0 orphan pages** (122 wiki pages — every one indexed in `index.md` and inbound-linked), **0 machine registry gaps** — 38 machine pages ↔ 37 roadmap `[x]` + 1 `[ ]` ([[injection]]); headline **37 boxes / 31 DockerLabs** matches the per-section ticks (super-easy 9, easy 16+1 open, intermediate 5, hard 1, THM 5, HTB 1) and the per-platform frontmatter counts (dockerlabs 32 incl. injection, THM 5, HTB 1). All 38 machine `**Writeup:**` links resolve. Image audit by filename: 26 refs ↔ 29 assets, **0 missing**, 3 unreferenced (unchanged trio: `Pasted image 20260910231453.png`, `20260910231520.png`, `20260922171335.png`). **Retraction:** the [[acme]] ingest flag that `![[Pasted image 20260929155414.png]]` had no matching file in `assets/` is withdrawn — the file is now present (arrived as an untracked asset; verified by filename, same class of mistake as the 2026-09-28 correction). Stale-claim scan clean outside `log.md` (append-only history). Remaining intentional gaps unchanged: SSH `-D`/`-L`/`-R` documented but unexercised, SSRF/CSRF unseen, OS-hash cracking untried, `tcpdump`/Wireshark GUI untried (CLI capture analysis now covered via [[pcap-analysis]]/[[tshark]]).
