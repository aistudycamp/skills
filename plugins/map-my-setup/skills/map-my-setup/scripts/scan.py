#!/usr/bin/env python3
"""
Read-only AUDIT of a Claude Code setup. Never writes, edits, or deletes.

The goal is not a pretty picture — it's the handful of facts that let a human (or a
Claude) make real recommendations about a setup:
  - WHERE is context (CLAUDE.md) defined, and is any of it BLOATED (loaded every turn)?
  - What skills / agents / commands / hooks / MCP servers exist, where, at what SCOPE?
  - What is BACKED UP (git + remote) vs only on this machine?
  - Where is the SPRAWL / DUPLICATION (e.g. git worktrees shadow-copying a tree)?

Model: a TREE of "meaningful folders" — any folder that has a CLAUDE.md, has Claude
config (.claude / skills), or is a git repo root. Everything else is collapsed into a
sprawl count. This matches how people actually nest context, and it's what the zoomable
map renders. Non-meaningful folders are never shown as nodes.

Emits TWO things on stdout:
  1. A human SUMMARY (counts + top findings) for quick reading.
  2. A `===== JSON =====` block: the machine contract the HTML dashboard + any Claude
     consume. Do not hand-edit it.

Usage:  python3 scan.py [root ...]
Run from the TOP of the workspace (e.g. ~/ or ~/cc) to see everything, or from one
project folder to map just that. ~/.claude is always folded in for global config.
"""
import json, os, subprocess, sys
from pathlib import Path

HOME = Path.home()
GLOBAL = Path(os.environ.get("CLAUDE_GLOBAL", HOME / ".claude"))
CWD = Path.cwd()

PRUNE = {"node_modules", "Library", ".Trash", ".cache", "cache", "Applications",
         ".npm", ".vscode", "dist", "build", ".next", "out", "venv", ".venv",
         "__pycache__", ".wrangler", ".turbo", ".pytest_cache", "coverage",
         "vendor", "target", ".gradle", ".idea", "Pods", "DerivedData", ".DS_Store",
         "worktrees",                       # git shadow-copies — would double-count everything
         "plugins", "marketplaces", ".claude-personal"}  # plugin internals, not the user's setup
BLOAT_HARD = 300   # likely bloated — loaded every turn in that folder
BLOAT_SOFT = 200   # worth a look
MAXDEPTH = 9
# Config plumbing: counted (skills fold into the parent) but never shown as its own map node.
INFRA = {".claude", ".git", "skills", "agents", "commands", "hooks"}
# Personal-life folders: real, but NOT where the high-impact setup work is. Demoted so the
# map leads with what matters (active build/work folders) and these sink to the bottom.
LOW_PRIORITY = {"wedding","sports","cooking","travel","vibing","shopping","la-paz","health",
                "life-admin","life-decisions","ele","pc"}

def impact_score(name, depth, lines, health, git_root, has_cfg, n_skills, sprawl, low_pri):
    """Rank a folder by how much it matters to the SETUP, not by size. Drives ordering."""
    s = 0
    if health == "bloated": s += 120          # an oversized always-loaded CLAUDE.md is the #1 thing to fix
    elif health == "watch": s += 60
    if lines > 0:           s += 10           # has steering context at all
    if git_root:            s += 25           # a real project
    if has_cfg:             s += 20           # carries Claude config (skills/agents)
    s += min(n_skills, 12) * 6                # more skills = more surface to manage
    s += max(0, 40 - depth * 12)              # shallower (top-level) = higher impact
    s += min(sprawl, 20) // 4                 # bigger subtree counts a little, capped (don't let wedding's 8 levels win)
    if low_pri: s -= 200                      # personal-life folders (and everything under them) sink to the bottom
    return s

def run(cmd, cwd=None):
    try: return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=10).stdout.strip()
    except Exception: return ""

def tilde(p): return str(p).replace(str(HOME), "~")
def is_global(p):
    try: return GLOBAL in p.parents or p == GLOBAL
    except Exception: return False

# ---- version-control status, cached per repo root (no per-file subprocess storms) ----
# Honest framing: we can only VERIFY git. We cannot see Time Machine / Backblaze / iCloud,
# so we never claim "not backed up" — only "in git" (provable) vs "not in git" (unknown).
# Symlink-aware: resolve the real path first so symlinked-into-a-repo content reads correctly.
_repo, _remote = {}, {}
def repo_root(d: Path):
    try: real = d.resolve()
    except Exception: real = d
    k = str(real)
    if k not in _repo: _repo[k] = run(["git","rev-parse","--show-toplevel"], cwd=k) or None
    return _repo[k]
