# Creative AI Use Log

Complete one entry for each meaningful AI-assisted component. Keep representative prompts detailed enough that judges can understand the task and constraints. Do not include secrets or personal data.

## Summary table

| Date/time | Tool/model | Component or artifact | Purpose | Human owner | Measurable outcome | Detailed entry |
|---|---|---|---|---|---|---|
| 2026-08-09 | OpenAI Codex | Project strategy, repository scaffold, application code, tests, and documentation | Accelerate implementation and rubric coverage | Team must assign | Measure after team review | Entry 1 |
| 2026-08-09 | OpenAI Codex + UI/UX Pro Max + Framer Motion guidance + 21st CLI | React/FastAPI interface redesign and review | Create a restrained, accessible, demo-ready interface | Team must assign | 0 errors / 0 warnings in 21st strict review; 12 automated tests after redesign | Entry 2 |

## Entry 1

- **Date/time:** 2026-08-09
- **Tool and model/version:** OpenAI Codex (exact served model version should be copied from the task UI if shown)
- **Component/element created:** TerraTrust concept refinement; model/evaluation pipeline; Streamlit interface; automated tests; VS Code configuration; GitHub/CI structure; README, model card, architecture, validation, deployment, and pitch documentation.
- **Why AI was appropriate:** Rapidly translated an explicit judging rubric and dataset constraints into a coherent, testable software architecture and documentation package during a short hackathon.
- **Representative detailed prompt:**

  > Using the attached OurPlanet.Rocks judging rubric and EuroSAT project notes, design and implement a Technical Track project that can satisfy each exceptional-level descriptor. Build a shareable GitHub/VS Code repository with a reproducible EuroSAT model pipeline, calibrated confidence, validation-selected human-review routing, a polished Streamlit demo, saved evidence artifacts, tests, architecture and model documentation, deployment instructions, SDG alignment, honest limitations, and a 2-3 minute demo plan. Do not fabricate metrics or claim segmentation, change detection, worldwide generalization, or environmental outcomes that EuroSAT cannot support.

- **Output used:** Repository files listed in the project README and `docs/` directory.
- **Human review and edits:** Required before submission. Team members must review claims, run the application, inspect metrics, approve design decisions, and personalize team/pitch content.
- **Validation performed:** Automated tests, real dataset training/evaluation, local application inspection, and clean-session link checks are required. Record the final completed evidence here.
- **Measurable outcome:** AI-assisted implementation produced a working repository and 6-test automated suite. Full EuroSAT evaluation reached 89.4% accuracy and 88.9% macro F1. The final confidence-plus-quality policy reached 91.4% accepted-case accuracy at 78.9% coverage. Browser QA found and corrected stale cached-policy evidence. Human usability outcomes remain pending.
- **Limitations/risks:** AI can introduce implementation errors, weak methodological assumptions, or inaccurate prose. All generated code and claims require human testing and source verification.
- **Artifact or commit link:** Add final GitHub repository and commit after publishing.

## Entry 2

- **Date/time:** 2026-08-09
- **Tools:** OpenAI Codex; UI/UX Pro Max local design database; Framer Motion performance guidance; 21st CLI 1.15.1.
- **Component/element created:** React/Vite presentation layer, FastAPI model bridge, responsive design tokens, semantic navigation, evidence visualizations, review-queue interaction, frontend/API tests, Docker packaging, and updated demo documentation.
- **Why AI was appropriate:** The team requested a fast visual redesign that remained technically traceable to the judging rubric and existing evaluated artifacts. The tools were used to generate constraints, critique implementation quality, and accelerate code—not to generate model results or user evidence.
- **Representative detailed prompt:**

  > Redesign TerraTrust as a minimal but creative scientific decision-support interface that does not look template-generated. Use 21st.dev, UI/UX Pro Max, and Framer Motion. Preserve the validated EuroSAT model, confidence-plus-quality review policy, held-out metrics, human-review handoff, limitations, and full rubric evidence. Avoid gradients, glassmorphism, decorative AI motifs, excessive cards, fabricated claims, and gratuitous animation. Use semantic React, accessible contrast and focus, 44px controls, mobile behavior at 375px, reduced-motion support, clear errors/loading/empty states, and a single production URL backed by the Python model.

- **Output used:** `frontend/`, `api.py`, `design-system/terratrust/MASTER.md`, `tests/test_api.py`, `Dockerfile`, VS Code/CI files, and related documentation edits.
- **Human-directed design decisions:** The user explicitly requested minimalism, creativity, and removal of an AI-generated aesthetic. The implementation selected Swiss/editorial structure, warm paper, square geometry, a single green action accent, and amber review states. UI/UX Pro Max's first generic blue-dashboard palette was rejected as a poor product fit.
- **Validation performed:** UI/UX Pro Max design-system and accessibility searches; Framer Motion rule checks; production Vite build; one frontend interaction test; ten Python/API/model tests; strict 21st local review; desktop visual inspection; 375px responsive inspection; full ambiguous-tile-to-review-queue browser flow; browser console check.
- **Measured outcome:** Production build succeeded. Automated tests passed (1 frontend + 11 Python). 21st strict review returned 0 errors and 0 warnings; its 20 informational findings were token declarations or deliberate CSS fallback colors. At 375px there was no page or navigation overflow and no visible button measured below 44×44px. Browser logs contained no warnings or errors.
- **21st boundary:** 21st AI sketch generation was attempted but the CLI had no authenticated account, and the browser login did not complete. No generated 21st take is claimed. The installed 21st deterministic local reviewer was used successfully.
- **Limitations/risks:** Automated accessibility and visual review cannot replace real user testing, assistive-technology testing, or judging. The React production bundle is larger than the former Python-only presentation; its animation features are lazy-scoped and the measured model latency is unchanged.
- **Artifact or commit link:** Add final GitHub repository and redesign commit after publishing.

## Where AI was not used

Document human-owned work and the reason it stayed human-led, such as firsthand interviews, final ethical decisions, consent, source verification, judging claims, original team opinions, or final approval.

| Work | Human owner | Why AI was not used | Evidence |
|---|---|---|---|
| Firsthand usability interviews and consent | Team member | These require real human participation and ethical handling | Add anonymized study record |
| Final factual and judging claims | Team member | The submitting team is accountable for accuracy | Final scorecard review |
| Final product and submission approval | Team member | AI must not submit or represent the team without approval | Submission checklist |

## AI quality and safety checks

- [ ] Every factual claim generated with AI was checked against a credible source.
- [ ] No private, identifying, copyrighted, or confidential data was entered without permission.
- [ ] Generated code/content was reviewed and tested by a team member.
- [ ] AI contributions are attributed honestly and do not misrepresent originality.
- [ ] Prompts, rationale, outcomes, and non-AI boundaries are ready to summarize in the pitch.
