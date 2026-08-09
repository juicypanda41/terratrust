# Architecture and Design Rationale

```mermaid
flowchart LR
    A["Official EuroSAT RGB archive"] --> B["Checksum + deterministic split"]
    B --> C["Image feature extraction"]
    C --> D["Gradient-boosting classifier"]
    D --> E["Validation-only calibration"]
    E --> F["Validation-selected threshold"]
    F --> G["FastAPI model bridge"]
    J --> G
    G --> K["React / Vite interface"]
    K --> H["Auto-accept"]
    K --> I["Human review queue"]
    D --> J["Held-out evidence artifacts"]
    J --> K
```

## Decisions

- **React/Vite + FastAPI:** separates presentation from model inference while retaining a single production URL. The interface can use semantic HTML, responsive behavior, accessible interaction states, and a narrowly scoped animation bundle.
- **Minimal editorial design system:** strict rules, square geometry, warm neutral surfaces, and one primary accent keep attention on evidence and avoid a generic card-dashboard presentation. The persisted source of truth is `design-system/terratrust/MASTER.md`.
- **Purposeful motion only:** Framer Motion uses `LazyMotion` with `domAnimation`; transitions are limited to view changes, result/queue entry, and press feedback. Reduced-motion preferences are respected.
- **Deterministic features plus gradient boosting:** trains on ordinary hardware, is reproducible inside a short hackathon, and keeps the repository deployable without a large deep-learning runtime.
- **Separate validation and test roles:** calibration and threshold selection use validation data; final claims use held-out test data.
- **Saved evidence artifacts:** the dashboard cannot drift away from the evaluated results.
- **Abstention:** confidence changes the workflow rather than being decorative.

## Scale path

The prototype handles single images and small batches. A pilot would package inference behind a containerized API, store review events in a database, ingest cloud-masked Sentinel-2 tiles, and measure region-specific performance. Throughput projections must be calculated from measured latency and deployment hardware before inclusion in the pitch.
