# TerraTrust Design System

Source of truth for the hackathon interface. Refined on August 9, 2026 after direct product review.

## Direction

- Product: responsible scientific decision-support tool.
- Style: quiet, utilitarian, and product-led.
- Tone: direct, measured, and human.
- Avoid: gradients, glass, abstract hero art, decorative motion, numbered navigation, agency-style labels, oversized slogans, soft card grids, fake maps, AI motifs, and color-only states.
- Geometry: 1px rules, 1px radius, and no shadows.
- Homepage principle: show the actual screening workflow. Keep dataset names, sample counts, model terminology, and event language in documentation or validation—not in the product introduction.

## Tokens

| Role | Value | Use |
|---|---|---|
| Paper | `#F4F1E8` | Page background |
| Paper deep | `#E9E5DA` | Selected and hover surfaces |
| Ink | `#171914` | Primary type, rules, primary action |
| Muted | `#5C6157` | Secondary copy |
| Field green | `#155F3E` | Primary accent and accepted state |
| Field green dark | `#0F4B31` | High-contrast green text/action |
| Review amber | `#9D5212` | Review state, paired with icon and text |
| Error | `#A12B24` | Recoverable errors, paired with explanation |
| White | `#FFFEFA` | Text on dark actions and image stages |

Typography uses the system Helvetica/Arial stack. Body text is at least 16px on mobile with 1.5 line height. Numerical evidence uses tabular figures.

Spacing follows an 8px base: 8 / 16 / 24 / 32 / 48 / 64 / 96. Desktop content is capped at 1440px; mobile gutters are 16–20px.

## Components

- Header: wordmark and four plainly labeled destinations with a restrained active underline.
- Hero: one concise product statement, one action, and one real reference scene from the working demo.
- Homepage workflow: three plain-language outcomes separated by rules; no diagram or decorative illustration.
- Buttons: rectangular, 48px minimum height, with one primary action per view.
- Status: icon + text + accessible color; green means eligible and amber means review.
- Charts: direct values and text alternatives; no gradients or hover-only meaning.
- Images: fixed aspect ratio and dimensions to prevent layout shift.
- Empty, error, and loading states: explicit next action and `aria-live` where appropriate.

## Motion

- Framer Motion `LazyMotion` with `domAnimation`; never import `motion`.
- Motion is functional only: view changes, result/queue entry and exit, and press feedback.
- Transform and opacity only, 140–240ms, with stable variants outside components.
- Honor system reduced-motion preferences through `MotionConfig` and CSS.

## Responsive behavior

- 1440px: two-column product introduction and three-column analysis workspace.
- 1024px: analysis result moves below the input/image pair.
- 768px: navigation becomes a two-by-two labeled grid and main layouts become one column.
- 375px: charts and tables remain readable without page-level horizontal scrolling.

## Evidence and rubric intent

The interface supports the Presentation Quality and Technical Execution rows in `docs/judging-scorecard.md`: a clear problem/solution story, reliable core demo, readable held-out metrics, error handling, scope boundaries, and a visible human-review handoff. Styling never implies measured impact that the project has not established.
