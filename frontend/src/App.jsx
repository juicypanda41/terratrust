import { AnimatePresence, m } from "framer-motion";
import {
  ArrowRight,
  Check,
  ChevronRight,
  CircleAlert,
  FileCheck2,
  FlaskConical,
  ImagePlus,
  LoaderCircle,
  ScanSearch,
  X,
} from "lucide-react";
import { useEffect, useMemo, useRef, useState } from "react";

const NAV_ITEMS = [
  { id: "briefing", label: "Briefing", index: "01" },
  { id: "screen", label: "Screen tile", index: "02" },
  { id: "queue", label: "Review queue", index: "03" },
  { id: "evidence", label: "Evidence", index: "04" },
];

const viewVariants = {
  hidden: { opacity: 0, y: 10 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.24, ease: "easeOut" } },
  exit: { opacity: 0, y: -6, transition: { duration: 0.14, ease: "easeIn" } },
};

const resultVariants = {
  hidden: { opacity: 0, y: 8 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.22, ease: "easeOut" } },
  exit: { opacity: 0, transition: { duration: 0.12 } },
};

const terrainVariants = {
  hidden: { opacity: 0, scale: 1.04, x: 18 },
  visible: { opacity: 1, scale: 1, x: 0, transition: { duration: 0.38, ease: "easeOut" } },
};

const PUBLIC_LIMITATIONS = [
  "Classifies whole scenes, not exact boundaries or area.",
  "Assesses one image at a time; it does not claim to detect change.",
  "Current evaluation is regional and requires local validation before deployment.",
  "Confidence guides review; it never guarantees correctness.",
];

const pct = (value, digits = 1) => `${(Number(value) * 100).toFixed(digits)}%`;

async function readJson(response) {
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail || "The request could not be completed.");
  return payload;
}

function App() {
  const [activeView, setActiveView] = useState("briefing");
  const [data, setData] = useState(null);
  const [loadError, setLoadError] = useState("");
  const [selectedDemo, setSelectedDemo] = useState(null);
  const [uploadedFile, setUploadedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState("");
  const [result, setResult] = useState(null);
  const [analysisError, setAnalysisError] = useState("");
  const [analyzing, setAnalyzing] = useState(false);
  const [queue, setQueue] = useState([]);
  const fileInput = useRef(null);

  useEffect(() => {
    fetch("/api/bootstrap")
      .then(readJson)
      .then((payload) => {
        setData(payload);
        setSelectedDemo(payload.demos[0] || null);
      })
      .catch((error) => setLoadError(error.message));
  }, []);

  useEffect(() => () => previewUrl && URL.revokeObjectURL(previewUrl), [previewUrl]);

  const featuredDemos = useMemo(() => {
    if (!data) return [];
    const names = ["Forest_1.jpg", "Highway_2.jpg", "Highway_1.jpg"];
    return names.map((name) => data.demos.find((item) => item.file === name)).filter(Boolean);
  }, [data]);

  const selectView = (view) => {
    setActiveView(view);
    window.history.replaceState(null, "", `#${view}`);
    document.getElementById("main-content")?.focus({ preventScroll: true });
  };

  const chooseDemo = (demo) => {
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl("");
    setUploadedFile(null);
    setSelectedDemo(demo);
    setResult(null);
    setAnalysisError("");
  };

  const chooseUpload = (event) => {
    const file = event.target.files?.[0];
    if (!file) return;
    if (previewUrl) URL.revokeObjectURL(previewUrl);
    setPreviewUrl(URL.createObjectURL(file));
    setUploadedFile(file);
    setSelectedDemo(null);
    setResult(null);
    setAnalysisError("");
  };

  const runAnalysis = async () => {
    setAnalyzing(true);
    setAnalysisError("");
    setResult(null);
    try {
      let response;
      if (uploadedFile) {
        const form = new FormData();
        form.append("file", uploadedFile);
        response = await fetch("/api/analyze/upload", { method: "POST", body: form });
      } else if (selectedDemo) {
        response = await fetch(`/api/analyze/demo/${encodeURIComponent(selectedDemo.file)}`, { method: "POST" });
      } else {
        throw new Error("Choose a demo tile or upload an image first.");
      }
      setResult(await readJson(response));
    } catch (error) {
      setAnalysisError(error.message);
    } finally {
      setAnalyzing(false);
    }
  };

  const addToQueue = () => {
    if (!result) return;
    const source = selectedDemo?.file || uploadedFile?.name || "Uploaded tile";
    setQueue((current) => {
      if (current.some((item) => item.source === source)) return current;
      return [...current, { id: `${source}-${Date.now()}`, source, result, preview: selectedDemo?.image_url || previewUrl }];
    });
    selectView("queue");
  };

  const removeFromQueue = (id) => setQueue((current) => current.filter((item) => item.id !== id));

  if (loadError) {
    return <SystemError message={loadError} />;
  }

  if (!data) {
    return (
      <div className="loading-shell" role="status" aria-live="polite">
        <LoaderCircle className="spin" aria-hidden="true" />
        <span>Loading evaluated model evidence…</span>
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Header activeView={activeView} queueCount={queue.length} onNavigate={selectView} />
      <main id="main-content" className="page-frame" tabIndex="-1">
        <AnimatePresence mode="wait" initial={false}>
          <m.div key={activeView} variants={viewVariants} initial="hidden" animate="visible" exit="exit">
            {activeView === "briefing" && <Briefing onStart={() => selectView("screen")} />}
            {activeView === "screen" && (
              <ScreenTile
                demos={featuredDemos}
                selectedDemo={selectedDemo}
                uploadedFile={uploadedFile}
                previewUrl={previewUrl}
                fileInput={fileInput}
                result={result}
                analyzing={analyzing}
                error={analysisError}
                onChooseDemo={chooseDemo}
                onChooseUpload={chooseUpload}
                onAnalyze={runAnalysis}
                onQueue={addToQueue}
              />
            )}
            {activeView === "queue" && <ReviewQueue items={queue} onScreen={() => selectView("screen")} onRemove={removeFromQueue} />}
            {activeView === "evidence" && <Evidence data={data} />}
          </m.div>
        </AnimatePresence>
      </main>
      <footer className="site-footer">
        <span>TerraTrust / Responsible land screening</span>
        <span>Built for decisions that deserve a second look</span>
      </footer>
    </div>
  );
}

function Header({ activeView, queueCount, onNavigate }) {
  return (
    <header className="site-header">
      <button className="wordmark" onClick={() => onNavigate("briefing")} aria-label="TerraTrust home">
        <span className="wordmark-mark" aria-hidden="true"><span /></span>
        <span>TerraTrust</span>
      </button>
      <nav className="primary-nav" aria-label="Primary navigation">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            className={activeView === item.id ? "nav-item active" : "nav-item"}
            onClick={() => onNavigate(item.id)}
            aria-current={activeView === item.id ? "page" : undefined}
          >
            <span>{item.index}</span>
            {item.label}
            {item.id === "queue" && queueCount > 0 && <b aria-label={`${queueCount} queued`}>{queueCount}</b>}
          </button>
        ))}
      </nav>
    </header>
  );
}

