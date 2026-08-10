# TerraTrust - Submission-Grade Project Brief

## One-line pitch

**TerraTrust helps environmental monitoring teams triage Sentinel-2 land imagery safely: it classifies clear land-cover tiles automatically, explains its confidence, and sends ambiguous cases to a human review queue instead of guessing.**

## Selected track

Technical Track.

## Why this version can stand out

A basic EuroSAT classifier is a common benchmark exercise. TerraTrust turns that model into a decision workflow and makes reliability the differentiator:

1. Predict one of EuroSAT's 10 land-cover classes.
2. Calibrate the model so confidence corresponds more closely to observed correctness.
3. Auto-accept sufficiently reliable cases.
4. Abstain and send uncertain cases to a human review queue.
5. Show the measurable tradeoff between workload reduction and error risk.

The product is not presented as a replacement for environmental experts. It is a screening layer that lets limited human attention focus on difficult imagery.

## Problem and intended user

Land-cover information supports forestry, agriculture, water management, urban planning, environmental protection, and crisis response. Sentinel-2 produces frequent multispectral observations, but turning imagery into reliable decisions requires technical expertise and quality control.

Primary user for the prototype: a small environmental organization, student research team, or GIS analyst who needs to sort satellite tiles before expert review.

The user's decision is concrete: **Which tiles are safe to classify automatically, and which require human attention?**

## Product experience

### Screen 1 - Overview

- Concise explanation of the land-cover screening and human-checkpoint workflow.
- One real reference scene that opens the analysis path.
- Plain-language distinction between a clear result, an uncertain result, and an unverified source.

### Screen 2 - Analyze a tile

- Choose a held-out example or upload a compatible RGB Sentinel-2 tile.
- Image preview and predicted class.
- Top two classes with calibrated probabilities.
- Decision badge: `Auto-accept` or `Human review required`.
- Plain-language reason for the routing decision.
- Full class-probability comparison and local inference time.
- Unverified uploaded imagery always remains in review.

### Screen 3 - Human Verification

- Preserve the source, prediction, confidence, and review reason for each flagged scene.
- Let the reviewer remove a completed item from the local demo queue.

### Screen 4 - Validation

- Held-out overall accuracy, macro F1, accepted-case accuracy, coverage, and sample size.
- Calibration error before and after temperature scaling.
- Risk-coverage curve showing the accuracy/workload tradeoff.
- Controlled quality stress-test table with explicit scope language.
- Clear operational limitations and SDG contribution boundary.

## Primary measurable claim

Choose a target accepted-case accuracy using only the validation set, then lock the threshold before final test evaluation.

Measured result:

> On the held-out EuroSAT RGB test set (n = 4,050), TerraTrust achieved 91.4% accuracy on the 78.9% of scenes accepted by the complete confidence-plus-quality policy, while routing 21.1% to human review. Calibration changed expected calibration error from 2.55% to 0.87%, and median warm local CPU inference was 16.2 ms across 100 images.

Never fill these values with projections. Generate them from the final reproducible evaluation.

## Required experiments

### E1 - Reproducible classification baseline

- Use a published or fixed train/validation/test split and record exact sample counts.
- Train the documented deterministic RGB feature pipeline with a histogram gradient-boosting classifier on ordinary hardware.
- Report accuracy, macro F1, per-class metrics, and confusion matrix.
- Fix random seeds and save configuration, weights, and evaluation outputs.

### E2 - Confidence calibration

- Fit temperature scaling on validation predictions only.
- Compare negative log likelihood, Brier score, and expected calibration error before/after.
- Plot a reliability diagram.

### E3 - Selective prediction/human review

- Select the abstention threshold on validation data.
- Report test coverage, selective accuracy, review rate, and a risk-coverage curve.
- Include examples where abstention prevented a confident-looking mistake and examples the system still gets wrong.

### E4 - Robustness check

- Evaluate controlled blur, brightness, contrast, and noise transformations without pretending these cover every real-world shift.
- Test whether corrupted images receive lower confidence or higher review rates.
- Document failure modes.

### E5 - RGB versus multispectral stretch experiment (not implemented)

- Compare models only with the same split and evaluation protocol.
- Record preprocessing for all 13 bands and avoid using RGB pretrained weights as an unfair direct comparison without explanation.
- If this experiment is incomplete or invalid, omit it from the headline demo instead of overstating results.

### E6 - Small usability validation

- Ask 5-8 target-adjacent testers to complete a short review task.
- Record consent, role/background, task completion, time, misinterpretations, and one short feedback question.
- Report the sample size and limitations. Do not call non-experts professional GIS users.

