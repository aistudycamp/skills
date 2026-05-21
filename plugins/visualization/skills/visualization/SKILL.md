---
name: visualization
description: "Create polished, single-file HTML visualizations — slide decks, dashboards, diagrams, before/after comparisons, interactive explanations. Zero dependencies, opens in any browser. Use when the user says 'make a presentation', 'build slides', 'make a deck', 'visualize this', 'make a diagram', 'create a visual', 'explain this visually', 'build an HTML deck', or asks for any standalone HTML artifact for teaching, presenting, or explaining. Do NOT use for production web apps or deployable UIs."
allowed-tools: ["Read", "Write"]
---

# Visualization

Create single-file HTML visualizations — presentations, dashboards, diagrams, teaching materials — that look polished and professional. Zero dependencies, open in any browser.

## Before you start — read these

This skill is a template. Two reference files make the output match YOUR style — read them at the start of every run:

1. `references/design-system.md` — the colors, fonts, and brand rules every visualization should follow. **Customize this file once** with your own palette and fonts; the skill then follows it every time.
2. `references/content-guidelines.md` — how to keep a visualization clear: text length, visual-first layout, one idea per slide.

**First-time setup:** If `design-system.md` still has the default neutral theme, offer to set it up for the user before building anything. They can paste their brand colors and fonts, or point to 1-3 decks they already like — read those, then write their palette, typography, and brand rules into `design-system.md`. Do this once, up front, so every later visualization matches their brand.

Also check for an `examples/` folder. If past decks have been dropped there, read 1-2 of them first and match their structure and style.

`references/design-patterns.md` holds the CSS/JS component library (cards, flows, timelines, slide navigation). Pull from it as needed — don't reinvent these.

## Step 1: Clarify the format

Ask what's being built if it isn't obvious. Pick the format based on what's being communicated:

| Format | When to Use | Navigation |
|--------|-------------|------------|
| Slides | Presenting to an audience, training, demos | Arrow keys, dots, progress bar |
| Tabbed Dashboard | Technical reference, multi-view exploration | Click tabs, scrollable content |
| Single Page | One concept, a diagram, a comparison | Scroll only |

## Step 2: Outline before building

Draft the slide titles or section names before writing any HTML. Confirm the outline with the user. A visualization with a clear spine beats a pretty one with no structure.

## Step 3: Build incrementally

- Start with the page structure and the design-system variables from `references/design-system.md`.
- Add one section/slide at a time using the components in `references/design-patterns.md`.
- Keep text minimal — follow `references/content-guidelines.md`.

## Step 4: Save and open

Save the file (ask where, or default to the current project). Then open it so the user sees it immediately:

```bash
open <filepath>
```

## Core principles

1. **Single file** — all CSS and JS inline. No dependencies except Google Fonts.
2. **Follow the design system** — don't invent colors or fonts per visualization.
3. **Generous whitespace** — 60-80px padding, never cramped.
4. **Color-coded semantics** — green = success, orange = warning, red = error/before, blue = info. Consistent meaning throughout.
5. **Smooth transitions** — 0.3-0.45s ease on interactive elements.

## Building blocks

The component patterns — cards, grids, flow diagrams, timelines, compare cards, stat cards, badges, slide navigation, tab navigation — are in `references/design-patterns.md` with copy-paste CSS and JS. Use them instead of writing components from scratch.

## Quality checklist

Before delivering, verify:
- [ ] Opens in a browser with no errors (single file, no broken references)
- [ ] All text readable (contrast, size, spacing)
- [ ] Navigation works (keyboard + click for slides; tabs for dashboards)
- [ ] Colors match `design-system.md` and semantic meaning is consistent
- [ ] Text is minimal — visuals carry the message

## Gotchas

- Always `open` the file after saving — the user wants to see it immediately.
- These are desktop / screen-share artifacts; mobile responsiveness is not required.
- Don't reinvent the slide-navigation JavaScript — copy it from `design-patterns.md`.

## Make it smarter over time

After a run, if the user corrects something or states a preference, append a note to `learnings.md` in this folder. Over time the skill learns how this user likes their visualizations.