function Briefing({ onStart }) {
  return (
    <>
      <section className="hero-grid" aria-labelledby="hero-heading">
        <TerrainField />
        <div className="hero-copy">
          <p className="kicker">Earth observation / Human review</p>
          <h1 id="hero-heading">Know what to trust.<br />Know what to review.</h1>
          <p className="hero-summary">
            TerraTrust moves clear land-cover signals forward and pauses uncertain ones for a person.
            No forced answers. No hidden handoffs.
          </p>
          <m.button className="primary-action" onClick={onStart} whileTap={{ scale: 0.98 }}>
            Screen a tile <ArrowRight size={18} aria-hidden="true" />
          </m.button>
        </div>
        <aside className="policy-plate" aria-label="Decision policy">
          <div className="plate-index">THE FLOW / 01</div>
          <div className="policy-diagram" aria-hidden="true">
            <span className="policy-node solid" />
            <span className="policy-line" />
            <span className="policy-node" />
          </div>
          <h2>Two outcomes.<br />One accountable flow.</h2>
          <ol>
            <li><span>01</span> Clear enough to continue.</li>
            <li><span>02</span> Uncertain or unfamiliar goes to review.</li>
          </ol>
          <p>Every handoff keeps the reason attached.</p>
        </aside>
      </section>

      <section className="principle-grid">
        <div>
          <p className="section-index">HOW IT WORKS / 02</p>
          <h2>One useful answer—or a clear stop.</h2>
        </div>
        <div className="principle-copy">
          <p>
            Most tools are built to answer. TerraTrust is also built to pause. That makes uncertainty useful:
            it changes the next action instead of becoming another number on a screen.
          </p>
          <div className="flow-rail" aria-label="Screen, assess, route">
            <span><b>01</b> Screen</span><ArrowRight size={16} aria-hidden="true" />
            <span><b>02</b> Assess</span><ArrowRight size={16} aria-hidden="true" />
            <span><b>03</b> Route</span>
          </div>
        </div>
      </section>
    </>
  );
}

