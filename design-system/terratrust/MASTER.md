# TerraTrust Design System

Source of truth for the interface. Refined on August 9, 2026 using the local Iris Hackathon interface as the concrete reference and the requested calm management-tool character as the secondary direction.

## Direction

- Product: a land-cover review instrument, not a marketing site.
- Tone: calm, practical, quiet, and accountable.
- Reference qualities: compact 1240px frame, serif display type, warm paper, thin rules, plain controls, and one focused workspace.
- Avoid: abstract hero art, gradients, glass, shadows, soft card walls, bento grids, numbered steps, agency labels, oversized slogans, decorative animation, fake maps, and AI-product motifs.
- Use real product states and measured evidence as the visual content.

## Tokens

| Role | Value | Use |
|---|---|---|
| Paper | `#F4F3EE` | Page background |
| Surface | `#FBFAF6` | Analysis workspace |
| Ink | `#20231E` | Primary text and strong rules |
| Muted | `#666A62` | Supporting copy |
| Line | `#D1D2CB` | Internal separators |
| Line dark | `#9A9E95` | Control borders |
| Field | `#B8C99B` | Primary action surface |
| Field dark | `#526342` | Focus and accepted state |
| Review | `#8A4D1F` | Human-review state |
| Error | `#9F2F25` | Recoverable errors |

Display headings use Newsreader with Georgia fallback. Interface copy uses Roboto with Arial fallback. Roboto Mono is reserved for filenames and small factual metadata.

Spacing follows a 4/8px rhythm. The page width is `min(100% - 40px, 1240px)` on desktop and `100% - 32px` on phones.

## Structure

- Masthead: small TT mark, wordmark, and one quiet product descriptor.
- Navigation: four plain text destinations under the masthead.
- Overview: one concise serif statement, one text action, and three ruled workflow lines.
- Analyze: one bordered two-column workspace. Source and controls stay left; the result stays right.
- Review: a ruled list, never a stack of floating cards.
- Validation: one metric strip followed by report-like sections and a native HTML table.
- Footer: short product boundary statement.

## Interaction

- Native semantic controls only.
- Minimum target height: 44px.
- One primary action in each task area.
- Loading is the only continuous animation.
- No Framer Motion components or decorative entrance transitions in the current interface.
- Reduced-motion CSS remains as a safety fallback.
- Status always uses text and an icon in addition to color.

## Responsive behavior

- Above 900px: two-column analysis workspace and validation layout.
- At 900px: workspaces become one column.
- At 640px: compact four-column navigation, stacked actions, two-by-two metrics, and simplified queue rows.
- At 375px: no page-level horizontal scrolling and all controls remain at least 44px high.

## Rubric intent

The restrained design supports Presentation Quality and Technical Execution by keeping the working analysis, review handoff, measured results, error states, and limitations easy to verify. Styling never implies environmental outcomes or deployment readiness that have not been measured.