def repo_remote(top):
    if not top: return ""
    if top not in _remote: _remote[top] = run(["git","remote","get-url","origin"], cwd=top) or ""
    return _remote[top]
def vc_status(d: Path):
    """('git_remote'|'git_local'|'untracked', remote_url). Resolves symlinks."""
    top = repo_root(d)
    if not top: return ("untracked", "")          # not in any git repo (may still be machine-backed-up — we can't tell)
    rem = repo_remote(top)
    return ("git_remote", rem) if rem else ("git_local", top)
# back-compat alias
def backup_of(d: Path):
    st, rem = vc_status(d)
    return (st, rem)

def count_lines(p: Path):
    try: return sum(1 for _ in open(p, "r", errors="ignore"))
    except Exception: return 0
def is_worktree(d: Path):
    return "worktrees" in d.parts or (d / ".git").is_file()
def child_dirs(d: Path):
    try:
        return sorted([c for c in d.iterdir()
                       if c.is_dir() and c.name not in PRUNE and not c.name.startswith(".Trash")
                       and not c.is_symlink()], key=lambda x: x.name.lower())
    except Exception:
        return []
def frontmatter_desc(p: Path):
    """First line of the YAML `description:` field, trimmed. '' if none."""
    try:
        txt = open(p, "r", errors="ignore").read(4000)
    except Exception:
        return ""
    if not txt.lstrip().startswith("---"): return ""
    body = txt.split("---", 2)
    if len(body) < 3: return ""
    desc, grab = [], False
    for line in body[1].splitlines():
        s = line.strip()
        if s.lower().startswith("description:"):
            grab = True; desc.append(s.split(":", 1)[1].strip()); continue
        if grab:
            if not s or ":" in s.split(" ")[0]: break   # next key
            desc.append(s)
    return " ".join(desc).strip().strip('"\'')[:200]

# Folder-scoped skills collected during the tree walk (global ones handled separately).
FOLDER_SKILLS = []
_seen_skills = set()   # dedupe symlinked / re-reachable skill dirs by real path
def collect_skills(d: Path):
    """Count skills under d AND record folder-scoped ones for the inventory."""
    n = 0
    for base in (d / ".claude" / "skills", d / "skills"):
        if base.is_dir():
            for s in base.iterdir():
                sm = s / "SKILL.md"
                if sm.exists():
                    n += 1
                    real = str(s.resolve())
                    if real in _seen_skills: continue
                    _seen_skills.add(real)
                    bstat, _ = backup_of(s)
                    FOLDER_SKILLS.append({"name": s.name, "scope": f"folder:{tilde(d)}",
                                          "desc": frontmatter_desc(sm), "backup": bstat})
    if (d / "SKILL.md").exists(): n += 1
    return n
def has_config(d: Path):
    return (d / ".claude").is_dir() or (d / "skills").is_dir() or (d / "SKILL.md").exists()

# ---------------------------------------------------------------------------
# Build the meaningful-folder tree.
#  Returns (node_or_None, descendant_dir_count). A node is emitted if the folder is
#  itself meaningful OR has a meaningful descendant. depth/sprawl tracked inline.
# ---------------------------------------------------------------------------
ALL_NODES = []  # flat list for findings