function TerrainField() {
  return (
    <m.svg
      className="terrain-field"
      viewBox="0 0 1200 720"
      preserveAspectRatio="xMidYMid slice"
      aria-hidden="true"
      focusable="false"
      variants={terrainVariants}
      initial="hidden"
      animate="visible"
    >
      <g className="terrain-grid">
        <path d="M720 -40V760M840 -40V760M960 -40V760M1080 -40V760" />
        <path d="M600 120H1240M600 240H1240M600 360H1240M600 480H1240M600 600H1240" />
      </g>
      <g className="terrain-contours">
        <path d="M1260 14C1025-72 780 24 764 211c-18 210 222 240 211 393-8 112-112 177-223 191" />
        <path d="M1268 72c-204-75-416 8-430 166-14 173 189 204 179 342-8 105-99 167-197 184" />
        <path d="M1278 134c-172-64-350 4-360 134-10 139 156 170 147 289-7 94-82 146-162 163" />
        <path d="M1282 195c-139-52-282 0-288 104-7 106 122 138 114 235-6 77-64 119-127 136" />
        <path d="M1288 257c-105-40-210-3-214 73-4 77 87 108 80 181-5 59-47 90-91 105" />
        <path d="M1293 318c-70-28-138-5-140 44-2 49 53 79 47 129-4 39-28 59-57 72" />
      </g>
    </m.svg>
  );
}

