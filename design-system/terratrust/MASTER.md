# TerraTrust Design System — Immersive Editorial Variant

This reversible variant was created on August 9, 2026 on branch `codex/immersive-terra-design`. The previous calm light interface remains recoverable from commit `7d2bb82` on `main`.

## Direction

- Product: a responsible land-cover verification instrument, not a generic AI landing page.
- Tone: cinematic, sober, environmental, and accountable.
- Adapted reference qualities: near-black canvas, Instrument Serif display type, atmospheric depth, a restrained glass header, generous space, and editorial scale.
- Preserve: all four working destinations, source selection, uploads, API inference, probability output, Human verification queue, validation evidence, limitations, and deployment plan.
- Avoid: unrelated agency copy, email capture, pricing, autoplay background video, fake maps, neon AI glows, pill overload, bento walls, decorative motion, and unsupported environmental claims.

## Tokens

| Role | Value | Use |
|---|---|---|
| Canvas | `#090B09` | Page background |
| Surface | `#111410` | Product workspaces |
| Raised surface | `#171B16` | Optional hierarchy |
| Ink | `#F2F3ED` | Primary text |
| Muted | `#A7ACA2` | Supporting text |
| Line | `rgba(242,243,237,.14)` | Internal rules |
| Strong line | `rgba(242,243,237,.32)` | Workspace boundaries |
| Field | `#B8D58F` | Primary actions |
| Review | `#EFB16F` | Human-verification state |
| Error | `#FF8F82` | Recoverable errors |

Display headings use Instrument Serif with Georgia fallback. Interface copy uses Roboto with Arial fallback. Roboto Mono is reserved for filenames, provenance, and small factual metadata.

## Structure

- Header: a plain ruled wordmark/navigation row with no badge, descriptor, glass shell, or decorative framing.
- Overview: viewport-scale product statement over a custom-generated oblique forest photograph. The image is decorative and is never presented as analyzed evidence or a real monitored location.
- Analyze: stable two-column source/result workspace; atmosphere never competes with task controls.
- Human verification: ruled operational queue.
- Validation: native tables, chart, metric strip, SDG contribution chain, limits, and deployment plan.
- Footer: explicit product boundary.

## Motion and accessibility

- One 280ms opacity/translate view entrance using `LazyMotion` and `domAnimation`.
- Motion variants live outside React components to prevent recreation.
- `useReducedMotion` skips the initial offset, and CSS enforces reduced-motion preferences.
- No scroll-linked motion, autoplay media, parallax, or continuous decorative animation.
- Native semantic controls, visible focus rings, textual status labels, 44px minimum targets, and horizontally scrollable data tables remain required.

## Reversibility

- Current experiment: branch `codex/immersive-terra-design`.
- Known-good light version: commit `7d2bb82` on `main`.
- To inspect the old design without deleting this work: `git switch main`.
- To return to this variant: `git switch codex/immersive-terra-design`.

## Rubric intent

The visual direction supports Presentation Quality without hiding Technical Execution. Measured evidence remains more prominent than decorative material, and projected or unmeasured outcomes remain labeled.
