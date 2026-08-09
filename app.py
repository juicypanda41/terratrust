from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from PIL import Image

from src.terratrust.config import (
    CONFUSION_PATH,
    DEMO_DIR,
    DISPLAY_NAMES,
    METRICS_PATH,
    MODEL_PATH,
    ROBUSTNESS_PATH,
    RISK_COVERAGE_PATH,
)
from src.terratrust.inference import TerraTrustModel

st.set_page_config(
    page_title="TerraTrust | Responsible land-cover screening",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --mint:#3ddc97; --cream:#f2f6e9; --ink:#071711; --muted:#9db8aa; --card:#10251e; }
html, body, [class*="css"] { font-family:'DM Sans',sans-serif; }
h1, h2, h3 { font-family:'Space Grotesk',sans-serif !important; letter-spacing:-0.025em; }
[data-testid="stAppViewContainer"] { background: radial-gradient(circle at 78% -10%, #173b2d 0, #081713 38%); }
[data-testid="stSidebar"] { background:#0b1d17; border-right:1px solid #244437; }
.hero { padding:1.25rem 0 1.6rem; }
.eyebrow { color:var(--mint); font-size:.78rem; font-weight:700; letter-spacing:.16em; text-transform:uppercase; }
.hero h1 { color:var(--cream); font-size:clamp(2.5rem,6vw,5rem); line-height:.92; margin:.45rem 0 .8rem; max-width:900px; }
.hero p { color:#b9cec3; font-size:1.08rem; max-width:720px; line-height:1.6; }
.metric-card { background:linear-gradient(145deg,#122a21,#0d211a); border:1px solid #29483b; border-radius:16px; padding:1rem 1.05rem; min-height:118px; }
.metric-label { color:#8eaa9b; text-transform:uppercase; letter-spacing:.1em; font-size:.7rem; font-weight:700; }
.metric-value { color:#f3f8ef; font-family:'Space Grotesk'; font-size:2rem; font-weight:700; margin:.3rem 0; }
.metric-note { color:#8eaa9b; font-size:.78rem; }
.decision-good { background:#0f3325; color:#83f3bd; border:1px solid #2d8b62; padding:.75rem 1rem; border-radius:12px; font-weight:700; }
.decision-review { background:#362815; color:#ffd58a; border:1px solid #8f682a; padding:.75rem 1rem; border-radius:12px; font-weight:700; }
.callout { background:#10251e; border-left:4px solid var(--mint); border-radius:0 12px 12px 0; padding:1rem 1.2rem; color:#cce0d5; }
.fineprint { color:#83a092; font-size:.78rem; line-height:1.5; }
div[data-testid="stMetric"] { background:#10251e; border:1px solid #29483b; padding:1rem; border-radius:14px; }
div.stButton > button { border-radius:999px; border:1px solid #3ddc97; }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def load_model() -> TerraTrustModel | None:
    return TerraTrustModel.load(str(MODEL_PATH)) if MODEL_PATH.exists() else None


@st.cache_data
def load_metrics() -> dict:
    if METRICS_PATH.exists():
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    return {}


@st.cache_data
def load_manifest() -> list[dict]:
    path = DEMO_DIR / "manifest.json"
    if not path.exists():
        return []
    items = json.loads(path.read_text(encoding="utf-8"))
    priority = {"Forest_1.jpg": 0, "Highway_2.jpg": 1, "Highway_1.jpg": 2}
    return sorted(items, key=lambda item: (priority.get(item["file"], 99), item["file"]))


def pct(value: float | None, digits: int = 1) -> str:
    return "Not evaluated" if value is None else f"{value * 100:.{digits}f}%"


def metric_card(label: str, value: str, note: str) -> None:
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


metrics = load_metrics()
model = load_model()
manifest = load_manifest()

with st.sidebar:
    st.markdown("## TerraTrust")
    st.caption("Responsible satellite screening")
    st.markdown("---")
    st.markdown("**Decision policy**")
    if metrics:
        st.write(f"Auto-accept at **≥ {metrics['threshold']:.0%}** calibrated confidence **and** a clear quality gate")
        st.write(f"Target accepted-case accuracy: **{metrics['target_selective_accuracy']:.0%}**")
    else:
        st.warning("Model artifacts have not been generated yet.")
    st.markdown("---")
    st.markdown("**Scope boundary**")
    st.caption(
        "European 64×64 Sentinel-2 scene classification. No segmentation, acreage, "
        "temporal change detection, or conservation outcome claims."
    )
    st.markdown("---")
    st.caption("Built for OurPlanet.Rocks 2026 · Technical Track")

st.markdown(
    """
<section class="hero">
  <div class="eyebrow">Human judgment, precisely where it matters</div>
  <h1>Satellite screening<br/>that knows when to stop.</h1>
  <p>TerraTrust classifies clear land-cover tiles automatically and routes uncertain
  cases to people—turning model confidence into an auditable review workflow.</p>
</section>
""",
    unsafe_allow_html=True,
)

if not model or not metrics:
    st.error(
        "Evaluated artifacts are missing. Run `python scripts/download_data.py` and "
        "`python scripts/train.py`, then refresh this page."
    )
    st.stop()

overview, analyze, queue, evidence, method = st.tabs(
    ["Mission control", "Analyze tile", "Review queue", "Evidence lab", "Method & limits"]
)

with overview:
    cols = st.columns(4)
    with cols[0]:
        metric_card("Accepted-case accuracy", pct(metrics["selective_accuracy"]), "Held-out test set")
    with cols[1]:
        metric_card("Auto-accepted", pct(metrics["coverage"]), "Full confidence + quality policy")
    with cols[2]:
        metric_card("Sent to review", pct(metrics["review_rate"]), "Confidence or quality flags")
    with cols[3]:
        metric_card("Calibration error", pct(metrics["ece_after"]), "ECE after temperature scaling")

    st.markdown("### One operating principle")
    st.markdown(
        '<div class="callout">A prediction is useful only when its uncertainty changes what happens next. '
        "TerraTrust converts calibrated confidence into a clear choice: accept the screening result or ask a person.</div>",
        unsafe_allow_html=True,
    )
    left, right = st.columns([1.2, 1])
    with left:
        st.markdown("#### Current benchmark")
        benchmark = pd.DataFrame(
            {
                "Metric": ["Overall accuracy", "Macro F1", "Accepted-case accuracy", "Coverage"],
                "Result": [
                    pct(metrics["accuracy"]),
                    pct(metrics["macro_f1"]),
                    pct(metrics["selective_accuracy"]),
                    pct(metrics["coverage"]),
                ],
            }
        )
        st.dataframe(benchmark, hide_index=True, use_container_width=True)
    with right:
        st.markdown("#### Measured scope")
        st.write(f"**{metrics['test_count']:,}** held-out test tiles")
        st.write(f"**{metrics['sample_count']:,}** total EuroSAT RGB images")
        st.write(f"**{len(metrics['per_class'])}** land-cover classes")
        if metrics.get("inference_latency_ms"):
            st.write(f"**{metrics['inference_latency_ms']['median']:.1f} ms** median warm local inference")
        st.caption(metrics["split_method"])

with analyze:
    st.markdown("### Analyze one satellite tile")
    st.caption("Choose a held-out demo tile or upload a compatible RGB image.")
    source_choice = st.radio("Image source", ["Curated demo tile", "Upload image"], horizontal=True)
    image = None
    source_label = None
    selected_file = None
    if source_choice == "Curated demo tile":
        if manifest:
            demo_story = {
                "Forest_1.jpg": "Clear forest demo",
                "Highway_2.jpg": "Ambiguous tile → review",
                "Highway_1.jpg": "Known failure case",
            }
            options = {
                f"{demo_story.get(item['file'], DISPLAY_NAMES.get(item['label'], item['label']))} · {item['file']}": item
                for item in manifest
            }
            selected = st.selectbox("Example", list(options))
            item = options[selected]
            selected_file = DEMO_DIR / item["file"]
            image = Image.open(selected_file).convert("RGB")
            source_label = item["label"]
    else:
        upload = st.file_uploader("RGB tile", type=["jpg", "jpeg", "png"], help="The model resizes the image to 64×64. Non-Sentinel imagery is outside the validated scope.")
        if upload:
            image = Image.open(upload).convert("RGB")

    if image is not None:
        result = model.predict(image)
        image_col, result_col = st.columns([0.8, 1.5])
        with image_col:
            st.image(image, caption="Input tile", width=320)
            if source_label:
                st.caption(f"Held-out label: {DISPLAY_NAMES.get(source_label, source_label)}")
        with result_col:
            st.markdown(f"## {DISPLAY_NAMES.get(result.predicted_class, result.predicted_class)}")
            st.write(f"Calibrated confidence **{result.confidence:.1%}**")
            if result.requires_review:
                st.markdown('<div class="decision-review">Human review required</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="decision-good">Eligible for auto-acceptance</div>', unsafe_allow_html=True)
            st.caption(result.review_reason)
            st.write(
                f"Runner-up: **{DISPLAY_NAMES.get(result.second_class, result.second_class)}** "
                f"at **{result.second_confidence:.1%}**"
            )
            st.caption(f"Local inference: {result.latency_ms:.1f} ms")

        probability_df = pd.DataFrame(
            {
                "Class": [DISPLAY_NAMES.get(name, name) for name in result.probabilities],
                "Probability": list(result.probabilities.values()),
            }
        ).sort_values("Probability")
        fig = px.bar(probability_df, x="Probability", y="Class", orientation="h", color="Probability", color_continuous_scale=["#2c5847", "#3ddc97"])
        fig.update_layout(height=430, coloraxis_showscale=False, margin=dict(l=0, r=10, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig, use_container_width=True)

        if result.requires_review and st.button("Add to human review queue", type="primary"):
            st.session_state.setdefault("review_queue", [])
            st.session_state.review_queue.append(
                {
                    "source": selected_file.name if selected_file else "uploaded image",
                    "prediction": DISPLAY_NAMES.get(result.predicted_class, result.predicted_class),
                    "confidence": result.confidence,
                    "status": "Pending",
                }
            )
            st.success("Added to the local review queue.")

with queue:
    st.markdown("### Human review queue")
    st.caption("The prototype records review decisions in this browser session; it does not retrain automatically.")
    review_queue = st.session_state.get("review_queue", [])
    if not review_queue:
        st.info("No tiles are waiting. Analyze an uncertain tile and add it to the queue.")
    else:
        frame = pd.DataFrame(review_queue)
        frame["confidence"] = frame["confidence"].map(lambda value: f"{value:.1%}")
        st.dataframe(frame, hide_index=True, use_container_width=True)
        if st.button("Mark oldest item reviewed"):
            st.session_state.review_queue[0]["status"] = "Reviewed"
            st.rerun()

with evidence:
    st.markdown("### Evidence lab")
    st.caption("Every headline number below comes from saved held-out evaluation artifacts.")
    risk = pd.read_csv(RISK_COVERAGE_PATH)
    risk_fig = px.line(risk, x="coverage", y="selective_accuracy", markers=True, labels={"coverage": "Auto-accepted share", "selective_accuracy": "Accepted-case accuracy"})
    risk_fig.add_vline(x=metrics["coverage"], line_dash="dash", line_color="#3ddc97")
    risk_fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(risk_fig, use_container_width=True)
    st.caption("Moving right automates more work but can increase error risk. The dashed line is the validation-selected operating point.")

    before = pd.DataFrame(metrics["reliability_bins_before"])
    after = pd.DataFrame(metrics["reliability_bins_after"])
    calibration = pd.concat([before.assign(Stage="Before"), after.assign(Stage="After")])
    cal_fig = px.scatter(calibration, x="confidence", y="accuracy", color="Stage", size="count", range_x=[0, 1], range_y=[0, 1])
    cal_fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", name="Perfect calibration", line=dict(dash="dash", color="#8fa99c")))
    cal_fig.update_layout(height=420, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(cal_fig, use_container_width=True)

    if ROBUSTNESS_PATH.exists():
        st.markdown("#### Controlled robustness audit")
        robustness = pd.read_csv(ROBUSTNESS_PATH)
        robust_fig = px.bar(
            robustness,
            x="condition",
            y=["accuracy", "review_rate"],
            barmode="group",
            labels={"value": "Result", "condition": "Condition", "variable": "Metric"},
            color_discrete_sequence=["#7da8ff", "#3ddc97"],
        )
        robust_fig.update_layout(
            height=420,
            yaxis_tickformat=".0%",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
        )
        st.plotly_chart(robust_fig, use_container_width=True)
        shifted = robustness[robustness["condition"] != "Clean"]
        st.success(
            f"The validation-trained quality gate routed {shifted['quality_alert_rate'].min():.1%}–"
            f"{shifted['quality_alert_rate'].max():.1%} of the four controlled perturbations to review."
        )
        st.caption(
            "A fixed 400-image class-balanced subset was tested under controlled transforms. "
            "This is a stress test, not evidence of complete real-world robustness."
        )

    confusion = pd.read_csv(CONFUSION_PATH, index_col=0)
    confusion.index = [DISPLAY_NAMES.get(name, name) for name in confusion.index]
    confusion.columns = [DISPLAY_NAMES.get(name, name) for name in confusion.columns]
    matrix = px.imshow(confusion, text_auto=True, color_continuous_scale=[[0, "#10251e"], [1, "#3ddc97"]], aspect="auto")
    matrix.update_layout(height=650, coloraxis_showscale=False, paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(matrix, use_container_width=True)

with method:
    st.markdown("### What was measured")
    st.write(
        "TerraTrust uses deterministic image statistics, spatial color pooling, histograms, and edge features "
        "with a histogram gradient-boosting classifier. Temperature scaling and the acceptance threshold are "
        "fit on validation data only; headline performance is reported on a held-out test set."
    )
    st.code(
        f"Dataset: {metrics['dataset']}\n"
        f"Split: {metrics['train_count']} train / {metrics['validation_count']} validation / {metrics['test_count']} test\n"
        f"Seed: {metrics['seed']}\n"
        f"Features: {metrics['feature_version']}\n"
        f"Model: {metrics['model']}",
        language="text",
    )
    st.markdown("### Important limitations")
    for limitation in metrics["limitations"]:
        st.warning(limitation)
    st.markdown(
        '<p class="fineprint">TerraTrust supports screening research and demonstration. It must not be used '
        "as the sole basis for environmental, legal, safety, or land-management decisions.</p>",
        unsafe_allow_html=True,
    )
