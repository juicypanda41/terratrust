# Scalability and Deployment Plan

This is a technical plan, not evidence of production deployment. Projections are derived from the measured local CPU p95 latency of 22.3 ms per image and must be replaced by hosted load-test results before a pilot claim is made.

## Assumptions

| Assumption | Planning value | Reason / validation needed |
|---|---:|---|
| Unit of work | One 64×64 RGB scene | Matches the evaluated model contract |
| Worker latency | 22.3 ms p95 | Measured locally across 100 warm runs |
| Theoretical worker throughput | 44 images/second | `1,000 / 22.3`; assumes continuous serial work and excludes network/storage overhead |
| Conservative planning throughput | 20 images/second | Less than half the theoretical rate to reserve capacity for I/O and contention |
| Availability target for pilot | 99% monthly | Planning target; not yet measured |
| Data retention | Configurable by pilot owner | Privacy, licensing, and audit requirements must be agreed before deployment |

## Phased infrastructure

| Phase | Reach target | Infrastructure | Deployment mechanism | Exit evidence |
|---|---|---|---|---|
| Prototype | 5–8 real usability testers | One container; saved model; in-memory demo queue | Build the provided Dockerfile and expose port 8501 | Tests pass, signed-out link works, usability record completed |
| Pilot | One named research/nonprofit team; planning capacity 1.7M images/day per continuously utilized worker at 20 images/s | Object storage, durable job queue, relational audit database, authentication, logging, backups | Versioned container image; managed container host; separate staging and production | Spatial holdout, hosted load test, access review, recovery drill, pilot-owner approval |
| Replication | Multiple independently validated regions | Autoscaled stateless workers, model registry, drift alerts, tenant isolation, GIS export | Infrastructure as code, staged rollout, model/version pinning, rollback | Region-specific model cards, service-level measurements, cost and error budgets |

The daily pilot figure is arithmetic (`20 × 86,400`) rather than a capacity claim. Real throughput will be lower when workers are not continuously occupied and must be measured with representative images, concurrency, storage, and network behavior.

## Failure handling and observability

- Reject unsupported formats and oversized uploads before inference.
- Record model version, threshold version, input provenance, decision, confidence, quality alert, latency, and human-verification outcome.
- Use idempotent job identifiers so retries do not duplicate work.
- Send failed jobs to a dead-letter queue and expose them to an operator.
- Monitor latency, error rate, queue age, verification rate, per-class drift, and calibration on newly labeled data.
- Roll back by pinning the last validated container and model artifact.

## Deployment gates

No region is called supported until it passes a spatially separate evaluation, calibration check, quality review, local data/license assessment, and named human approval. No conservation outcome is claimed without a separately designed field or operational study.