function ScreenTile({ demos, selectedDemo, uploadedFile, previewUrl, fileInput, result, analyzing, error, onChooseDemo, onChooseUpload, onAnalyze, onQueue }) {
  const imageSource = selectedDemo?.image_url || previewUrl;
  const imageAlt = selectedDemo ? `${selectedDemo.story}, reference scene labeled ${selectedDemo.display_label}` : `Uploaded scene ${uploadedFile?.name || ""}`;
  return (
    <section aria-labelledby="screen-heading">
      <PageIntro index="02" eyebrow="Operational demo" title="Screen one scene." description="Choose a reference scene or upload an RGB image. New imagery stays in review until its source is verified." />
      <div className="screen-layout">
        <div className="input-column">
          <fieldset className="demo-selector">
            <legend>Choose a reference scene</legend>
            {demos.map((demo, index) => (
              <button key={demo.file} className={selectedDemo?.file === demo.file ? "demo-row selected" : "demo-row"} onClick={() => onChooseDemo(demo)} aria-pressed={selectedDemo?.file === demo.file}>
                <span>0{index + 1}</span>
                <img src={demo.image_url} width="64" height="64" alt="" />
                <span><strong>{demo.story}</strong><small>Reference: {demo.display_label}</small></span>
                <ChevronRight size={18} aria-hidden="true" />
              </button>
            ))}
          </fieldset>
          <div className="upload-block">
            <input ref={fileInput} hidden id="tile-upload" type="file" accept="image/jpeg,image/png,image/webp" onChange={onChooseUpload} />
            <button className="secondary-action" onClick={() => fileInput.current?.click()}>
              <ImagePlus size={18} aria-hidden="true" /> {uploadedFile ? "Choose another image" : "Upload an RGB image"}
            </button>
            <p>JPEG, PNG, or WebP / maximum 10 MB</p>
          </div>
        </div>

        <div className="analysis-stage">
          <div className="image-stage">
            {imageSource ? <img src={imageSource} width="512" height="512" alt={imageAlt} /> : <div className="empty-image"><ScanSearch aria-hidden="true" /><span>No tile selected</span></div>}
            <div className="image-caption"><span>{selectedDemo?.file || uploadedFile?.name || "Awaiting input"}</span><span>Analysis frame</span></div>
          </div>
          <m.button className="primary-action full" onClick={onAnalyze} disabled={analyzing || !imageSource} whileTap={{ scale: 0.99 }}>
            {analyzing ? <><LoaderCircle className="spin" size={18} aria-hidden="true" /> Screening…</> : <><ScanSearch size={18} aria-hidden="true" /> Run screening</>}
          </m.button>
          {error && <div className="error-message" role="alert"><CircleAlert size={18} aria-hidden="true" /> <span>{error} Try another file or restart the local server.</span></div>}
        </div>

        <div className="result-column" aria-live="polite">
          <AnimatePresence mode="wait">
            {result ? (
              <m.div key={`${result.predicted_class}-${result.confidence}`} variants={resultVariants} initial="hidden" animate="visible" exit="exit">
                <ResultPanel result={result} onQueue={onQueue} />
              </m.div>
            ) : (
              <div className="result-empty">
                <p className="plate-index">OUTPUT / PENDING</p>
                <h2>The decision appears here.</h2>
                <p>Predicted class, calibrated confidence, review reason, runner-up, latency, and every class probability remain visible.</p>
              </div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </section>
  );
}

function ResultPanel({ result, onQueue }) {
  return (
    <div className="result-panel">
      <p className="plate-index">OUTPUT / COMPLETE</p>
      <div className={result.requires_review ? "decision-tag review" : "decision-tag accept"}>
        {result.requires_review ? <CircleAlert size={17} aria-hidden="true" /> : <Check size={17} aria-hidden="true" />}
        {result.requires_review ? "Human review required" : "Eligible for auto-acceptance"}
      </div>
      <h2>{result.predicted_display}</h2>
      <div className="confidence-line"><strong>{pct(result.confidence)}</strong><span>calibrated confidence</span></div>
      <p className="review-reason">{result.review_reason}</p>
      <dl className="result-details">
        <div><dt>Runner-up</dt><dd>{result.second_display} / {pct(result.second_confidence)}</dd></div>
        <div><dt>Local inference</dt><dd>{result.latency_ms.toFixed(1)} ms</dd></div>
      </dl>
      <h3>Class probabilities</h3>
      <div className="probability-list" aria-label="Class probability comparison">
        {result.probabilities.map((item) => (
          <div className="probability-row" key={item.class_name}>
            <span>{item.display_name}</span>
            <div className="bar-track" aria-hidden="true"><span style={{ transform: `scaleX(${item.probability})` }} /></div>
            <strong>{pct(item.probability)}</strong>
          </div>
        ))}
      </div>
      {result.requires_review && <m.button className="queue-action" onClick={onQueue} whileTap={{ scale: 0.98 }}><FileCheck2 size={18} aria-hidden="true" /> Add to review queue</m.button>}
    </div>
  );
}

function ReviewQueue({ items, onScreen, onRemove }) {
  return (
    <section aria-labelledby="queue-heading">
      <PageIntro index="03" eyebrow="Human checkpoint" title="Review queue." description="Flagged scenes arrive with the model's decision, uncertainty, and review reason intact. No silent overrides." />
      {items.length === 0 ? (
        <div className="queue-empty">
          <FileCheck2 size={28} aria-hidden="true" />
          <h2>No scenes are waiting.</h2>
          <p>Run the ambiguous reference scene to exercise the handoff.</p>
          <button className="secondary-action" onClick={onScreen}>Go to screen tile <ArrowRight size={18} aria-hidden="true" /></button>
        </div>
      ) : (
        <div className="queue-list">
          <div className="queue-header"><span>{items.length.toString().padStart(2, "0")} pending</span><span>Human disposition required</span></div>
          <AnimatePresence initial={false}>
            {items.map((item) => (
              <m.article key={item.id} className="queue-item" variants={resultVariants} initial="hidden" animate="visible" exit="exit">
                <img src={item.preview} width="96" height="96" alt={`Queued satellite tile ${item.source}`} />
                <div><span className="plate-index">{item.source}</span><h2>{item.result.predicted_display}</h2><p>{item.result.review_reason}</p></div>
                <div className="queue-confidence"><strong>{pct(item.result.confidence)}</strong><span>confidence</span></div>
                <button className="icon-button" onClick={() => onRemove(item.id)} aria-label={`Remove ${item.source} from review queue`}><X size={20} aria-hidden="true" /></button>
              </m.article>
            ))}
          </AnimatePresence>
        </div>
      )}
    </section>
  );
}

function Evidence({ data }) {
  const { metrics, robustness, risk_coverage: riskCoverage } = data;
  const target = metrics.target_selective_accuracy;
  return (
    <section aria-labelledby="evidence-heading">
      <PageIntro index="04" eyebrow="Accountability" title="Proof, with limits." description="Performance, safeguards, and boundaries stay visible for anyone who wants to inspect them." />
      <div className="evidence-grid">
        <article className="evidence-block wide">
          <div className="block-heading"><span>Accuracy / coverage trade-off</span><span>Validation-selected threshold: {pct(metrics.threshold, 0)}</span></div>
          <RiskCurve rows={riskCoverage} threshold={metrics.threshold} />
          <p className="chart-note">Higher thresholds trade automation for accuracy. The selected policy also applies a separate image-quality check, so final coverage differs from confidence-only points.</p>
        </article>
        <article className="evidence-block">
          <div className="block-heading"><span>Measured benchmark</span><span>Independent evaluation</span></div>
          <div className="benchmark-list">
            <Benchmark label="Overall accuracy" value={metrics.accuracy} />
            <Benchmark label="Macro F1" value={metrics.macro_f1} />
            <Benchmark label="Accepted-case accuracy" value={metrics.selective_accuracy} target={target} />
            <Benchmark label="Coverage" value={metrics.coverage} />
          </div>
        </article>
        <article className="evidence-block">
          <div className="block-heading"><span>Calibration</span><span>Expected calibration error</span></div>
          <div className="calibration-compare">
            <div><strong>{pct(metrics.ece_before, 2)}</strong><span>Before</span></div>
            <ArrowRight aria-hidden="true" />
            <div><strong>{pct(metrics.ece_after, 2)}</strong><span>After temperature scaling</span></div>
          </div>
          <p className="chart-note">Lower is better. Calibration uses validation data; the result shown here is held-out.</p>
        </article>
        <article className="evidence-block wide">
          <div className="block-heading"><span>Controlled quality stress test</span><span>Not general out-of-distribution proof</span></div>
          <div className="table-wrap">
            <table>
              <thead><tr><th>Condition</th><th>Samples</th><th>Accuracy</th><th>Review rate</th><th>Quality alerts</th></tr></thead>
              <tbody>{robustness.map((row) => <tr key={row.condition}><th scope="row">{row.condition}</th><td>{row.sample_count}</td><td>{pct(row.accuracy)}</td><td>{pct(row.review_rate)}</td><td>{pct(row.quality_alert_rate)}</td></tr>)}</tbody>
            </table>
          </div>
        </article>
        <article className="evidence-block wide limits-block">
          <div>
            <p className="section-index">BOUNDARIES / 05</p>
            <h2>What TerraTrust does not claim.</h2>
          </div>
          <ul>{PUBLIC_LIMITATIONS.map((limit) => <li key={limit}>{limit}</li>)}</ul>
          <div className="sdg-note"><FlaskConical size={20} aria-hidden="true" /><p><strong>SDG 15.1 and 15.2 alignment:</strong> TerraTrust is an enabling screening workflow. The prototype measures reliability and review workload—not conservation, deforestation, acreage, carbon, or biodiversity outcomes.</p></div>
        </article>
      </div>
    </section>
  );
}

function Benchmark({ label, value, target }) {
  return <div className="benchmark-row"><div><span>{label}</span><strong>{pct(value)}</strong></div><div className="benchmark-track" aria-hidden="true"><span style={{ transform: `scaleX(${value})` }} />{target && <i style={{ left: `${target * 100}%` }} />}</div>{target && <small>Target {pct(target, 0)}</small>}</div>;
}

function RiskCurve({ rows, threshold }) {
  const points = rows.map((row, index) => {
    const x = 18 + (index / Math.max(rows.length - 1, 1)) * 564;
    const y = 166 - ((Number(row.selective_accuracy) - 0.88) / 0.12) * 132;
    return `${x},${Math.max(18, Math.min(166, y))}`;
  }).join(" ");
  const selectedIndex = rows.reduce((best, row, index) => Math.abs(Number(row.threshold) - threshold) < Math.abs(Number(rows[best].threshold) - threshold) ? index : best, 0);
  const selected = points.split(" ")[selectedIndex]?.split(",") || [0, 0];
  return (
    <div className="risk-curve">
      <svg viewBox="0 0 600 190" role="img" aria-labelledby="risk-title risk-desc">
        <title id="risk-title">Accepted-case accuracy as the confidence threshold increases</title>
        <desc id="risk-desc">Accepted-case accuracy rises as a stricter confidence threshold sends more cases to review.</desc>
        <line x1="18" x2="582" y1="166" y2="166" />
        <line x1="18" x2="18" y1="18" y2="166" />
        <line className="target-line" x1="18" x2="582" y1="141" y2="141" />
        <polyline points={points} />
        <circle cx={selected[0]} cy={selected[1]} r="5" />
        <text x="20" y="136">90% target</text><text x="18" y="184">30% threshold</text><text x="500" y="184">99% threshold</text>
      </svg>
    </div>
  );
}

function PageIntro({ index, eyebrow, title, description }) {
  return <header className="page-intro"><div><p className="section-index">{index} / {eyebrow}</p><h1>{title}</h1></div><p>{description}</p></header>;
}

function SystemError({ message }) {
  return <main className="system-error"><CircleAlert aria-hidden="true" /><h1>TerraTrust could not start.</h1><p role="alert">{message}</p><code>python -m uvicorn api:app --port 8501</code></main>;
}

export default App;
