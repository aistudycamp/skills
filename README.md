# Skills

Installable skills and exercises for [AI Study Camp](https://aistudycamp.com) students.

## What's in this repo

### idea-breakdown (Skill)

A ready-to-use Claude Code skill. Give it one big idea or a list of automation candidates and get back a classified, prioritized build plan with agent vs. workflow recommendations.

**Install:**

```bash
cp -r idea-breakdown ~/.claude/skills/idea-breakdown
```

That's it. Next time you open Claude Code and say something like "help me break this down" or "what should I build first," it activates automatically.

---

### skill-builder (Exercise)

An interactive 45-minute exercise where you build your first Claude Code skill from scratch. Claude walks you through everything - no prior skill-building experience needed.

| Module | Topic | Time | You'll Produce |
|--------|-------|------|----------------|
| 1 | What is a Skill? | ~5 min | Understanding of when and why to create skills |
| 2 | Build Your First Skill | ~20 min | A working skill installed at `~/.claude/skills/` |
| 3 | Iterate & Refine | ~10 min | learnings.md + references/ added to your skill |
| 4 | Find & Share Skills | ~10 min | A community plugin installed + knowledge of sharing skills |

**Run it:**

```bash
git clone https://github.com/aistudycamp/skills.git
cd skills/skill-builder
claude
```

Say hello to get started.

---

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) installed and working
- Comfortable using a terminal (cd, ls, basic navigation)