def build(d: Path, depth: int, lp: bool = False):
    low_pri = lp or d.name.lower() in LOW_PRIORITY   # inherit: everything under wedding/ is low-priority too
    kids, sprawl = [], 0
    if depth < MAXDEPTH:
        for c in child_dirs(d):
            if is_worktree(c) or c.name in INFRA:
                sprawl += 1
                continue
            node, sub = build(c, depth + 1, low_pri)
            sprawl += 1 + sub
            if node: kids.append(node)
    md = d / "CLAUDE.md"
    lines = count_lines(md) if md.exists() else 0
    cfg = has_config(d)
    git_root = (d / ".git").is_dir()
    meaningful = md.exists() or cfg or git_root
    if not meaningful and not kids:
        return None, sprawl
    health = ("missing" if not md.exists() else
              "bloated" if lines > BLOAT_HARD else
              "watch" if lines > BLOAT_SOFT else "ok")
    bstat, brem = backup_of(d)
    nsk = collect_skills(d)
    imp = impact_score(d.name, depth, lines, health, git_root, cfg, nsk, sprawl, low_pri)
    kids.sort(key=lambda k: (-k["impact"], k["name"].lower()))   # high-impact first; low-priority sinks
    node = {
        "name": d.name or str(d),
        "path": tilde(d),
        "depth": depth,
        "claudemd_lines": lines,
        "health": health if (md.exists() or git_root or cfg) else "none",
        "n_skills": nsk,
        "has_config": cfg,
        "git_root": git_root,
        "backup": bstat,                 # 'git_remote' | 'git_local' | 'untracked' (honest: only git is verifiable)
        "remote": brem.split("/")[-1].replace(".git", "") if brem else "",
        "impact": imp,                   # ranking score — drives ordering everywhere
        "low_priority": low_pri,         # this folder or an ancestor is personal-life (wedding, etc.)
        "sprawl": sprawl,                # descendant dirs collapsed under this node
        "n_meaningful_kids": len(kids),
        "children": kids,
    }
    ALL_NODES.append(node)
    return node, sprawl

# ---------------------------------------------------------------------------
# Global config + MCP (all sources)
# ---------------------------------------------------------------------------
def global_picture():
    cj = {}
    cjp = HOME / ".claude.json"
    if cjp.exists():
        try: cj = json.load(open(cjp))
        except Exception: pass
    def skill_items():
        base = GLOBAL / "skills"
        if not base.exists(): return []
        out = []
        for s in sorted(base.iterdir(), key=lambda x: x.name.lower()):
            if (s / "SKILL.md").exists():
                vc, _ = vc_status(s)   # symlink-aware: symlinked-into-a-repo skills read as git_remote
                out.append({"name": s.name, "desc": frontmatter_desc(s / "SKILL.md"),
                            "backup": vc, "linked": s.is_symlink()})
        return out
    def md_items(sub):
        base = GLOBAL / sub
        if not base.exists(): return []
        return [{"name": p.stem, "desc": frontmatter_desc(p)}
                for p in sorted(base.glob("*.md"), key=lambda x: x.stem.lower()) if p.stem.lower() != "readme"]
    gmd = GLOBAL / "CLAUDE.md"
    HOOK_EVENTS = ["PreToolUse","PostToolUse","UserPromptSubmit","SessionStart","Stop","Notification","SubagentStop","PreCompact"]
    hooks = []
    for sp in (GLOBAL / "settings.json", GLOBAL / "settings.local.json"):
        if sp.exists():
            try: evs = [e for e in HOOK_EVENTS if e in json.load(open(sp)).get("hooks", {})]
            except Exception: evs = []
            if evs: hooks.append({"file": tilde(sp), "events": evs})
    mcp = {"user_scope": list((cj.get("mcpServers") or {}).keys()), "per_project": [], "plugins": []}
    for pth, cfg in (cj.get("projects") or {}).items():
        m = list((cfg.get("mcpServers") or {}).keys())
        if m: mcp["per_project"].append({"folder": tilde(Path(pth)), "servers": m})
    pl = GLOBAL / "plugins" / "installed_plugins.json"
    if pl.exists():
        try: mcp["plugins"] = sorted((json.load(open(pl)).get("plugins") or {}).keys())
        except Exception: pass
    skills = skill_items()
    commands = md_items("commands")
    skill_names = {s["name"] for s in skills}
    # In Claude Code a skill IS invoked as /name. Flag commands that duplicate a skill name
    # so the dashboard can reconcile the two lists instead of double-counting.
    for c in commands:
        c["also_skill"] = c["name"] in skill_names
    return {
        "global_dir": tilde(GLOBAL), "global_exists": GLOBAL.exists(),
        "global_claudemd_lines": count_lines(gmd) if gmd.exists() else 0,
        "global_backup": ("symlink" if gmd.is_symlink() else backup_of(GLOBAL)[0]) if gmd.exists() else "missing",
        "skills": skills,
        "agents": md_items("agents"),
        "commands": commands,
        "hooks": hooks, "mcp": mcp,
    }

