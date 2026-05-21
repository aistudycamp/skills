# Design System

This file defines the look of every visualization the skill produces — colors, fonts, and brand rules. **Customize it once with your own brand, then the skill follows it every time.**

The values below are a clean neutral dark theme that works out of the box. Replace them with your own.

## Color Palette

Defined as CSS variables. This `:root` block goes into every visualization.

```css
:root {
  --bg: #0f1117;        /* page background */
  --surface: #1a1d27;   /* card background */
  --surface2: #232735;  /* nested surface */
  --border: #2d3148;    /* borders */
  --text: #e1e4ed;      /* primary text */
  --text2: #8b90a5;     /* secondary text */
  --accent: #6366f1;    /* main accent — your brand color */
  --accent2: #818cf8;   /* lighter accent — highlights */

  /* Semantic colors — keep these meanings consistent */
  --green: #22c55e;     /* success / confirmed / after */
  --orange: #f59e0b;    /* warning / pending */
  --red: #ef4444;       /* error / danger / before */
  --blue: #3b82f6;      /* info */
}
```

**To make it yours:** change `--accent` and `--accent2` to your brand color. Adjust `--bg` and `--surface` for a lighter or warmer theme. Leave the semantic colors unless you have a strong reason — consistent meaning matters more than variety.

## Typography

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');
```

- **Headings & body:** DM Sans
- **Numbers, code, data:** JetBrains Mono
- **Scale:** h1 52px / h2 36px / body 16-20px / labels 12px uppercase

**To make it yours:** swap the Google Fonts import and the family names. Pick one display font for headings and one clean font for body — that single choice changes the whole feel.

## Brand Rules

Optional. Fill in anything specific to your brand so the skill never has to guess:

- **Logo / wordmark:** where it goes (e.g. "fixed bottom-left on every slide")
- **Default theme:** light or dark
- **Never use:** anything that should never appear (e.g. "no gradients", "one accent color only")

---

## Example: a fully filled-in design system

Here is what this file looks like completely customized — the AI Study Camp deck system. Use it as a reference for the level of detail to aim for:

> **Palette:** warm cream background `#F5F0EB`, primary text `#1C1917`, white cards, a single teal accent `#0D9488` (no secondary accent).
>
> **Typography:** Playfair Display for headings, Geist for body and UI, Geist Mono for code.
>
> **Conventions:** dark title slide, cream content slides, `[ ai study camp ]` wordmark bottom-left on every content slide, solid teal progress bar fixed at the top.
>
> **Hard rule:** teal is the only accent — no amber, violet, or brown anywhere on any slide.

The point: every design decision is made once, here. The skill never improvises — it just follows this file.
