# Cybersecurity Vault — Schema

This vault implements the **LLM Wiki** pattern: a persistent, compounding knowledge base that sits between raw source material and the user. You (the LLM) own and maintain the `wiki/` layer. The user curates sources, asks questions, and directs analysis. Write all wiki content in **English**, keeping technical terms verbatim.

## The three layers

1. **Raw sources** — `writeups/` and `assets/`. **Immutable.** Read from them, never modify them. They are the source of truth.
2. **The wiki** — `wiki/` (and `index.md`, `log.md`, `roadmap.md`). You own this entirely: create pages, update on ingest, maintain cross-references, keep consistent.
3. **The schema** — this file (`AGENTS.md`). Tells you how the wiki is structured and how to behave. Co-evolve with the user.

## Directory layout

```
AGENTS.md                 # this file
index.md                  # content catalog — read first on any query
log.md                    # append-only chronological record
roadmap.md                # eJPTv2 learning path + checklist
writeups/                 # raw sources (immutable)
  dockerlabs/{super-easy,easy,intermediate,hard}/
  tryhackme/
assets/                   # images (immutable)
wiki/
  overview.md             # synthesis of current progress
  platforms/              # dockerlabs.md, tryhackme.md
  machines/               # one page per box
  techniques/             # reusable techniques (privesc, brute force, ...)
  tools/                  # nmap, gobuster, hydra, ...
  cves/                   # CVE reference pages
```

## Page conventions

- **Filenames**: lowercase kebab-case (`los-3-hackers.md`, `cve-2011-2523.md`).
- **Links**: use Obsidian wikilinks `[[page-name]]` (no extension, no path) for wiki↔wiki links. Link to raw sources (`writeups/`, `assets/`) with a relative Markdown path, e.g. `[raw writeup](../../writeups/...)`.
- **Frontmatter** (YAML) on every page. Use the `type` to select the right schema:

```yaml
# machine
---
type: machine
platform: dockerlabs          # dockerlabs | tryhackme | ...
difficulty: super-easy        # super-easy | easy | intermediate | hard
ip: 172.17.0.2
cves: [CVE-2011-2523]         # [] if none
tools: [nmap, hydra]
techniques: [ssh-bruteforce]
tags: [ejpt:host-net-pentest] # one or more eJPT domain tags
related: [[other-page]]
---

# technique
---
type: technique
tags: [ejpt:web-pentest]
tools: [gobuster]
cves: []
related: [[directory-fuzzing]]
---

# tool
---
type: tool
category: scanner            # scanner | bruteforcer | proxy | framework | ...
related: []
---

# cve
---
type: cve
cve: CVE-2011-2523
severity: critical
year: 2011
related: [[vsftpd-backdoor]]
---

# platform
---
type: platform
difficulties: [super-easy, easy, intermediate, hard]
related: []
---
```

### eJPT domain tags

Every concept maps to one or more eJPTv2 domains. Use exactly these tags:

| Tag | Domain |
|-----|--------|
| `ejpt:assessment` | Assessment Methodologies (info gathering, scanning, enumeration) |
| `ejpt:auditing` | Host & Network Auditing |
| `ejpt:host-net-pentest` | Host & Network Penetration Testing (attacks, Metasploit, exploitation, privesc, pivoting) |
| `ejpt:web-pentest` | Web Application Penetration Testing (SQLi, XSS, file upload, ...) |

## Workflows

### Ingest (one source at a time by default)

1. Read the raw source in `writeups/` (and view any referenced images in `assets/` separately if needed).
2. Discuss key takeaways with the user; confirm what to emphasize.
3. Write/update a `wiki/machines/<name>.md` page with frontmatter + concise walkthrough, including a link back to the raw writeup directly under the title: `**Writeup:** [raw writeup](<relative path>)`.
4. Update relevant `wiki/techniques/`, `wiki/tools/`, and `wiki/cves/` pages (add the machine to their "Seen in" lists).
5. Update `wiki/platforms/<platform>.md` (append the box to its list).
6. Update `index.md` (add/refresh entries) and append an entry to `log.md`.

A single source often touches 10–15 wiki pages.

### Query

1. Read `index.md` first to locate relevant pages.
2. Read those pages; synthesize an answer **with citations** (`[[page]]` links).
3. If the answer is valuable, offer to file it back as a new wiki page (a comparison, an analysis, a new concept).

### Lint

Periodically, on request:
- Find contradictions between pages and stale claims superseded by newer sources.
- Find orphan pages (no inbound links) and missing cross-references.
- Find important concepts mentioned but lacking their own page.
- Suggest new boxes/sources to fill gaps, mapped to the eJPTv2 domains in `roadmap.md`.

## Indexing & logging

- **`index.md`** — content catalog. Every wiki page gets one line: link + one-line summary, grouped by category. Update on every ingest. Read it first on every query.
- **`log.md`** — append-only. One entry per action, starting with a parseable prefix:
  `## [YYYY-MM-DD] ingest | Machine Name`
  Actions: `ingest`, `query`, `lint`, `roadmap`, `update`.

## Output formats

Default is a markdown page. On request you may also produce: a comparison table, a Mermaid diagram, a Marp slide deck, or a matplotlib chart. The eJPTv2 study flow uses markdown pages + checklists in `roadmap.md`.
