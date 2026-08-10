# Interface Design and QA Evidence

Date: August 9, 2026  
Rubric rows supported: Presentation Quality, Technical Execution, Creative AI Use

## Design intent

TerraTrust uses a calm, compact management-tool interface so judges can understand the review policy and verify evidence quickly. The visual system is documented in `design-system/terratrust/MASTER.md`.

- Compact masthead, restrained serif hierarchy, and one framed analysis workspace.
- Warm paper, near-black type, thin rules, one field-green action surface, and amber review states.
- Square geometry, no shadows, gradients, glass, decorative AI motifs, or generic card wall.
- Newsreader display headings, Roboto interface copy, and limited monospace metadata with system fallbacks.
- Status always combines icon, text, and color.
- Direct numerical labels and an HTML table keep evidence readable without hover.

## Tool-assisted review

UI/UX Pro Max was used to refine the persistent design system, check accessible chart patterns, and run the required `animation accessibility z-index loading` validation search. Generic dashboards, exaggerated minimalism, and AI-native treatments were rejected.

The final pass removed Framer Motion components from the rendered interface. Screen changes are direct React state updates; the loading spinner is the only continuous animation. A CSS reduced-motion fallback remains.

The installed 21st CLI 1.15.1 ran `review frontend/src --strict --json`:

| Finding level | Count |
|---|---:|
| Errors | 0 |
| Warnings | 0 |
| Suggestions | 15 |

The suggestions are informational hardcoded-color checks. Most identify centralized `:root` token declarations; the rest are intentional state surfaces. No component-specific palette was introduced. 21st AI sketch generation was not used because the CLI was not authenticated; this boundary is disclosed in `docs/ai-use-log.md`.

## Final reference-based refinement

The final interface follows the concrete rhythm of the local Iris Hackathon reference: a compact frame, small masthead, serif display type, thin rules, subdued surfaces, and one framed workspace. It removes the previous showcase hero, reference-image hero card, numbered concepts, page choreography, dashboard cards, and promotional microcopy. Technical performance remains under **Validation** rather than acting as the product headline.

## Functional and responsive QA

| Check | Evidence | Result |
|---|---|---|
| Production build | Vite 6.4.3, 1,980 modules transformed | Pass |
| Frontend interaction test | Vitest + Testing Library | 1/1 pass |
| Python/model/API tests | Pytest | 11/11 pass |
| Live health | `/api/health` | model ready; frontend ready |
| Core model path | API/model tests plus preserved accepted/review routing | Pass |
| Desktop visual inspection | Isolated 1280x900 render of overview and analysis | Pass |
| Narrow-layout visual inspection | Isolated 500x812 render with mobile breakpoint active | Pass |
| Exact 375px inspection | Live-preview controller unavailable during the final reference-based pass | Manual verification required |
| Touch targets | CSS minimum plus interaction test inspection | 44px minimum defined |
| Browser console | Not re-measured after the final reference-based pass | Manual verification required |
| Empty/loading/error states | Interface and API paths | Present |

The final narrow render uses four plain navigation labels and hides the secondary masthead descriptor to preserve space. An exact 375px manual pass remains required because the isolated Windows browser enforces a wider minimum layout viewport.

## Remaining human checks

- Run an exact 375px pass in the live browser, plus screen-reader and 200% zoom checks.
- Test on at least one physical phone and a second desktop browser.
- Build and run the included Docker image on a machine with Docker; Docker was unavailable locally.
- Conduct the planned usability sessions with real participants; do not invent outcomes.
- Rehearse and record the final 2-3 minute demo with all team members represented.
