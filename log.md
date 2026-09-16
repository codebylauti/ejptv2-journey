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
