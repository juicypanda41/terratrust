# Interface Design and QA Evidence

Date: August 9, 2026  
Rubric rows supported: Presentation Quality, Technical Execution, Creative AI Use

## Design intent

TerraTrust uses a restrained scientific-editorial interface so judges can understand the decision policy and verify evidence quickly. The visual system is documented in `design-system/terratrust/MASTER.md`.

- Swiss/editorial grid with asymmetric briefing layout.
- Warm paper background, near-black type and rules, one field-green action color, and amber review states.
- Square geometry, no shadows, no gradients, no glass surfaces, no decorative AI motifs, and no generic card wall.
- System sans-serif typography plus monospace evidence labels; no blocking font request.
- Status always combines icon, text, and color.
- Direct numerical labels and HTML table alternatives keep evidence legible without hover.

## Tool-assisted review

UI/UX Pro Max was used to generate a persistent design system, query citizen-science palettes, compare Swiss/editorial styles, select accessible chart types, and run the required `animation accessibility z-index loading` validation search. Its generic blue dashboard result was rejected in favor of a context-specific system.

Framer Motion follows the requested performance rules:

- `LazyMotion` with `domAnimation` and the `m` component.
- Stable variants defined outside render functions.
- Transform and opacity animations only.
- Motion limited to view changes, result/queue entry, and press feedback.
- `MotionConfig reducedMotion="user"` plus a CSS reduced-motion fallback.

The installed 21st CLI 1.15.1 ran `review src --strict --json` against the frontend:

| Finding level | Count |
|---|---:|
| Errors | 0 |
| Warnings | 0 |
| Suggestions | 20 |

All suggestions were informational hardcoded-color checks. Thirteen pointed to the centralized `:root` token declarations; the remainder were intentional state/fallback literals. No scattered component palette was introduced. 21st AI sketch generation was not used because the CLI was not authenticated; this boundary is disclosed in `docs/ai-use-log.md`.

## Functional and responsive QA

| Check | Evidence | Result |
|---|---|---|
| Production build | Vite 6.4.3, 1,980 modules transformed | Pass |
| Frontend interaction test | Vitest + Testing Library | 1/1 pass |
| Python/model/API tests | Pytest | 11/11 pass |
| Live health | `/api/health` | model ready; frontend ready |
| Core demo | Ambiguous `Highway_2.jpg` → 46.0% confidence → review queue | Pass |
| Desktop visual inspection | 1265px browser viewport | Pass |
| Small phone | 375×812 override; rendered client width 360px | Pass |
| Page/navigation overflow | scroll width equals client width | None |
| Touch targets | visible buttons measured in screen flow | None below 44×44px |
| Browser console | warnings and errors | None |
| Empty/loading/error states | interface and API paths | Present |

The first mobile inspection exposed a horizontal navigation scrollbar. The navigation was changed to a two-by-two labeled index and retested with equal scroll/client widths.

## Remaining human checks

- Run a real screen-reader pass and 200% browser zoom pass.
- Test on at least one physical phone and a second desktop browser.
- Build and run the included Docker image on a machine with Docker; Docker was unavailable in the local test environment.
- Conduct the planned usability sessions with real participants; do not invent outcomes.
- Rehearse and record the final 2–3 minute demo with all team members represented.
