# AI Study Camp Skills

A Claude Code plugin marketplace for [AI Study Camp](https://aistudycamp.com) students. Install skills straight into Claude Code - no downloads, no files to move.

> **New to skills?** Start with the **[Visualization Skill guide](https://aistudycamp.github.io/skills/visualization-guide.html)** - a short deck on what makes a good skill, plus how to install and customize the visualization skill.

## Install a skill

Two commands, typed inside Claude Code. First, add this marketplace (once):

```
/plugin marketplace add aistudycamp/skills
```

Then install whichever skill you want:

```
/plugin install visualization@aistudycamp-skills
/plugin install idea-breakdown@aistudycamp-skills
```

That's it - the skill installs and activates automatically when you need it. Updates later are one command: `/plugin update`.

## Skills

### visualization

Builds polished, single-file HTML slide decks, dashboards, and diagrams. Zero dependencies, opens in any browser. Activates when you say "make a deck," "build slides," or "visualize this."

It ships as a **template** - it works out of the box with a neutral theme, and you make it yours:

- Tell Claude your brand (colors, fonts) and it sets up the design system - or edit `design-system.md` directly
- Show Claude a few decks you like so it matches your style

See the [guide](https://aistudycamp.github.io/skills/visualization-guide.html) for the full walkthrough.

### idea-breakdown

Give it one big idea or a list of automation candidates and get back a classified, prioritized build plan with agent vs. workflow recommendations. Activates when you say "help me break this down" or "what should I build first."

## Exercise: skill-builder

An interactive 45-minute exercise where you build your first Claude Code skill from scratch - no prior experience needed.

| Module | Topic | Time | You'll Produce |
|--------|-------|------|----------------|
| 1 | What is a Skill? | ~5 min | Understanding of when and why to create skills |
| 2 | Build Your First Skill | ~20 min | A working skill installed at `~/.claude/skills/` |
| 3 | Iterate & Refine | ~10 min | learnings.md + references/ added to your skill |
| 4 | Find & Share Skills | ~10 min | A community plugin installed + knowledge of sharing skills |

This one is a clone-and-run exercise, not an installable skill:

```bash
git clone https://github.com/aistudycamp/skills.git
cd skills/skill-builder
claude
```

Say hello to get started.

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- For the skill-builder exercise: comfortable using a terminal (`cd`, `ls`, basic navigation)

## For maintainers

This repo is a plugin marketplace. Each installable skill is a plugin under `plugins/`, cataloged in `.claude-plugin/marketplace.json`. To add a skill: create `plugins/<name>/` with a `.claude-plugin/plugin.json` and `skills/<name>/SKILL.md`, then add an entry to the marketplace manifest.
