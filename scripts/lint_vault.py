#!/usr/bin/env python3
"""Vault lint: YAML, links, registries, parity, dup stems, assets, stale counts."""
import re, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("pyyaml missing")

ROOT = Path(__file__).resolve().parents[1]
WIKI = ROOT / "wiki"
errors, warnings = [], []

wiki_pages = sorted(WIKI.rglob("*.md"))
link_files = wiki_pages + [ROOT / "index.md", ROOT / "log.md", ROOT / "roadmap.md"]

def read(p): return p.read_text(encoding="utf-8")

def strip_code(t):
    t = re.sub(r"````.*?````", "", t, flags=re.S)
    t = re.sub(r"```.*?```", "", t, flags=re.S)
    t = re.sub(r"``[^`\n]*``", "", t)
    t = re.sub(r"(?<!`)`[^`\n]+`(?!`)", "", t)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    return t

LINK = re.compile(r"(?<!!)\[\[([^\]|#]+)(?:\|[^\]]+)?\]\]")

# --- 1. strict YAML frontmatter ---
fm_data = {}
for p in wiki_pages:
    t = read(p)
    m = re.match(r"^---\n(.*?)\n---\n", t, re.S)
    if not m:
        warnings.append(f"no frontmatter: {p.relative_to(ROOT)}"); continue
    try:
        fm_data[p] = yaml.safe_load(m.group(1))
    except Exception as e:
        errors.append(f"YAML PARSE {p.relative_to(ROOT)}: {e}")

all_wiki = {p.stem for p in wiki_pages} | {"index", "log", "roadmap"}
tool_pages = {p.stem for p in (WIKI / "tools").glob("*.md")}
tech_pages = {p.stem for p in (WIKI / "techniques").glob("*.md")}
machine_pages = {p.stem for p in (WIKI / "machines").glob("*.md")}
platform_pages = {p.stem for p in (WIKI / "platforms").glob("*.md")}

# --- 2. frontmatter refs resolve ---
for p, d in fm_data.items():
    if not isinstance(d, dict): continue
    rel = str(p.relative_to(ROOT))
    cve_pages = {p.stem.upper() for p in (WIKI / "cves").glob("*.md")}
    for key, valid in (("tools", tool_pages), ("techniques", tech_pages), ("cves", cve_pages)):
        for v in (d.get(key) or []):
            vv = v.upper() if key == "cves" else v
            if vv not in valid: errors.append(f"FM {rel}: {key} -> '{v}' missing")
    for v in (d.get("related") or []):
        m = re.fullmatch(r"\[\[([^\]]+)\]\]", str(v))
        if not m: errors.append(f"FM {rel}: related not a wikilink: {v}")
        elif m.group(1) not in all_wiki: errors.append(f"FM {rel}: related -> {m.group(1)} missing")
    if d.get("platform") and d["platform"] not in platform_pages:
        errors.append(f"FM {rel}: platform -> {d['platform']} missing")

# --- 3. wikilinks resolve + inbound set ---
inbound = set()
for p in link_files:
    t = re.sub(r"!\[\[[^\]]*\]\]", "", strip_code(read(p)))
    for m in LINK.finditer(t):
        tgt = m.group(1).strip(); inbound.add(tgt)
        if tgt not in all_wiki:
            errors.append(f"BROKEN LINK {p.relative_to(ROOT)}: [[{tgt}]]")

orphans = sorted(n for n in (p.stem for p in wiki_pages) if n not in inbound and n != "index")
warnings += [f"ORPHAN: {n}" for n in orphans]

# --- 4. index membership ---
idx = strip_code(read(ROOT / "index.md"))
idx_links = set(LINK.findall(idx))
for m in sorted(machine_pages):
    if m not in idx_links: errors.append(f"INDEX: machine {m} missing")
missing_tech = sorted(t for t in tech_pages if t not in idx_links)
warnings += [f"INDEX: technique missing: {t}" for t in missing_tech]

# --- 5. roadmap registry ---
rm = read(ROOT / "roadmap.md")
sec = ""
if "## Completed boxes" in rm:
    sec = re.split(r"\n## ", rm.split("## Completed boxes", 1)[1])[0]
checked = re.findall(r"^- \[x\] \[\[([^\]]+)\]\]", sec, re.M)
opened = re.findall(r"^- \[ \] \[\[([^\]]+)\]\]", sec, re.M)
reg = set(checked) | set(opened)
if machine_pages != reg:
    errors.append(f"REGISTRY: pages-only={sorted(machine_pages - reg)} roadmap-only={sorted(reg - machine_pages)}")
hm = re.search(r"\*\*(\d+) boxes done\*\*", rm)
if hm and int(hm.group(1)) != len(checked):
    errors.append(f"HEADLINE: '{hm.group(1)} boxes done' vs {len(checked)} [x]")

# per-platform counts from machine frontmatter vs overview vs platform pages
def plat_of(stem):
    d = fm_data.get(WIKI / "machines" / f"{stem}.md", {})
    return d.get("platform") if isinstance(d, dict) else None

