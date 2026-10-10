import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="TelecomInsight BW", page_icon="📡", layout="wide")
DATA_PATH = Path(__file__).parent / "data" / "sample_telecom_data.csv"

st.markdown("""
<style>
.block-container {padding-top: 1.5rem;}
h1 {color: #4936a8;}
div[data-testid="stMetric"] {background:#f6f5ff;border:1px solid #e5e1ff;padding:14px;border-radius:12px;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_sample_data():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])

st.sidebar.title("TelecomInsight BW")
st.sidebar.caption("Telecommunications Service Quality & Customer Experience")
uploaded = st.sidebar.file_uploader("Upload a CSV dataset", type=["csv"])
st.sidebar.markdown("---")
st.sidebar.caption("The included sample records are fictional demonstration data.")

if uploaded is None:
    df = load_sample_data()
else:
    df = pd.read_csv(uploaded)
    required = {"date","provider","location","issue_type","download_mbps","upload_mbps","latency_ms","satisfaction","complaint_reported"}
    missing = required - set(df.columns)
    if missing:
        st.error("CSV is missing required columns: " + ", ".join(sorted(missing)))
        st.stop()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

for col in ["provider","location","issue_type"]:
    df[col] = df[col].fillna("Unknown").astype(str)
df = df.dropna(subset=["date"])

st.title("TelecomInsight BW")
st.caption("Explore telecommunications service quality, customer complaints and network trends.")
with st.expander("About this prototype"):
    st.write("This version uses fictional sample records to demonstrate analysis. It does not represent actual provider performance.")

st.sidebar.subheader("Filters")
providers = sorted(df["provider"].unique().tolist())
locations = sorted(df["location"].unique().tolist())
issues = sorted(df["issue_type"].unique().tolist())
p = st.sidebar.multiselect("Provider", providers, default=providers)
loc = st.sidebar.multiselect("Location", locations, default=locations)
issue = st.sidebar.multiselect("Issue type", issues, default=issues)
min_date, max_date = df["date"].min().date(), df["date"].max().date()
date_range = st.sidebar.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = df[df["provider"].isin(p) & df["location"].isin(loc) & df["issue_type"].isin(issue)].copy()
if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
    filtered = filtered[filtered["date"].dt.date.between(date_range[0], date_range[1])]
if filtered.empty:
    st.warning("No records match these filters. Change the filters to see results.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Records analysed", f"{len(filtered):,}")
c2.metric("Complaint reports", f"{int(filtered['complaint_reported'].sum()):,}")
c3.metric("Average download", f"{filtered['download_mbps'].mean():.1f} Mbps")
c4.metric("Average latency", f"{filtered['latency_ms'].mean():.0f} ms")

left, right = st.columns(2)
with left:
    st.subheader("Reported issues")
    counts = filtered.groupby("issue_type", as_index=False).size().rename(columns={"size":"records"}).sort_values("records", ascending=False)
    fig = px.bar(counts, x="issue_type", y="records", labels={"issue_type":"Issue type","records":"Number of records"}, color="records", color_continuous_scale=["#c7c1ff","#4936a8"])
    fig.update_layout(coloraxis_showscale=False, margin=dict(t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader("Complaints by provider")
    counts = filtered.groupby("provider", as_index=False)["complaint_reported"].sum().sort_values("complaint_reported", ascending=False)
    fig = px.bar(counts, x="provider", y="complaint_reported", labels={"provider":"Provider","complaint_reported":"Complaint reports"}, color="complaint_reported", color_continuous_scale=["#b8d9ff","#2457a7"])
    fig.update_layout(coloraxis_showscale=False, margin=dict(t=20,b=10))
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Network performance over time")
daily = filtered.assign(day=filtered["date"].dt.date).groupby("day", as_index=False).agg(download_mbps=("download_mbps","mean"), latency_ms=("latency_ms","mean"))
metric = st.radio("Choose a metric", ["Average download speed (Mbps)", "Average latency (ms)"], horizontal=True)
if metric.startswith("Average download"):
    fig = px.line(daily, x="day", y="download_mbps", markers=True, labels={"day":"Date","download_mbps":"Average download (Mbps)"})
else:
    fig = px.line(daily, x="day", y="latency_ms", markers=True, labels={"day":"Date","latency_ms":"Average latency (ms)"})
fig.update_layout(margin=dict(t=20,b=10))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Filtered data")
st.dataframe(filtered.sort_values("date", ascending=False), use_container_width=True, hide_index=True)
st.download_button("Download filtered data as CSV", filtered.to_csv(index=False).encode("utf-8"), "telecominsight_filtered_data.csv", "text/csv")
st.caption(f"Average customer satisfaction in this filtered dataset: {filtered['satisfaction'].mean():.1f}/5. Use authorised real data before drawing conclusions about providers or locations.")