# ---------------------------------------------------------------------------
# Find every .mcp.json across the workspace (folder-scoped servers)
# ---------------------------------------------------------------------------
def find_mcp_files(roots):
    out = []
    for ws in roots:
        base = len(ws.parts)
        for dp, dn, fn in os.walk(ws):
            d = Path(dp)
            dn[:] = [x for x in dn if x not in PRUNE and not x.startswith(".Trash")]
            if len(d.parts) - base > MAXDEPTH: dn[:] = []; continue
            if ".mcp.json" in fn:
                fp = d / ".mcp.json"
                try: servers = list(json.load(open(fp)).get("mcpServers", {}).keys())
                except Exception: servers = []
                if servers:
                    top = repo_root(d)
                    out.append({"file": tilde(fp),
                                "scope": "global" if is_global(fp) else f"folder:{tilde(Path(top)) if top else tilde(d)}",
                                "servers": servers, "backup": backup_of(d)[0]})
    return out

# --------------------------- drive ---------------------------
# flags: --html PATH (write single-file dashboard) · --desc PATH (json overrides) · --recs PATH (json recs)
argv = sys.argv[1:]
html_out, desc_path, recs_path, positional, no_open = None, None, None, [], False
i = 0
while i < len(argv):
    if argv[i] == "--html" and i + 1 < len(argv): html_out = argv[i+1]; i += 2
    elif argv[i] == "--desc" and i + 1 < len(argv): desc_path = argv[i+1]; i += 2
    elif argv[i] == "--recs" and i + 1 < len(argv): recs_path = argv[i+1]; i += 2
    elif argv[i] == "--no-open": no_open = True; i += 1   # suppress auto-open (headless/CI)
    else: positional.append(argv[i]); i += 1
roots = [Path(a).expanduser().resolve() for a in positional if Path(a).expanduser().exists()] or [CWD.resolve()]
seen, ws = set(), []
for r in roots:
    if r not in seen and r.is_dir(): seen.add(r); ws.append(r)

forest = []
for w in ws:
    node, _ = build(w, 0)
    if node: forest.append(node)
forest.sort(key=lambda k: (-k["impact"], k["name"].lower()))   # lead with the highest-impact root
glob = global_picture()
mcp_files = find_mcp_files(ws)

# --------------------------- findings ---------------------------
# Rank by IMPACT, not raw lines. A bloated CLAUDE.md's real cost = how often it loads, which
# tracks how shallow/central the folder is (a root/daily-driver folder loads constantly; a deep
# wedding-venue doc almost never). `impact` already encodes shallowness + config + skills, and
# sinks low-priority personal folders. So a central 312L root beats a deep 587L venue doc.
def bloat_priority(n):
    sev = n["claudemd_lines"]                 # severity (how bloated)
    central = max(0, 6 - n["depth"]) * 60     # shallower folder = loaded far more often
    if n["has_config"] or n["n_skills"]: central += 120   # a folder you actually work in
    if n["low_priority"]: return sev * 0.1 - 1000         # personal-life docs sink hard
    return sev + central
bloated = sorted(
    [{"path": n["path"], "name": n["name"], "lines": n["claudemd_lines"], "flag": n["health"],
      "low_priority": n["low_priority"], "depth": n["depth"],
      "central": bool(n["has_config"] or n["n_skills"]),
      "priority": round(bloat_priority(n))}
     for n in ALL_NODES if n["health"] in ("bloated", "watch")],
    key=lambda x: -x["priority"])
# "missing" matters only where context is clearly warranted: a real git repo root with
# no CLAUDE.md to steer it. (Config-only folders like .claude/skills are not flagged.)
missing = [{"path": n["path"], "name": n["name"], "why": "git repo, no CLAUDE.md"}
           for n in ALL_NODES if n["health"] == "missing" and n["git_root"] and not n["name"].startswith("_")]
# Honest + neutral: only surface PROJECT folders (git roots) that aren't pushed to a remote.
# We don't flag every untracked folder as a "gap" — we can't see machine backups, and global
# skills living only in ~/.claude is reported in the inventory, not as an alarm here.
backup_gaps = [{"path": n["path"], "name": n["name"],
                "why": "git repo, no remote (local commits only)" if n["backup"] == "git_local"
                       else "not in version control"}
               for n in ALL_NODES if n["git_root"] and n["backup"] in ("git_local", "untracked")]
