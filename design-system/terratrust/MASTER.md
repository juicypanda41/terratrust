# TerraTrust Design System

Source of truth for the hackathon interface. Generated from UI/UX Pro Max searches on August 9, 2026, then intentionally narrowed by the team to avoid a generic dashboard aesthetic.

## Direction

- Product: responsible scientific decision-support tool.
- Style: Swiss Modernism 2.0 × editorial field report.
- Tone: measured, auditable, direct, human.
- Avoid: gradients, glassmorphism, floating decoration, soft card grids, neon, oversized pill controls, fake maps, decorative AI motifs, and color-only states.
- Geometry: 1px rules, 1px radius, no shadows. Circles are reserved for the decision-policy diagram and queue count.

## Tokens

| Role | Value | Use |
|---|---|---|
| Paper | `#F4F1E8` | Page background |
| Paper deep | `#E9E5DA` | Selected and hover surfaces |
| Ink | `#171914` | Primary type, rules, primary action |
| Muted | `#5C6157` | Secondary copy; verify 4.5:1 at body sizes |
| Field green | `#155F3E` | Primary accent and accepted state |
| Field green dark | `#0F4B31` | High-contrast green text/action |
| Review amber | `#9D5212` | Review state, always paired with icon and text |
| Error | `#A12B24` | Recoverable errors, paired with explanation |
| White | `#FFFEFA` | Text on dark actions and image stage |

Typography uses the system Helvetica/Arial stack for a fast, unbranded editorial voice and a system monospace stack for indices, metadata, and evidence labels. Body text is at least 16px on mobile with 1.5 line height. Data uses tabular figures.

Spacing follows an 8px base: 8 / 16 / 24 / 32 / 48 / 64 / 96. Desktop content is capped at 1440px; mobile gutters are 16–20px.

## Components

- Header: wordmark, four labeled destinations, active underline, track label.
- Metrics: a ruled ledger, not detached cards.
- Buttons: rectangular, 48px minimum height, single primary action per view.
- Status: icon + text + accessible color; green means eligible, amber means review.
- Charts: direct values and text alternatives; green lines/bars, amber target markers; no gradients.
- Images: fixed aspect ratio and dimensions to prevent layout shift.
- Empty/error/loading states: explicit next action and `aria-live` where appropriate.

## Motion

- Framer Motion `LazyMotion` with `domAnimation`; never import `motion`.
- Only view transitions, result entry/exit, queue entry/exit, and press feedback.
- Transform and opacity only, 140–240ms, stable variants outside components.
- Honor system reduced-motion preferences through `MotionConfig` and CSS.

## Responsive behavior

- 1440px: editorial asymmetric grid.
- 1024px: analysis result moves below input/image pair.
- 768px: navigation becomes a labeled horizontal strip; all main grids become one column.
- 375px: metrics become a one-column ledger and charts/tables remain readable without page-level horizontal scroll.

## Evidence and rubric intent

The interface prioritizes the Presentation Quality and Technical Execution rows in `docs/judging-scorecard.md`: a clear problem/solution story, reliable core demo, readable held-out metrics, error handling, scope boundaries, and a visible human-review handoff. Styling never implies measured impact that the project has not established.
