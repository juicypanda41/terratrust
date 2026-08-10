import {
  ArrowRight,
  Check,
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
  { id: "briefing", label: "Overview" },
  { id: "screen", label: "Analyze" },
  { id: "queue", label: "Human verification" },
  { id: "evidence", label: "Validation" },
];

const PUBLIC_LIMITATIONS = [
  "Classifies whole scenes, not exact boundaries or area.",
  "Assesses one image at a time; it does not claim to detect change.",
  "Current evaluation is regional and requires local validation before deployment.",
  "Confidence guides verification; it never guarantees correctness.",
];

const pct = (value, digits = 1) => `${(Number(value) * 100).toFixed(digits)}%`;

async function readJson(response) {
  const payload = await response.json().catch(() => ({}));
  if (!response.ok) throw new Error(payload.detail || "The request could not be completed.");
  return payload;
}

function App() {
  const [activeView, setActiveView] = useState(() => {
    const hash = window.location.hash.replace("#", "");
    return NAV_ITEMS.some((item) => item.id === hash) ? hash : "briefing";
  });
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
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    requestAnimationFrame(() => document.getElementById("main-content")?.focus({ preventScroll: true }));
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
        throw new Error("Choose a reference scene or upload an image first.");
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
    const source = selectedDemo?.file || uploadedFile?.name || "Uploaded scene";
    setQueue((current) => {
      if (current.some((item) => item.source === source)) return current;
      return [...current, { id: `${source}-${Date.now()}`, source, result, preview: selectedDemo?.image_url || previewUrl }];
    });
    selectView("queue");
  };

  const removeFromQueue = (id) => setQueue((current) => current.filter((item) => item.id !== id));

  if (loadError) return <SystemError message={loadError} />;

  if (!data) {
    return (
      <div className="loading-shell" role="status" aria-live="polite">
        <LoaderCircle className="spin" aria-hidden="true" />
        <span>Opening TerraTrust...</span>
      </div>
    );
  }

  return (
    <div className="site-shell">
      <a className="skip-link" href="#main-content">Skip to content</a>
      <Header activeView={activeView} queueCount={queue.length} onNavigate={selectView} />
      <main id="main-content" tabIndex="-1">
        {activeView === "briefing" && <Overview onStart={() => selectView("screen")} />}
        {activeView === "screen" && (
          <Analyze
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
        {activeView === "queue" && <ReviewQueue items={queue} onAnalyze={() => selectView("screen")} onRemove={removeFromQueue} />}
        {activeView === "evidence" && <Validation data={data} />}
      </main>
      <footer><span>TerraTrust</span><span>Screening support, not a final land-use record</span></footer>
    </div>
  );
}

function Header({ activeView, queueCount, onNavigate }) {
  return (
    <header className="site-header">
      <div className="masthead">
        <button className="wordmark" onClick={() => onNavigate("briefing")} aria-label="TerraTrust home">
          <span className="wordmark-mark" aria-hidden="true">TT</span>
          <span>TerraTrust</span>
        </button>
        <span className="masthead-note">Land-cover verification</span>
      </div>
      <nav className="primary-nav" aria-label="Primary navigation">
        {NAV_ITEMS.map((item) => (
          <button
            key={item.id}
            className={activeView === item.id ? "nav-item active" : "nav-item"}
            onClick={() => onNavigate(item.id)}
            aria-current={activeView === item.id ? "page" : undefined}
          >
            {item.label}
            {item.id === "queue" && queueCount > 0 && <span className="queue-count" aria-label={`${queueCount} queued`}>{queueCount}</span>}
          </button>
        ))}
      </nav>
    </header>
  );
}

function Overview({ onStart }) {
  return (
    <>
      <section className="intro" aria-labelledby="intro-title">
        <p className="section-label">Responsible screening</p>
        <h1 id="intro-title">Verify uncertain land-cover results before they move forward.</h1>
        <div className="intro-bottom">
          <p>TerraTrust classifies one satellite scene at a time and holds uncertain or unfamiliar images for a person to verify.</p>
          <button className="text-action" onClick={onStart}>Start an analysis <ArrowRight size={17} aria-hidden="true" /></button>
        </div>
      </section>
      <section className="overview-list" aria-label="How TerraTrust works">
        <div><span>Analyze</span><p>Choose a reference scene or upload an RGB image.</p></div>
        <div><span>Check</span><p>Verify the class, calibrated confidence, and reason.</p></div>
        <div><span>Route</span><p>Move uncertain or unverified scenes to human verification.</p></div>
      </section>
    </>
  );
}

function Analyze({ demos, selectedDemo, uploadedFile, previewUrl, fileInput, result, analyzing, error, onChooseDemo, onChooseUpload, onAnalyze, onQueue }) {
  const imageSource = selectedDemo?.image_url || previewUrl;
  const imageAlt = selectedDemo ? `${selectedDemo.story}, reference scene labeled ${selectedDemo.display_label}` : `Uploaded scene ${uploadedFile?.name || ""}`;
  return (
    <section aria-labelledby="analyze-title">
      <PageIntro label="Analyze" title="Land-cover analysis" description="Choose a reference scene or upload an image. New sources require human verification before they can continue." titleId="analyze-title" />
      <div className="workspace">
        <div className="source-panel">
          <div className="panel-heading"><span>Source</span><span>{uploadedFile ? "Uploaded image" : "Reference scene"}</span></div>
          <fieldset className="demo-selector">
            <legend>Examples</legend>
            <div className="demo-options">
              {demos.map((demo) => (
                <button key={demo.file} className={selectedDemo?.file === demo.file ? "demo-option selected" : "demo-option"} onClick={() => onChooseDemo(demo)} aria-pressed={selectedDemo?.file === demo.file}>
                  <img src={demo.image_url} width="56" height="56" alt="" />
                  <span><strong>{demo.story}</strong><small>{demo.display_label}</small></span>
                </button>
              ))}
            </div>
          </fieldset>
          <div className="image-stage">
            {imageSource ? <img src={imageSource} width="512" height="512" alt={imageAlt} /> : <div className="empty-image"><ScanSearch aria-hidden="true" /><span>No image selected</span></div>}
            <div className="image-meta"><span>{selectedDemo?.file || uploadedFile?.name || "No source"}</span></div>
          </div>
          <div className="source-actions">
            <input ref={fileInput} className="visually-hidden" id="scene-upload" type="file" accept="image/jpeg,image/png,image/webp" aria-label="Upload satellite scene" onChange={onChooseUpload} />
            <button className="secondary-action" onClick={() => fileInput.current?.click()}><ImagePlus size={17} aria-hidden="true" />{uploadedFile ? "Replace image" : "Upload image"}</button>
            <button className="primary-action" onClick={onAnalyze} disabled={analyzing || !imageSource}>
              {analyzing ? <><LoaderCircle className="spin" size={17} aria-hidden="true" />Analyzing...</> : <>Run analysis <ArrowRight size={17} aria-hidden="true" /></>}
            </button>
          </div>
          <p className="file-note">JPEG, PNG, or WebP. Maximum 10 MB.</p>
          {error && <div className="error-message" role="alert"><CircleAlert size={18} aria-hidden="true" /><span>{error} Try another image or restart the local server.</span></div>}
        </div>
        <div className="workspace-result" aria-live="polite">
          {result ? <ResultPanel result={result} onQueue={onQueue} /> : <EmptyResult />}
        </div>
      </div>
    </section>
  );
}

function EmptyResult() {
  return (
    <div className="result-empty">
      <ScanSearch size={22} aria-hidden="true" />
      <h2>No result yet</h2>
      <p>Choose a scene and run the analysis. The classification, confidence, and verification decision will appear here.</p>
    </div>
  );
}

function ResultPanel({ result, onQueue }) {
  return (
    <div className="result-panel">
      <div className="result-title">
        <div><span>Land cover</span><h2>{result.predicted_display}</h2></div>
        <div className={result.requires_review ? "decision review" : "decision accept"}>
          {result.requires_review ? <CircleAlert size={15} aria-hidden="true" /> : <Check size={15} aria-hidden="true" />}
          {result.requires_review ? "Human verification required" : "Ready to continue"}
        </div>
      </div>
      <div className="confidence"><strong>{pct(result.confidence)}</strong><span>calibrated confidence</span></div>
      <p className="review-reason">{result.review_reason}</p>
      <dl className="result-details">
        <div><dt>Runner-up</dt><dd>{result.second_display} / {pct(result.second_confidence)}</dd></div>
        <div><dt>Local inference</dt><dd>{result.latency_ms.toFixed(1)} ms</dd></div>
      </dl>
      <div className="probability-section">
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
      </div>
      {result.requires_review && <button className="queue-action" onClick={onQueue}><FileCheck2 size={17} aria-hidden="true" />Send to human verification</button>}
    </div>
  );
}

function ReviewQueue({ items, onAnalyze, onRemove }) {
  return (
    <section aria-labelledby="review-title">
      <PageIntro label="Queue" title="Human verification" description="Scenes that need a person stay here with their source, confidence, and verification reason." titleId="review-title" />
      {items.length === 0 ? (
        <div className="quiet-empty">
          <FileCheck2 size={22} aria-hidden="true" />
          <h2>Nothing is waiting</h2>
          <p>Analyze the ambiguous reference scene to test the handoff.</p>
          <button className="text-action" onClick={onAnalyze}>Go to analysis <ArrowRight size={17} aria-hidden="true" /></button>
        </div>
      ) : (
        <div className="queue-list">
          <div className="queue-heading"><span>{items.length} waiting</span><span>Awaiting verification</span></div>
          {items.map((item) => (
            <article key={item.id} className="queue-item">
              <img src={item.preview} width="88" height="88" alt={`Queued satellite scene ${item.source}`} />
              <div className="queue-copy"><span>{item.source}</span><h2>{item.result.predicted_display}</h2><p>{item.result.review_reason}</p></div>
              <div className="queue-confidence"><strong>{pct(item.result.confidence)}</strong><span>confidence</span></div>
              <button className="icon-button" onClick={() => onRemove(item.id)} aria-label={`Remove ${item.source} from human verification`}><X size={19} aria-hidden="true" /></button>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}

function Validation({ data }) {
  const { metrics, robustness, risk_coverage: riskCoverage } = data;
  return (
    <section aria-labelledby="validation-title">
      <PageIntro label="Validation" title="Performance and limits" description="Measured results from the held-out evaluation, alongside the boundaries of the current prototype." titleId="validation-title" />
      <div className="metric-strip" aria-label="Headline metrics">
        <Metric label="Overall accuracy" value={pct(metrics.accuracy)} />
        <Metric label="Macro F1" value={pct(metrics.macro_f1)} />
        <Metric label="Accepted-case accuracy" value={pct(metrics.selective_accuracy)} />
        <Metric label="Coverage" value={pct(metrics.coverage)} />
      </div>
      <div className="validation-layout">
        <article className="validation-section curve-section">
          <SectionHeading title="Accuracy and coverage" detail={`Threshold ${pct(metrics.threshold, 0)}`} />
          <RiskCurve rows={riskCoverage} threshold={metrics.threshold} />
          <p className="note">A stricter threshold sends more scenes to human verification. The complete policy also checks image quality.</p>
        </article>
        <article className="validation-section calibration-section">
          <SectionHeading title="Calibration" detail={`Held-out test, n=${metrics.test_count.toLocaleString()}`} />
          <div className="calibration-values">
            <div><span>Before</span><strong>{pct(metrics.ece_before, 2)}</strong></div>
            <ArrowRight size={18} aria-hidden="true" />
            <div><span>After</span><strong>{pct(metrics.ece_after, 2)}</strong></div>
          </div>
          <p className="note">Expected calibration error. Lower is better.</p>
        </article>
        <article className="validation-section full-width">
          <SectionHeading title="Controlled quality checks" detail="Not proof of general real-world robustness" />
          <div className="table-wrap">
            <table>
              <thead><tr><th>Condition</th><th>Samples</th><th>Accuracy</th><th>Review rate</th><th>Quality alerts</th></tr></thead>
              <tbody>{robustness.map((row) => <tr key={row.condition}><th scope="row">{row.condition}</th><td>{row.sample_count}</td><td>{pct(row.accuracy)}</td><td>{pct(row.review_rate)}</td><td>{pct(row.quality_alert_rate)}</td></tr>)}</tbody>
            </table>
          </div>
        </article>
        <article className="validation-section full-width limits-section">
          <div><SectionHeading title="Current boundaries" detail="Use with expert judgment" /><h2>What TerraTrust does not claim</h2></div>
          <ul>{PUBLIC_LIMITATIONS.map((limit) => <li key={limit}>{limit}</li>)}</ul>
          <div className="sdg-note"><FlaskConical size={18} aria-hidden="true" /><p><strong>SDG 15.1 and 15.2:</strong> TerraTrust supports a screening workflow. It does not claim measured conservation or deforestation outcomes.</p></div>
        </article>
      </div>
    </section>
  );
}

function Metric({ label, value }) {
  return <div><span>{label}</span><strong>{value}</strong></div>;
}

function SectionHeading({ title, detail }) {
  return <div className="section-heading"><h2>{title}</h2><span>{detail}</span></div>;
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
        <desc id="risk-desc">Accepted-case accuracy rises as a stricter confidence threshold sends more cases to human verification.</desc>
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

function PageIntro({ label, title, description, titleId }) {
  return <header className="page-intro"><div><p className="section-label">{label}</p><h1 id={titleId}>{title}</h1></div><p>{description}</p></header>;
}

function SystemError({ message }) {
  return <main className="system-error"><CircleAlert aria-hidden="true" /><h1>TerraTrust could not start</h1><p role="alert">{message}</p><code>python -m uvicorn api:app --port 8501</code></main>;
}

export default App;
