# eJPTv2 Journey — Cybersecurity Vault

A personal, compounding knowledge base for my **eJPTv2** certification journey. Every lab and CTF machine I root gets distilled into a structured, interlinked wiki of techniques, tools, and CVEs — so knowledge builds up over time instead of being re-derived from scratch on every question.

## What this is

This vault follows the **LLM Wiki** pattern. Instead of a folder of writeups plus ad-hoc notes, an LLM agent maintains a living wiki that sits between my raw sources and my questions:

| Layer | Location | Who writes it | Role |
|-------|----------|---------------|------|
| Raw sources | `writeups/`, `assets/` | me | Immutable source of truth (CTF notes + screenshots) |
| The wiki | `wiki/` | the LLM | Structured, cross-linked synthesis (machines, techniques, tools, CVEs) |
| The schema | `AGENTS.md` | co-evolved | Tells the LLM how to structure pages and how to ingest, query, and lint |

## The LLM's role (briefly)

The LLM does the **bookkeeping**: it reads a new writeup, creates or updates the machine page, files reusable techniques/tools/CVEs, maintains cross-references, and keeps `index.md` and `log.md` current. I do the actual work — running the labs, curating sources, and asking the questions. The LLM does the summarizing, cross-referencing, and maintenance that keeps a knowledge base useful as it grows.

## Structure

```
AGENTS.md          # schema + conventions for the LLM
index.md           # content catalog — read this first
log.md             # append-only chronological record
roadmap.md         # eJPTv2 learning path + progress checklist
writeups/          # raw sources (immutable)
assets/            # images (immutable)
wiki/
├── overview.md    # synthesis of current progress
├── platforms/     # DockerLabs, TryHackMe
├── machines/      # one page per box
├── techniques/    # reusable techniques (privesc, brute force, ...)
├── tools/         # nmap, gobuster, hydra, ...
└── cves/          # CVE reference pages
```

## Credits

The structure is based on the **LLM Wiki** idea by [Andrej Karpathy](https://github.com/karpathy) — <https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f>. Thanks for the structure!