ov = read(WIKI / "overview.md")
m = re.search(r"\*\*(\d+) boxes\*\* completed across three platforms: \[\[dockerlabs\]\] \((\d+)\), \[\[tryhackme\]\] \((\d+)\), and \[\[hack-the-box\]\] \((\d+)\)", ov)
if not m:
    errors.append("OVERVIEW: snapshot line not parseable")
else:
    total, dl, thm, htb = map(int, m.groups())
    if total != len(checked): errors.append(f"OVERVIEW total {total} != roadmap [x] {len(checked)}")
    for plat, want in (("dockerlabs", dl), ("tryhackme", thm), ("hack-the-box", htb)):
        got = sum(1 for c in checked if plat_of(c) == plat)
        if got != want: errors.append(f"OVERVIEW {plat}: line says {want}, machines are {got}")

for pp in sorted(platform_pages):
    pd = fm_data.get(WIKI / "platforms" / f"{pp}.md")
    if not isinstance(pd, dict): continue
    text = read(WIKI / "platforms" / f"{pp}.md")
    listed = set()
    if "## Completed boxes" in text:
        body = re.split(r"\n## ", text.split("## Completed boxes", 1)[1])[0]
        for line in body.splitlines():
            m2 = re.match(r"^- \[\[([^\]]+)\]\]", line)
            if m2:
                stem = m2.group(1)
                if stem in opened and not re.search(r"incomplete|\u26a0", line):
                    errors.append(f"PLATFORM {pp}: open box {stem} listed WITHOUT incomplete marker")
                listed.add(stem)
    actual = {c for c in checked if plat_of(c) == pp} | {c for c in opened if plat_of(c) == pp}
    if listed != actual:
        errors.append(f"PLATFORM {pp}: page-only={sorted(listed - actual)} registry-only={sorted(actual - listed)}")

# --- 6. writeup relative links resolve ---
for p in sorted((WIKI / "machines").glob("*.md")):
    for href in re.findall(r"\]\((\.\./\.\./writeups/[^)]+)\)", read(p)):
        if not (p.parent / href).resolve().exists():
            errors.append(f"WRITEUP LINK {p.relative_to(ROOT)}: {href} missing")

# --- 7. dup stems within link-target layer ---
from collections import Counter
dup = [s for s, c in Counter(p.stem for p in link_files).items() if c > 1]
if dup: errors.append(f"DUP STEM in link layer: {sorted(dup)}")

# --- 8. tag <-> coverage parity ---
TAGS = {"ejpt:assessment": ("Assessment", "ejpt:assessment"),
        "ejpt:host-net-pentest": ("Host & Network Pentest", "ejpt:host-net-pentest"),
        "ejpt:web-pentest": ("Web Pentest", "ejpt:web-pentest")}
tech_tags = {}
for p in sorted((WIKI / "techniques").glob("*.md")):
    d = fm_data.get(p, {})
    tech_tags[p.stem] = set(d.get("tags", []) or []) if isinstance(d, dict) else set()

for tag, (ov_label, rm_tag) in TAGS.items():
    expected = {t for t, ts in tech_tags.items() if tag in ts}
    # overview table row
    row = re.search(rf"^\| {re.escape(ov_label)} \| (.+) \|$", ov, re.M)
    ov_set = set(LINK.findall(row.group(1))) if row else set()
    if ov_set != expected:
        errors.append(f"PARITY overview/{tag}: only-in-table={sorted(ov_set - expected)} only-in-fm={sorted(expected - ov_set)}")
    # roadmap Covered line
    rm_set = set()
    for sec_m in re.finditer(rf"^### [^\n]*\(`{re.escape(rm_tag)}`\)[^\n]*\n\n\*\*Covered:\*\* (.+)$", rm, re.M):
        rm_set |= set(LINK.findall(sec_m.group(1)))
    if rm_set != expected:
        errors.append(f"PARITY roadmap/{tag}: only-in-covered={sorted(rm_set - expected)} only-in-fm={sorted(expected - rm_set)}")

# --- 9. stale counts (excluding log.md) ---
for p in link_files:
    if p.name == "log.md": continue
    for n in re.findall(r"(\d+) boxes(?= (?:done|completed)|\*\*)", read(p)):
        if n != "47":
            warnings.append(f"STALE COUNT? {p.name}: '{n} boxes'")
# overview per-platform numbers checked in block 5; check dockerlabs (41) written correctly handled there

# --- 10. assets referenced ---
assets = {f.name for f in (ROOT / "assets").rglob("*") if f.is_file()}
refs = set()
scan = [p for p in link_files if p.name != "log.md"] + sorted((ROOT / "writeups").rglob("*.md"))
for p in scan:
    t = read(p)
    for name in assets:
        if name in t: refs.add(name)
warnings += [f"ASSET unreferenced: {a}" for a in sorted(assets - refs)]

# --- report ---
print(f"pages={len(wiki_pages)} links-files={len(link_files)} machines={len(machine_pages)} "
      f"checked={len(checked)} open={len(opened)} yaml_ok={len(fm_data)}")
print(f"ERRORS={len(errors)} WARNINGS={len(warnings)}")
for e in errors: print(f"  E {e}")
for w in warnings: print(f"  W {w}")
sys.exit(1 if errors else 0)