total_claudemd = sum(1 for n in ALL_NODES if n["claudemd_lines"] > 0)
total_dirs = sum(n["sprawl"] for n in forest) + len(forest)

doc = {
    "workspace": [tilde(w) for w in ws],
    "hostname": run(["hostname", "-s"]) or "local",
    "totals": {
        "meaningful_folders": len(ALL_NODES),
        "dirs_scanned": total_dirs,
        "claudemd_files": total_claudemd,
        "bloated": sum(1 for b in bloated if b["flag"] == "bloated"),
        "watch": sum(1 for b in bloated if b["flag"] == "watch"),
        "max_depth": max((n["depth"] for n in ALL_NODES), default=0),
    },
    "tree": forest,
    "global": glob,
    "folder_skills": sorted(FOLDER_SKILLS, key=lambda x: x["name"].lower()),
    "mcp_files": mcp_files,
    "findings": {"bloated_claudemds": bloated, "missing_claudemd": missing, "backup_gaps": backup_gaps},
    "thresholds": {"bloat_hard": BLOAT_HARD, "bloat_soft": BLOAT_SOFT},
}

# --------------------------- human summary ---------------------------
print("===== SUMMARY =====")
print(f"workspace: {', '.join(doc['workspace'])}   host: {doc['hostname']}")
t = doc["totals"]
print(f"meaningful folders: {t['meaningful_folders']}   dirs scanned: {t['dirs_scanned']}   "
      f"CLAUDE.md files: {t['claudemd_files']}   bloated(>{BLOAT_HARD}): {t['bloated']}   "
      f"watch({BLOAT_SOFT}-{BLOAT_HARD}): {t['watch']}   deepest nesting: {t['max_depth']}")
print(f"global ~/.claude: skills {len(glob['skills'])}, agents {len(glob['agents'])}, "
      f"commands {len(glob['commands'])}, CLAUDE.md {glob['global_claudemd_lines']}L ({glob['global_backup']}), "
      f"hooks {sum(len(h['events']) for h in glob['hooks'])}")
print(f"MCP: user-scope {glob['mcp']['user_scope']}, .mcp.json files {len(mcp_files)}, "
      f"plugins {len(glob['mcp']['plugins'])}  (run /mcp for managed connectors)")
print("\nTOP FINDINGS")
if bloated: print(f"  Long/bloated CLAUDE.md ({len(bloated)}): " + "; ".join(f"{b['name']} {b['lines']}L" for b in bloated[:8]))
if missing: print(f"  Warrants a CLAUDE.md ({len(missing)}): " + ", ".join(m["name"] for m in missing[:12]))
if backup_gaps: print(f"  Not in version control ({len(backup_gaps)}): " + ", ".join(f"{n['name']}" for n in backup_gaps[:12]))
print("\n===== JSON =====")
data_json = json.dumps(doc, separators=(",", ":"))
print(data_json)
print("\n===== END =====")

# --------------------------- optional: render single-file HTML ---------------------------
if html_out:
    assets = Path(__file__).resolve().parent.parent / "assets"
    tpl = (assets / "map-template.html").read_text()
    d3 = (assets / "d3.min.js").read_text()
    def load_json(p, default):
        if p and Path(p).expanduser().exists():
            try: return json.dumps(json.load(open(Path(p).expanduser())))
            except Exception: pass
        return default
    descriptions = load_json(desc_path, "{}")
    recommendations = load_json(recs_path, "[]")
    # order matters: inline d3 first (large, contains no other placeholders), then data
    html = (tpl.replace("{{D3_INLINE}}", d3)
               .replace("{{DATA_JSON}}", data_json)
               .replace("{{DESCRIPTIONS}}", descriptions)
               .replace("{{RECOMMENDATIONS}}", recommendations))
    outp = Path(html_out).expanduser()
    outp.write_text(html)
    print(f"\nWrote dashboard: {tilde(outp)}  ({len(html)//1024} KB, self-contained - opens offline)")
    if not no_open:
        try:
            import platform
            sysname = platform.system()
            if sysname == "Darwin": subprocess.run(["open", str(outp)], check=False)
            elif sysname == "Windows": os.startfile(str(outp))  # type: ignore[attr-defined]
            else: subprocess.run(["xdg-open", str(outp)], check=False)
            print("Opened it in your default browser.")
        except Exception:
            print("(Could not auto-open - open the file path above in your browser.)")
