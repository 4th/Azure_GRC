import os
import json
import time
import math
from typing import List, Dict, Any, Optional

import streamlit as st
import pandas as pd
from dotenv import load_dotenv

# Matplotlib only (no seaborn) to meet internal guidelines
import matplotlib.pyplot as plt

try:
    from azure.cosmos import CosmosClient
except Exception:
    CosmosClient = None  # optional for local demo

load_dotenv()

st.set_page_config(
    page_title="4th.GRC — Governance Scorecard",
    page_icon="✅",
    layout="wide"
)

# ---- Sidebar ----
logo_path = os.path.join(os.path.dirname(__file__), "assets", "4th_logo.png")
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, use_column_width=True)

st.sidebar.title("4th.GRC Scorecard")
st.sidebar.caption("Autonomy with Accountability™")

PAGE = st.sidebar.radio("Navigate", ["Overview", "Systems", "Controls", "Findings"])

# Cosmos DB config (optional)
COSMOS_URL = os.getenv("COSMOS_URL", "")
COSMOS_KEY = os.getenv("COSMOS_KEY", "")
COSMOS_DB = os.getenv("COSMOS_DB", "grc")
COSMOS_CONTAINER = os.getenv("COSMOS_CONTAINER", "findings")

@st.cache_data(ttl=60)
def load_data() -> pd.DataFrame:
    """
    Load latest findings from Cosmos DB. If Cosmos is not configured,
    return sample data for demo.
    """
    # Minimal columns: system_id, control_id, status, score, ts
    cols = ["system_id","control_id","rule_id","status","score","ts"]
    # Use sample if Cosmos isn't reachable
    if not CosmosClient or not COSMOS_URL or not COSMOS_KEY:
        data = [
            {"system_id":"checkout","control_id":"ISO42001-6.3.2","rule_id":"bias_fairness","status":"pass","score":0.92,"ts":"2025-11-10T18:00:00Z"},
            {"system_id":"checkout","control_id":"SEC-ENC-01","rule_id":"encryption","status":"pass","score":1.00,"ts":"2025-11-10T18:00:00Z"},
            {"system_id":"cust-support","control_id":"PRIV-PII-02","rule_id":"pii","status":"warn","score":0.50,"ts":"2025-11-10T17:55:00Z"},
            {"system_id":"agent-orch","control_id":"GOV-ALLOW-01","rule_id":"tool_allowlist","status":"fail","score":0.00,"ts":"2025-11-10T17:45:00Z"},
            {"system_id":"agent-orch","control_id":"OPS-LOG-01","rule_id":"logging_audit","status":"pass","score":1.00,"ts":"2025-11-10T17:45:00Z"},
        ]
        return pd.DataFrame(data, columns=cols)

    try:
        client = CosmosClient(COSMOS_URL, credential=COSMOS_KEY)  # type: ignore
        db = client.get_database_client(COSMOS_DB)
        container = db.get_container_client(COSMOS_CONTAINER)
        # Fetch last N hours of findings (adjust query as needed)
        query = "SELECT TOP 1000 c.system_id, c.control_id, c.rule_id, c.status, c.score, c.ts FROM c ORDER BY c.ts DESC"
        items = list(container.query_items(query=query, enable_cross_partition_query=True))
        df = pd.DataFrame(items)
        if df.empty:
            raise ValueError("No data")
        # Ensure required columns
        for c in cols:
            if c not in df.columns:
                df[c] = None
        return df[cols]
    except Exception as e:
        st.sidebar.warning(f"Cosmos error: {e}. Showing sample data.")
        return load_data.clear() or load_data()  # clean cache then fallback

def metric_tile(label: str, value: str, help_text: Optional[str] = None):
    st.markdown(f"<div class='metric'><div class='metric-label'>{label}</div><div class='metric-value'>{value}</div></div>", unsafe_allow_html=True)
    if help_text:
        st.caption(help_text)

def plot_bar(series: pd.Series, title: str):
    fig, ax = plt.subplots()
    series.plot(kind="bar", ax=ax)  # do not specify colors/styles
    ax.set_title(title)
    ax.set_xlabel("")
    ax.set_ylabel("Count")
    st.pyplot(fig)

# Load
df = load_data()

# ---- Styles ----
css_path = os.path.join(os.path.dirname(__file__), "assets", "styles.css")
if os.path.exists(css_path):
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---- Pages ----
if PAGE == "Overview":
    st.header("📊 Governance Overview")
    col1, col2, col3, col4 = st.columns(4)

    total = len(df)
    passes = int((df["status"] == "pass").sum())
    warns = int((df["status"] == "warn").sum())
    fails = int((df["status"] == "fail").sum())
    overall = round(df["score"].mean() if "score" in df and not df.empty else 0.0, 3)

    with col1: metric_tile("Findings (Last Batch)", str(total), "Total evaluated records")
    with col2: metric_tile("Pass", str(passes))
    with col3: metric_tile("Warn", str(warns))
    with col4: metric_tile("Fail", str(fails))

    st.markdown("---")
    st.subheader("Status Breakdown")
    plot_bar(df["status"].value_counts(), "Findings by Status")

    st.subheader("Top Systems by Risk (Failures)")
    failures = df[df["status"] == "fail"]["system_id"].value_counts().head(10)
    if not failures.empty:
        plot_bar(failures, "Failures per System")
    else:
        st.info("No failures in the current dataset.")

elif PAGE == "Systems":
    st.header("🏷️ Systems")
    systems = sorted(df["system_id"].dropna().unique().tolist())
    sel = st.multiselect("Filter systems", systems, default=systems[:3] if systems else [])
    filtered = df[df["system_id"].isin(sel)] if sel else df.copy()
    st.dataframe(filtered.sort_values("ts"))
    st.download_button("Download CSV", filtered.to_csv(index=False), "grc_findings.csv", "text/csv")

elif PAGE == "Controls":
    st.header("🧩 Controls")
    by_control = df.groupby(["control_id","rule_id","status"]).size().reset_index(name="count")
    st.dataframe(by_control.sort_values(["control_id","status","count"], ascending=[True, True, False]))

    st.subheader("Rule Heat (Pass/Warn/Fail)")
    ct = df.pivot_table(index="rule_id", columns="status", values="system_id", aggfunc="count", fill_value=0)
    st.dataframe(ct)

elif PAGE == "Findings":
    st.header("📑 Findings")
    st.write("Latest evaluation results from the PolicyEngine.")
    st.dataframe(df.sort_values("ts", ascending=False))
    # Simple distribution of scores
    if "score" in df.columns:
        st.subheader("Score Distribution")
        fig, ax = plt.subplots()
        ax.hist(df["score"].dropna(), bins=10)  # default color
        ax.set_xlabel("Score")
        ax.set_ylabel("Frequency")
        ax.set_title("Distribution of Findings Scores")
        st.pyplot(fig)

st.sidebar.markdown("---")
with st.sidebar.expander("Configuration"):
    st.code(json.dumps({
        "COSMOS_URL": COSMOS_URL[:6] + "…" if COSMOS_URL else "",
        "COSMOS_DB": COSMOS_DB,
        "COSMOS_CONTAINER": COSMOS_CONTAINER
    }, indent=2))
    st.caption("Set COSMOS_URL, COSMOS_KEY, COSMOS_DB, COSMOS_CONTAINER in environment to enable live data.")
