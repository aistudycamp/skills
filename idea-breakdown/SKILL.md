---
name: idea-breakdown
description: "Break down product ideas and automation opportunities into a prioritized build plan. Use when user says 'help me break this down', 'I want to automate this', 'here are things I want to automate', 'what should I build first', 'help me prioritize these', 'is this a good automation candidate', or describes a product idea or list of workflows they want to build or automate."
allowed-tools: ["Write"]
---

# Idea Breakdown

Turn one big idea or a list of automation ideas into a prioritized build plan - classified by type, difficulty, and what to tackle first.

## Workflow

### Step 1: Understand what they brought

Two cases:

**Case A - one big idea** (e.g. "I want to build a tool that manages my client onboarding"):
Tell them: "Let me break this into components first, then we'll figure out what's automatable and what to build first."
List every distinct piece of the idea: user-facing features, data flows, integrations, background processes. Think "what does this system need to do?" not code.

**Case B - a list of specific ideas or workflows** (e.g. "here are 5 things I want to automate"):
Skip decomposition. Go straight to Step 2.

---

### Step 2: Check pain levels

Before classifying anything, ask:

> "Before I dig in -- are any of these particularly painful right now? Something you're doing manually that's eating a lot of your time?"

Let them tell you. Note which ones they flag as high-pain -- these get priority weight later.

---

### Step 3: Classify each component or idea

For each item, assign one of four categories:

**Manual / UI**
User-facing interaction. Claude Code builds it, but it's not an automation candidate -- a human needs to be there. Examples: a form, a dashboard, a settings page.

**Simple workflow**
Predictable trigger → predictable output. The same input always produces the same output. No judgment needed. Examples: send an email when a form is submitted, format a spreadsheet, post to Slack when a file is uploaded.
→ Tools in this category: n8n, Zapier, GumLoop, Make, and similar. All the same idea -- pick whichever you already use.

**Agent**
Needs to make decisions, handle ambiguity, use multiple tools, or loop until a goal is reached. Examples: research a company and write a summary, read an email and draft a contextual reply, debug code until tests pass.
→ Tools in this category: Claude API with tool use, custom code. More complex to build, but handles tasks that have no fixed output.

**Not yet**
High-stakes, judgment-heavy, or too context-dependent. The cost of getting it wrong is high. Do this manually for now -- revisit once you've built simpler things.

---

### Step 4: Score difficulty

For each automatable item (simple workflow or agent):

- **Low** -- single trigger, single action, minimal edge cases. Can be set up in an afternoon.
- **Medium** -- multi-step, some branching or tool use, a few things that could go wrong.
- **High** -- complex context, many edge cases, needs tuning over time.

---

### Step 5: Output the plan

Present a table:

| Idea / Component | Type | Difficulty | Pain Level | Recommendation |
|-----------------|------|------------|------------|----------------|
| [item] | Simple workflow / Agent / Manual / Not yet | Low / Medium / High | High / Medium / Low | ⭐ Start here / Build next / Skip for now |

Then give a clear recommendation:

> "Start with [X]. It's [high pain / low difficulty / high value] and will give you a quick win. After that, [Y] is the next logical step because [reason]."

---

### Step 6: Offer to save it

Ask: "Want me to save this as a file so you can reference it while you build?"

If yes, save to `plans/idea-breakdown.md` in the current directory.

---

## Notes

- If everything gets labeled "agent," push back: "Does this actually need to make a judgment call, or is it just a trigger → action?" Most things are simpler than they look.
- If the list is longer than 7 items, ask them to cut it to the most important 5 before classifying. Too many options leads to no action.
- If they're not sure which category something falls into, ask: "Does the output change based on context, or is it always the same?" Same output = workflow. Context-dependent output = agent.