## Metric hierarchy

### Headline metrics

1. Selective accuracy on auto-accepted test cases.
2. Coverage/workload reduction at that accuracy.
3. Review rate.

### Technical guardrails

- Macro F1 and worst-class recall.
- Expected calibration error, Brier score, and negative log likelihood.
- Corruption review-rate change.
- Median and p95 inference latency.
- Model size and peak memory if available.

### Usability evidence

- Task completion rate.
- Median time to reach a review decision.
- Percentage who correctly understand that the prediction is not a final environmental determination.
- Qualitative feedback themes with anonymized notes.

## SDG alignment and theory of change

Primary target: **SDG 15.1**, conservation, restoration, and sustainable use of terrestrial and inland freshwater ecosystems.

Secondary target: **SDG 15.2**, sustainable forest management and efforts to halt deforestation.

Evidence chain:

`Sentinel-2 imagery` -> `land-cover screening` -> `uncertain cases prioritized for expert review` -> `faster, more consistent inventory workflow` -> `better information for ecosystem and forest monitoring decisions`.

This is an enabling contribution, not evidence that TerraTrust has already conserved land. The prototype metrics measure screening reliability and workload reduction. Any future conservation outcome remains a projected downstream result requiring field validation and temporal data.

Authoritative context:

- UN Goal 15 targets and indicators: https://sdgs.un.org/goals/goal15
- ESA Sentinel-2 applications: https://www.esa.int/Applications/Observing_the_Earth/Copernicus/Sentinel-2/Changing_lands
- Official EuroSAT dataset: https://zenodo.org/records/7711810
- EuroSAT paper: https://arxiv.org/abs/1709.00029

## Architecture

```text
       EuroSAT RGB
          |
  reproducible data split
          |
 model training + evaluation
          |
 saved model + temperature scaler + threshold
          |
     inference service
       /          \
 auto-accept    review queue
       \          /
       evidence dashboard
```

Recommended hackathon stack:

- Python and scikit-learn for the evaluated model.
- FastAPI for a small typed model bridge and one production URL.
- React/Vite for a semantic, responsive presentation layer.
- Static React state changes with CSS loading and focus feedback only.
- Native SVG and HTML tables for accessible evidence displays.
- Pytest for preprocessing, inference-shape, threshold, and API/UI helper tests.
- JSON/CSV artifacts for reproducible metrics and demo examples.

Do not introduce a database, vector service, complex cloud stack, or live Sentinel ingestion until the core evidence workflow is reliable.

## Build priorities

### P0 - Must work for submission

- Reproducible RGB training/evaluation or a transparently documented pretrained checkpoint trained during the hackathon.
- Calibration and abstention threshold.
- Analyze-tile flow.
- Human review queue.
- Evidence dashboard using real saved outputs.
- Reliable local or hosted demo with graceful errors.
- README, architecture diagram, citations, model card, limitations, AI-use log, and tests.

### P1 - Strong differentiators

- Risk-coverage visualization.
- Corruption/robustness demonstration.
- Similar labeled examples.
- Small user-validation study.
- Batch upload and CSV report.

### P2 - Only if P0 and P1 are polished

- Fair RGB-versus-multispectral comparison.
- Map visualization using clearly identified sample coordinates.
- Hosted API.

## Rubric strategy

| Rubric row | Exceptional-level plan |
|---|---|
| Innovation & Impact | Define the risky behavior of always-predict classifiers; show multiple real test metrics, baseline comparison, failure examples, and a small user study. The core innovation is calibrated abstention plus a usable review workflow. |
| Technical Execution | Working end-to-end product; clean modules; fixed data split; documented architecture and rationale; saved artifacts; tests; loading/upload errors; calibrated model; reproducible evaluation. |
| SDG Alignment | Cite targets 15.1 and 15.2, UN baseline context, and ESA evidence that Sentinel-2 supports land-cover/forest monitoring. Present an honest theory of change and distinguish prototype outcomes from conservation outcomes. |
| Scalability | Batch inference today; future containerized API and object storage; quantify latency, memory, and estimated throughput; phase live Sentinel ingestion and region-specific validation; document assumptions and risks. |
| Presentation Quality | Use a single story: an easy forest tile is auto-accepted, an ambiguous vegetation tile is routed to review, and the dashboard proves the tradeoff. Rehearse to approximately 2:40. |
| Creative AI Use | Keep detailed prompts and tool/component mapping; explain human verification; measure time or defects saved where possible; explicitly identify interviews, ethical decisions, final claims, and approvals as human-owned. |

