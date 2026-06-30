---
name: map-my-setup
description: Audit a Claude Code setup and produce a polished, shareable single-file HTML dashboard. The script (scan.py) is read-only and finds every CLAUDE.md, skill, agent, command, hook, and MCP server (from ALL sources), where each lives, whether it is available everywhere or only in one folder, whether it is in version control, and which CLAUDE.md files are bloated. Claude then enriches it with plain-English descriptions and writes prioritized recommendations. Use when the user says "map my setup", "audit my Claude setup", "inventory my Claude config", "what's in my Claude config", "what do I have installed", "is my setup bloated", or wants a shareable picture of their configuration to review with someone (e.g. a consultant or teammate).
---

# Map My Setup

Audit this Claude Code setup and produce one polished, self-contained HTML dashboard the user can open offline and share with a collaborator. The dashboard has four tabs: **Recommendations** (what to change, highest-impact first), **Findings** (bloated CLAUDE.mds, version-control gaps), **Folder map** (an interactive Icicle / Sunburst / Columns view), and **Inventory** (skills, agents, commands, hooks, MCP).

The script finds WHAT exists and flags problems deterministically. Claude adds the two things a script cannot: a plain-English description of each piece, and prioritized, judgment-based recommendations. It is **read-only** - it never edits, reorganizes, or "fixes" anything.

## How to run it

0. **Get MCP ground truth first - ask the user to run `/mcp` and paste the result.** This is the one step that is easy to skip and the one that matters most for MCP. `/mcp` shows what is *actually loaded* in their session - the only reliable source for managed claude.ai connectors (Gmail, Slack, etc.) and for config inherited from a folder you would not think to scan. A bare `.mcp.json` check can report "0 servers" while `/mcp` shows 15. Reconcile the script's MCP output against `/mcp`; if a server is missing, ask which folder they were in when they added it and pass that folder as an extra root.

1. **Run the scan, generating the HTML in one command:**
   ```bash
   python3 scripts/scan.py [root ...] --html OUTPUT.html [--recs recs.json] [--desc desc.json]
   ```
   - It is read-only. It inspects the given roots (default: current dir) and always folds in `~/.claude` for global config. **Pass the roots that hold the user's real work** - e.g. `python3 scripts/scan.py ~/cc ~/cacti --html map.html`. If `/mcp` showed servers the scan missed, add the folder that holds that `.mcp.json` as a root.
   - The script prints a SUMMARY and a `===== JSON =====` block, and (with `--html`) writes a self-contained dashboard (d3 + data inlined, opens offline).

2. **Read the SUMMARY and the JSON.** Note the bloated CLAUDE.mds (ranked by impact, see below), the version-control gaps, and the inventory. The folder map, findings, and inventory tabs are populated automatically from the JSON - you do not hand-build them.

3. **Enrich the inventory - describe each item in plain English.** The script pulls each skill/agent/command's frontmatter `description`, but for anything thin or missing, open the file and write a one-line "what it does." Pass these as `--desc desc.json` (a `{ "name": "one-liner", ... }` map) to override/fill. Don't summarize from the name alone - read it. Don't undercount **custom automation the user built themselves** (homemade agent loops, scheduled harnesses, prompt libraries) that live outside `~/.claude`; if you see candidate folders, ask "do you have any automation or agent loops you built that aren't standard Claude skills/agents?" and describe them.

4. **Write the recommendations - this is the judgment step (`--recs recs.json`).** Read the flagged CLAUDE.mds and the folder shape, then write concrete, prioritized actions. Schema: a JSON array of `{ "title", "severity": "high"|"med"|"low", "why", "action", "paths": [] }`. **Order by IMPACT, not raw line count** (see the priority rule below). Then re-run step 1 with `--recs recs.json` (and `--desc`) to bake them into the dashboard.

5. **Tell the user where the file is** and what the top recommendation is. Offer to commit it so the map itself is saved.

## How to judge impact (the priority rule)

A bloated CLAUDE.md's real cost is **how often it loads**, which tracks how shallow and central the folder is - not how many lines it has. The script already ranks findings this way (`priority` field) and sinks personal-life folders; your recommendations must reflect the same judgment:

- **A shallow, central, daily-driver CLAUDE.md beats a long, buried one.** A 312-line config at the root of a folder the user works in constantly (a personal-assistant repo, the global `~/.claude/CLAUDE.md` that loads in *every* project) is a far bigger deal than a 587-line research doc 5 levels deep in a wedding-planning folder that loads almost never. Lead with the former; explicitly call the latter "not a priority."
- **Position in the tree = frequency of loading = impact.** Shallower and config-bearing folders load more. Weight them up.
- **Disposable scaffolds (test/cohort projects) are bloated but throwaway** - say "archive, don't trim," don't rank them high.

## Backup status - be honest, never alarm

The script reports version control only, because that is all it can verify:
- `git_remote` = in git with a remote (provably safe). `git_local` = committed but no remote. `untracked` = not in git.
- **Never say "not backed up."** The tool cannot see Time Machine / Backblaze / iCloud. Say "not in version control" - a precise, true statement - and frame an untracked global-skills folder as a gentle finding ("these live only on this machine in git terms"), not an alarm. Symlinked-into-a-repo content reads correctly as in-git (the script resolves symlinks).

## Files in this skill
- `scripts/scan.py` - the read-only audit + `--html` generator. Never modify the setup it scans.
- `assets/map-template.html` - the dashboard template (4 tabs, AISC cream design, the 3-mode folder map). `scan.py --html` inlines `d3.min.js` + the data + your `--desc`/`--recs` into it.
- `assets/d3.min.js` - inlined into the dashboard so it opens offline (no CDN).

## Rules
- **Read-only, always.** scan.py and this skill never write, edit, delete, or reorganize the scanned setup. The only thing written is the output HTML.
- **Read files to describe them.** A map whose descriptions were guessed from filenames is worse than none.
- **Scope is a first-class fact.** For every item, say whether it is global (every project) or folder-only.
- **Reconcile MCP against `/mcp`.** Never trust an empty MCP result without checking `~/.claude.json` and the `/mcp` list.
- **If a section is empty, say so** rather than omitting it - absence is information.
