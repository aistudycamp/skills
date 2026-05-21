# Design Patterns Reference

Reusable CSS and JS patterns extracted from proven visualizations. Copy and adapt.

## Table of Contents
- [Base Reset & Typography](#base-reset--typography)
- [Card Components](#card-components)
- [Flow Diagrams](#flow-diagrams)
- [Timeline](#timeline)
- [Compare Cards (Before/After)](#compare-cards)
- [Stat Cards](#stat-cards)
- [Classification Grid](#classification-grid)
- [Status Badges & Pills](#status-badges--pills)
- [Slide Navigation JavaScript](#slide-navigation-javascript)
- [Tab Navigation JavaScript](#tab-navigation-javascript)
- [Light Theme UI Mockups](#light-theme-ui-mockups)

---

## Base Reset & Typography

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700&family=JetBrains+Mono:wght@400;500&display=swap');

* { margin: 0; padding: 0; box-sizing: border-box; }
body {
  font-family: 'DM Sans', -apple-system, sans-serif;
  background: var(--bg); color: var(--text);
  line-height: 1.6;
}

/* Slide presentations: lock viewport */
body.slides { overflow: hidden; height: 100vh; }

/* Typography scale */
h1 { font-size: 52px; font-weight: 700; letter-spacing: -1.5px; line-height: 1.1; }
h2 { font-size: 36px; font-weight: 700; letter-spacing: -1px; line-height: 1.2; }
h1 span, h2 span { color: var(--accent2); } /* accent word */

.slide-label {
  font-size: 12px; font-weight: 600; text-transform: uppercase;
  letter-spacing: 2px; color: var(--accent2); margin-bottom: 16px;
}
.subtitle { font-size: 20px; color: var(--text2); font-weight: 400; line-height: 1.5; }
```

## Card Components

Base card with colored top stripe:

```css
.card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 24px; position: relative; overflow: hidden;
}
.card::before {
  content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px;
}
/* Color variants via additional class */
.card.green::before { background: var(--green); }
.card.orange::before { background: var(--orange); }
.card.blue::before { background: var(--blue); }
.card.red::before { background: var(--red); }
.card.accent::before { background: var(--accent2); }
```

Grid layouts:

```css
.grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
.grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; }
```

## Flow Diagrams

Horizontal node -> arrow -> node chains:

```css
.flow-row { display: flex; align-items: center; gap: 0; margin: 12px 0; }
.flow-node {
  padding: 18px 30px; border-radius: 12px;
  font-size: 18px; font-weight: 600; white-space: nowrap;
}
.flow-arrow {
  width: 56px; height: 2px; background: var(--accent);
  flex-shrink: 0; position: relative;
}
.flow-arrow::after {
  content: ''; position: absolute; right: -1px; top: -5px;
  border: 6px solid transparent; border-left: 7px solid var(--accent);
}

/* Node color variants */
.node-primary { background: rgba(29,71,63,0.5); border: 1px solid var(--accent); color: var(--accent2); }
.node-secondary { background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.3); color: #818cf8; }
.node-pink { background: rgba(236,72,153,0.1); border: 1px solid rgba(236,72,153,0.3); color: #f472b6; }
.node-red { background: rgba(239,68,68,0.1); border: 1px solid rgba(239,68,68,0.3); color: #fca5a5; }
```

HTML usage:
```html
<div class="flow-row">
  <div class="flow-node node-primary">Step 1</div>
  <div class="flow-arrow"></div>
  <div class="flow-node node-secondary">Step 2</div>
  <div class="flow-arrow"></div>
  <div class="flow-node node-pink">Step 3</div>
</div>
```

## Timeline

Vertical numbered steps:

```css
.timeline { margin-top: 28px; position: relative; padding-left: 60px; }
.timeline::before {
  content: ''; position: absolute; left: 23px; top: 8px; bottom: 8px;
  width: 2px; background: linear-gradient(to bottom, var(--accent2), var(--accent));
}
.timeline-step { position: relative; margin-bottom: 32px; }
.timeline-step:last-child { margin-bottom: 0; }
.timeline-step .step-num {
  position: absolute; left: -60px; top: 0;
  width: 44px; height: 44px; border-radius: 50%;
  background: var(--surface); border: 2px solid var(--accent2);
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 700; color: var(--accent2);
  font-family: 'JetBrains Mono', monospace; z-index: 1;
}
.timeline-step .step-content {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px 24px;
}
```

## Compare Cards

Before/After side-by-side:

```css
.compare-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }
.compare-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 14px; padding: 32px; position: relative; overflow: hidden;
}
.compare-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 4px; }
.compare-card.before::before { background: var(--red); }
.compare-card.after::before { background: var(--green); }
.compare-label {
  font-size: 12px; font-weight: 700; text-transform: uppercase;
  letter-spacing: 2px; margin-bottom: 16px;
}
.compare-card.before .compare-label { color: var(--red); }
.compare-card.after .compare-label { color: var(--green); }
.compare-item {
  display: flex; align-items: flex-start; gap: 12px;
  padding: 10px 0; border-bottom: 1px solid var(--border);
  font-size: 15px; color: var(--text2);
}
.compare-callout {
  margin-top: 16px; padding-top: 16px; border-top: 1px solid var(--border);
  font-size: 14px; font-weight: 600; font-style: italic;
}
```

## Stat Cards

Big number metrics:

```css
.stat-row { display: flex; gap: 20px; }
.stat-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 24px 32px; text-align: center; flex: 1;
}
.stat-number {
  font-size: 48px; font-weight: 700; letter-spacing: -2px; line-height: 1;
  color: var(--accent2); font-family: 'JetBrains Mono', monospace;
}
.stat-label { font-size: 13px; color: var(--text2); margin-top: 8px; font-weight: 500; }
```

## Classification Grid

Color-coded category cards (2x2):

```css
.class-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; }
.class-card {
  background: var(--surface); border: 1px solid var(--border);
  border-radius: 12px; padding: 20px; position: relative; overflow: hidden;
}
.class-card::before { content: ''; position: absolute; top: 0; left: 0; right: 0; height: 3px; }
/* Apply color per category with additional class */
```

## Status Badges & Pills

```css
.badge {
  display: inline-block; padding: 4px 12px; border-radius: 6px;
  font-size: 12px; font-weight: 600;
}
.badge-green { background: rgba(34,197,94,0.15); color: var(--green); }
.badge-orange { background: rgba(245,158,11,0.15); color: var(--orange); }
.badge-red { background: rgba(239,68,68,0.15); color: var(--red); }
.badge-blue { background: rgba(59,130,246,0.15); color: var(--blue); }

.pill {
  padding: 8px 16px; border-radius: 8px; font-size: 13px; font-weight: 600;
}
```

## Slide Navigation JavaScript

Complete slide presentation engine:

```html
<!-- Required HTML structure -->
<div class="progress-bar" id="progressBar"></div>

<div class="slide active" data-slide="0"><!-- content --></div>
<div class="slide" data-slide="1"><!-- content --></div>

<!-- Speaker notes (optional, per slide) -->
<div class="speaker-notes" data-notes="0">Notes for slide 0</div>

<div class="nav-footer">
  <div class="brand">BRAND NAME</div>
  <div class="nav-dots" id="navDots"></div>
  <div class="slide-count" id="slideCount"></div>
</div>

<div class="key-hint">
  <div class="key">&#8592;</div>
  <div class="key">&#8594;</div>
</div>
```

```css
/* Slide base */
.slide {
  position: absolute; top: 0; left: 0; width: 100%; height: 100%;
  display: flex; flex-direction: column; justify-content: center;
  padding: 60px 80px;
  opacity: 0; pointer-events: none;
  transition: opacity 0.45s ease, transform 0.45s ease;
  transform: translateX(30px);
}
.slide.active { opacity: 1; pointer-events: auto; transform: translateX(0); }
.slide.exiting { opacity: 0; transform: translateX(-30px); }

/* Scrollable slides (for dense content) */
.slide-scroll { max-height: calc(100vh - 160px); overflow-y: auto; padding-right: 16px; }
.slide-scroll::-webkit-scrollbar { width: 4px; }
.slide-scroll::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }

/* Progress bar */
.progress-bar {
  position: fixed; top: 0; left: 0; height: 3px; z-index: 100;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

/* Footer nav */
.nav-footer {
  position: fixed; bottom: 0; left: 0; right: 0;
  display: flex; justify-content: space-between; align-items: center;
  padding: 16px 80px; background: linear-gradient(transparent, var(--bg)); z-index: 50;
}
.nav-dots { display: flex; gap: 6px; }
.dot { width: 8px; height: 8px; border-radius: 50%; background: var(--border); cursor: pointer; transition: all 0.3s; }
.dot.active { background: var(--accent2); width: 24px; border-radius: 4px; }

/* Speaker notes */
.speaker-notes {
  position: fixed; bottom: 50px; left: 80px; right: 80px;
  background: rgba(0,0,0,0.92); border: 1px solid var(--border); border-radius: 12px;
  padding: 20px 24px; font-size: 14px; color: var(--text2); line-height: 1.6;
  z-index: 200; display: none; max-height: 160px; overflow-y: auto;
}
.speaker-notes.visible { display: block; }
```

```javascript
const slides = document.querySelectorAll('.slide');
const progressBar = document.getElementById('progressBar');
const slideCount = document.getElementById('slideCount');
const navDots = document.getElementById('navDots');
let current = 0;
const total = slides.length;
let notesVisible = false;

// Build nav dots
for (let i = 0; i < total; i++) {
  const dot = document.createElement('div');
  dot.className = 'dot' + (i === 0 ? ' active' : '');
  dot.addEventListener('click', () => goTo(i));
  navDots.appendChild(dot);
}

function updateUI() {
  progressBar.style.width = ((current + 1) / total * 100) + '%';
  slideCount.textContent = (current + 1) + ' / ' + total;
  document.querySelectorAll('.dot').forEach((d, i) => {
    d.className = 'dot' + (i === current ? ' active' : '');
  });
  document.querySelectorAll('.speaker-notes').forEach(n => {
    n.classList.toggle('visible', notesVisible && n.dataset.notes == current);
  });
}

function goTo(index) {
  if (index < 0 || index >= total || index === current) return;
  const prev = current;
  slides[prev].classList.remove('active');
  slides[prev].classList.add('exiting');
  current = index;
  slides[current].classList.add('active');
  setTimeout(() => slides[prev].classList.remove('exiting'), 450);
  updateUI();
}

document.addEventListener('keydown', (e) => {
  if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); goTo(current + 1); }
  if (e.key === 'ArrowLeft') { e.preventDefault(); goTo(current - 1); }
  if (e.key === 'n' || e.key === 'N') { notesVisible = !notesVisible; updateUI(); }
});

updateUI();
```

## Tab Navigation JavaScript

For multi-view dashboards:

```html
<div class="nav">
  <button class="active" onclick="showView('overview')">Overview</button>
  <button onclick="showView('details')">Details</button>
  <button onclick="showView('comparison')">Comparison</button>
</div>

<div class="content">
  <div class="view active" id="view-overview"><!-- content --></div>
  <div class="view" id="view-details"><!-- content --></div>
  <div class="view" id="view-comparison"><!-- content --></div>
</div>
```

```css
.nav { display: flex; gap: 4px; border-bottom: 1px solid var(--border); }
.nav button {
  padding: 10px 20px; background: none; border: none; color: var(--text2);
  font-size: 14px; font-weight: 500; cursor: pointer;
  border-bottom: 2px solid transparent; position: relative; bottom: -1px;
  font-family: inherit; transition: all 0.2s;
}
.nav button:hover { color: var(--text); }
.nav button.active { color: var(--accent2); border-bottom-color: var(--accent); }

.view { display: none; }
.view.active { display: block; }
```

```javascript
function showView(name) {
  document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
  document.querySelectorAll('.nav button').forEach(b => b.classList.remove('active'));
  document.getElementById('view-' + name).classList.add('active');
  event.target.classList.add('active');
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
```

## Light Theme UI Mockups

When embedding UI mockups inside dark-themed slides (e.g., showing what a product screen looks like):

```css
.mockup {
  background: #f8f8f8; border: 1px solid #ddd;
  border-radius: 12px; padding: 24px; color: #222;
}
.mockup-field-label { font-size: 12px; font-weight: 600; color: #444; margin-bottom: 6px; }
.mockup-field-value {
  background: #fff; border: 1px solid #ddd; border-radius: 8px;
  padding: 10px 14px; font-size: 13px; color: #333;
}
.mockup-field-value.highlight {
  border-color: var(--accent); background: rgba(61,155,122,0.06);
}
```