## Scaling plan

### Phase 1 - Hackathon prototype

- Single and small-batch EuroSAT tiles.
- Local/hosted inference.
- Benchmark users: students and small environmental teams.
- Reach target: 5-8 usability testers; report actual result.

### Phase 2 - Pilot

- Partner with one university lab, GIS club, or environmental nonprofit.
- Add Sentinel-2 ingestion, cloud masking, audit logs, and organization-specific thresholds.
- Validate against a spatially separate local dataset.
- Target and cost must be estimated with explicit assumptions.

### Phase 3 - Replication

- Containerized inference API and batch jobs.
- Region-specific models/model cards and drift monitoring.
- Review analytics and export to common GIS workflows.
- Funding route: university research partnership, environmental grant, or nonprofit pilot sponsorship.

## Major risks and mitigation

| Risk | Why it matters | Mitigation |
|---|---|---|
| Geographic distribution shift | EuroSAT is European; random test performance may not transfer globally | State scope, use a fixed split, run corruptions, require local pilot validation, and plan spatial holdouts/additional regional datasets |
| Scene labels are not segmentation | A 64x64 tile can contain mixed cover | Present scene classification only; do not calculate boundaries or acreage |
| No temporal pairs | EuroSAT cannot prove change | Do not claim change detection; add time-series Sentinel-2 data only in a later phase |
| Miscalibrated confidence | Users may interpret probability as certainty | Calibrate, abstain, display limitations, and test whether users understand the warning |
| Class imbalance/confusion | Aggregate accuracy can hide weak categories | Report macro F1, per-class recall, confusion matrix, and worst-class performance |
| Multispectral complexity | Band resolution/preprocessing can invalidate comparison | Document every transformation; make the experiment optional rather than endangering the MVP |
| Overclaiming SDG impact | Technical accuracy is not conservation impact | Separate measured prototype outcomes, projected operational outcomes, and unmeasured environmental outcomes |

## Demo storyboard - target 2:40

1. **0:00-0:20 - Problem:** Satellite land monitoring matters, but a model that guesses on every tile can create false confidence.
2. **0:20-0:35 - Solution:** TerraTrust classifies clear cases and refers uncertain cases to people.
3. **0:35-1:25 - Live demo:** Auto-accept an easy tile, route an ambiguous tile, show the reviewer workflow.
4. **1:25-1:55 - Evidence:** Show the held-out sample size, overall accuracy, macro F1, selective accuracy, coverage, calibration improvement, and controlled stress test.
5. **1:55-2:15 - SDG and impact:** Explain targets 15.1/15.2 and the honest enabling theory of change.
6. **2:15-2:30 - Scale and limitations:** Live Sentinel data, spatial validation, partner pilot; state that current prototype is European scene classification.
7. **2:30-2:40 - Close:** One memorable sentence and team contribution.

## Pitch close

> TerraTrust does not ask people to trust AI blindly. It measures when the model is dependable, exposes when it is not, and directs human attention to the satellite images that need it most.

## Competitive lessons from comparable projects

- FireWatch won First Overall with a sharply defined risk problem, a satellite-image model, and a complete frontend story: https://devpost.com/software/firewatch-2u5e4k
- EnviroHack paired satellite analysis with a coordinate-driven interface and visible environmental indices, winning a sponsor prize: https://devpost.com/software/envirohack
- Andromeda won a category prize by connecting a hard environmental problem to a demonstrable satellite/ML proof of concept and explaining its data challenge: https://devpost.com/software/andromeda

TerraTrust should borrow their focus and visual completeness, not their exact features. Its defensible distinction is measurable model reliability and human review rather than a broad collection of environmental claims.

## Hard no-claim list

Unless additional validated data and functionality are added, never claim TerraTrust:

- Detects deforestation or temporal land-use change.
- Produces pixel-level maps, boundaries, or acreage.
- Detects individual roads, buildings, trees, or objects.
- Measures carbon, biodiversity, crop health, wildfire risk, or water quality.
- Works reliably outside European-like EuroSAT imagery.
- Replaces GIS analysts, field surveys, or environmental experts.
- Has created real conservation impact.

## Submission readiness definition

TerraTrust is ready only when the demo works without intervention, every headline number regenerates from saved evaluation data, links open in a clean browser session, the video is 2-3 minutes, all claims have citations or measured evidence, limitations are visible, and `docs/judging-scorecard.md` has no unsupported exceptional-level claim.
