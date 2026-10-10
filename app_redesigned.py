import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="TelecomInsight BW | Network Intelligence",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="expanded",
)

DATA_PATH = Path(__file__).parent / "data" / "sample_telecom_data.csv"

PURPLE = "#7057D9"
ROYAL_BLUE = "#245DB8"
LIGHT_PURPLE = "#F3F0FF"
INK = "#20283A"
MUTED = "#697386"
BORDER = "#E4E8F0"
PAGE = "#F8FAFD"
CYAN = "#16A6A1"

# Approximate city-centre coordinates used only to place location-level summaries on the map.
# They are NOT telecom tower locations, GPS observations, or measured coverage boundaries.
LOCATION_COORDS = {
    "Gaborone": {"lat": -24.6282, "lon": 25.9231},
    "Francistown": {"lat": -21.1702, "lon": 27.5144},
    "Maun": {"lat": -19.9833, "lon": 23.4167},
    "Palapye": {"lat": -22.5460, "lon": 27.1250},
    "Serowe": {"lat": -22.3875, "lon": 26.7100},
    "Kasane": {"lat": -17.8000, "lon": 25.1500},
    "Molepolole": {"lat": -24.4066, "lon": 25.4950},
    "Kanye": {"lat": -24.9833, "lon": 25.3500},
    "Mochudi": {"lat": -24.4167, "lon": 26.1500},
    "Lobatse": {"lat": -25.2167, "lon": 25.6833},
    "Ghanzi": {"lat": -21.7000, "lon": 21.6500},
    "Jwaneng": {"lat": -24.6000, "lon": 24.7333},
}

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');
    .stApp {{ background:{PAGE}; color:{INK}; font-family:'DM Sans',sans-serif; }}
    [data-testid="stHeader"] {{ background:rgba(248,250,253,.94); }}
    [data-testid="stSidebar"] {{ background:#fff; border-right:1px solid {BORDER}; }}
    [data-testid="stSidebar"] * {{ color:{INK}; }}
    .block-container {{ padding-top:2rem; padding-bottom:3rem; max-width:1500px; }}
    h1,h2,h3,p,label {{ font-family:'Manrope','DM Sans',sans-serif; }}
    h1 {{ color:{INK}; letter-spacing:-1.1px; font-weight:800; }}
    h2,h3 {{ color:{INK}; letter-spacing:-.45px; }}
    .brand-lockup {{ display:flex; align-items:center; gap:12px; padding:8px 0 20px; }}
    .brand-mark {{ display:flex; align-items:center; justify-content:center; width:44px; height:44px; border-radius:13px; background:linear-gradient(135deg,{PURPLE},{ROYAL_BLUE}); color:#fff; font-size:23px; }}
    .brand-name {{ color:{INK}; font-family:'Manrope',sans-serif; font-size:18px; font-weight:800; line-height:1.15; }}
    .brand-subtitle {{ color:{MUTED}; font-size:10px; margin-top:4px; letter-spacing:1px; text-transform:uppercase; }}
    .eyebrow {{ color:{PURPLE}; font-size:11px; letter-spacing:1.8px; font-weight:800; text-transform:uppercase; margin-bottom:8px; }}
    .hero-subtitle {{ color:{MUTED}; font-size:15px; margin-top:-8px; margin-bottom:20px; }}
    .status-pill {{ display:inline-block; color:#176C68; background:#E8F8F5; border:1px solid #BFE9E2; border-radius:999px; padding:7px 11px; font-size:11px; font-weight:700; white-space:nowrap; }}
    .section-label {{ color:{MUTED}; text-transform:uppercase; font-size:11px; letter-spacing:1.5px; font-weight:800; margin:12px 0 8px; }}
    div[data-testid="stMetric"] {{ background:#fff; border:1px solid {BORDER}; border-radius:16px; padding:18px 20px; box-shadow:0 4px 14px rgba(31,45,75,.035); min-height:122px; }}
    div[data-testid="stMetricLabel"] {{ color:{MUTED}; font-size:12px; font-weight:600; }}
    div[data-testid="stMetricValue"] {{ color:{INK}; font-family:'Manrope',sans-serif; font-weight:800; font-size:29px; }}
    div[data-testid="stPlotlyChart"] {{ background:#fff; border:1px solid {BORDER}; border-radius:16px; padding:8px 8px 0; box-shadow:0 4px 14px rgba(31,45,75,.025); }}
    div[data-testid="stDataFrame"] {{ border:1px solid {BORDER}; border-radius:12px; overflow:hidden; }}
    .info-banner {{ background:{LIGHT_PURPLE}; border:1px solid #DED7FF; border-left:4px solid {PURPLE}; border-radius:10px; padding:12px 15px; color:#4E428B; font-size:12px; margin:14px 0 22px; }}
    .footer-note {{ color:{MUTED}; font-size:11px; text-align:center; padding-top:28px; }}
    .stButton button,.stDownloadButton button {{ border-radius:9px; border:1px solid {ROYAL_BLUE}; background:{ROYAL_BLUE}; color:#fff; font-weight:700; }}
    .stButton button:hover,.stDownloadButton button:hover {{ border-color:{PURPLE}; background:{PURPLE}; color:#fff; }}
    [data-baseweb="select"]>div,[data-testid="stDateInput"] input {{ background:#fff; border-color:{BORDER}; border-radius:9px; }}
    [data-testid="stFileUploader"] section {{ background:{PAGE}; border:1px dashed #C7CEDC; border-radius:12px; }}
    hr {{ border-color:{BORDER}; }}
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_sample_data():
    return pd.read_csv(DATA_PATH, parse_dates=["date"])


def style_chart(fig, height=340):
    fig.update_layout(
        height=height, paper_bgcolor="#FFFFFF", plot_bgcolor="#FFFFFF",
        font=dict(family="DM Sans, sans-serif", color=MUTED, size=12),
        margin=dict(l=12, r=12, t=25, b=12),
        legend=dict(bgcolor="rgba(255,255,255,0)", font=dict(color=MUTED)),
        xaxis=dict(showgrid=False, zeroline=False, linecolor=BORDER, tickfont=dict(color=MUTED)),
        yaxis=dict(showgrid=True, gridcolor="#EDF0F5", zeroline=False, linecolor=BORDER, tickfont=dict(color=MUTED)),
        colorway=[PURPLE, ROYAL_BLUE, CYAN, "#E6A23C"],
    )
    return fig


with st.sidebar:
    st.markdown(
        f"""<div class="brand-lockup"><div class="brand-mark">📡</div><div>
        <div class="brand-name">TelecomInsight BW</div><div class="brand-subtitle">Network intelligence</div>
        </div></div>""",
        unsafe_allow_html=True,
    )
    st.markdown('<div class="section-label">DATA SOURCE</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader("Upload a CSV dataset", type=["csv"])
    st.caption("CSV must include the required TelecomInsight columns.")
    st.markdown("---")
    st.markdown('<div class="section-label">FILTER THE ANALYSIS</div>', unsafe_allow_html=True)
    st.caption("Filters apply to the KPIs, charts, map and table.")

if uploaded is None:
    df = load_sample_data()
    using_sample = True
else:
    try:
        df = pd.read_csv(uploaded)
    except Exception as exc:
        st.error(f"We couldn't read this CSV file: {exc}")
        st.stop()
    using_sample = False
    required = {
        "date", "provider", "location", "issue_type", "download_mbps",
        "upload_mbps", "latency_ms", "satisfaction", "complaint_reported"
    }
    missing = required - set(df.columns)
    if missing:
        st.error("CSV is missing required columns: " + ", ".join(sorted(missing)))
        st.stop()
    df["date"] = pd.to_datetime(df["date"], errors="coerce")

for col in ["provider", "location", "issue_type"]:
    df[col] = df[col].fillna("Unknown").astype(str)
for col in ["download_mbps", "upload_mbps", "latency_ms", "satisfaction", "complaint_reported"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")
df = df.dropna(subset=["date", "download_mbps", "latency_ms", "complaint_reported"])
if df.empty:
    st.error("There are no usable records in this dataset after basic validation.")
    st.stop()

with st.sidebar:
    providers = sorted(df["provider"].unique().tolist())
    locations = sorted(df["location"].unique().tolist())
    issues = sorted(df["issue_type"].unique().tolist())
    selected_providers = st.multiselect("Provider", providers, default=providers)
    selected_locations = st.multiselect("Location", locations, default=locations)
    selected_issues = st.multiselect("Issue type", issues, default=issues)
    min_date, max_date = df["date"].min().date(), df["date"].max().date()
    selected_dates = st.date_input("Date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

filtered = df[
    df["provider"].isin(selected_providers)
    & df["location"].isin(selected_locations)
    & df["issue_type"].isin(selected_issues)
].copy()
if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    filtered = filtered[filtered["date"].dt.date.between(selected_dates[0], selected_dates[1])]

head_left, head_right = st.columns([4, 1])
with head_left:
    st.markdown('<div class="eyebrow">BOTSWANA · TELECOM SERVICE INTELLIGENCE</div>', unsafe_allow_html=True)
    st.title("TelecomInsight BW")
    st.markdown('<div class="hero-subtitle">Explore service quality, customer experience and location-level patterns.</div>', unsafe_allow_html=True)
with head_right:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="status-pill">● PROTOTYPE ONLINE</div>', unsafe_allow_html=True)

if using_sample:
    st.markdown('<div class="info-banner"><strong>DEMO DATA</strong> · The included records are fictional. Map points use approximate city-centre coordinates to illustrate geographic analysis; they are not measured network coverage or tower locations.</div>', unsafe_allow_html=True)
else:
    st.markdown('<div class="info-banner"><strong>UPLOADED DATA</strong> · Results depend on your dataset. Map markers use approximate city-centre coordinates for recognized locations unless your CSV includes valid latitude and longitude columns.</div>', unsafe_allow_html=True)

if filtered.empty:
    st.warning("No records match your selected filters. Adjust the filters in the sidebar.")
    st.stop()

st.markdown('<div class="section-label">SERVICE QUALITY SNAPSHOT</div>', unsafe_allow_html=True)
complaints = int(filtered["complaint_reported"].fillna(0).sum())
avg_download = filtered["download_mbps"].mean()
avg_latency = filtered["latency_ms"].mean()
m1, m2, m3, m4 = st.columns(4)
m1.metric("Records analysed", f"{len(filtered):,}")
m2.metric("Complaint reports", f"{complaints:,}")
m3.metric("Avg. download speed", f"{avg_download:.1f} Mbps")
m4.metric("Avg. latency", f"{avg_latency:.0f} ms")

# ------------------------------------------------------------
# Geographic analysis
# ------------------------------------------------------------
st.markdown("## Geographic service analysis")
st.caption("Compare record volume, reported complaints and average network performance by location.")

geo = filtered.copy()
if "latitude" in geo.columns and "longitude" in geo.columns:
    geo["latitude"] = pd.to_numeric(geo["latitude"], errors="coerce")
    geo["longitude"] = pd.to_numeric(geo["longitude"], errors="coerce")
    geo = geo.dropna(subset=["latitude", "longitude"])
    geo = geo[
        geo["latitude"].between(-27.5, -17.0)
        & geo["longitude"].between(19.0, 30.0)
    ]
    coord_source = "uploaded coordinates"
else:
    geo["latitude"] = geo["location"].map(lambda name: LOCATION_COORDS.get(name, {}).get("lat"))
    geo["longitude"] = geo["location"].map(lambda name: LOCATION_COORDS.get(name, {}).get("lon"))
    geo = geo.dropna(subset=["latitude", "longitude"])
    coord_source = "approximate city-centre coordinates"

if geo.empty:
    st.info("No recognized Botswana locations or valid latitude/longitude coordinates were found. Add latitude and longitude columns to your CSV, or use recognized location names such as Gaborone, Francistown, Maun or Palapye.")
else:
    geo_summary = (
        geo.groupby("location", as_index=False)
        .agg(
            latitude=("latitude", "mean"),
            longitude=("longitude", "mean"),
            records=("location", "size"),
            complaints=("complaint_reported", "sum"),
            avg_download_mbps=("download_mbps", "mean"),
            avg_latency_ms=("latency_ms", "mean"),
            avg_satisfaction=("satisfaction", "mean"),
        )
    )
    geo_summary["complaint_rate_pct"] = (geo_summary["complaints"] / geo_summary["records"] * 100).round(1)
    geo_summary["avg_download_mbps"] = geo_summary["avg_download_mbps"].round(1)
    geo_summary["avg_latency_ms"] = geo_summary["avg_latency_ms"].round(1)
    geo_summary["avg_satisfaction"] = geo_summary["avg_satisfaction"].round(2)

    map_left, map_right = st.columns([1.65, 1], gap="large")
    with map_left:
        st.markdown("### Botswana location map")
        st.caption(f"Marker positions are based on {coord_source}. Marker size reflects number of records, not coverage.")
        map_metric = st.selectbox(
            "Colour markers by",
            ["Complaint rate (%)", "Average download speed (Mbps)", "Average latency (ms)", "Records"],
            key="geo_map_metric",
        )
        metric_columns = {
            "Complaint rate (%)": "complaint_rate_pct",
            "Average download speed (Mbps)": "avg_download_mbps",
            "Average latency (ms)": "avg_latency_ms",
            "Records": "records",
        }
        colour_column = metric_columns[map_metric]
        fig_map = px.scatter_geo(
            geo_summary,
            lat="latitude",
            lon="longitude",
            size="records",
            color=colour_column,
            hover_name="location",
            hover_data={
                "records": True,
                "complaints": True,
                "complaint_rate_pct": True,
                "avg_download_mbps": True,
                "avg_latency_ms": True,
                "avg_satisfaction": True,
                "latitude": False,
                "longitude": False,
            },
            color_continuous_scale=["#DCD5FF", PURPLE, ROYAL_BLUE],
            projection="mercator",
            fitbounds="locations",
            height=500,
            labels={
                "complaint_rate_pct": "Complaint rate (%)",
                "avg_download_mbps": "Avg download (Mbps)",
                "avg_latency_ms": "Avg latency (ms)",
                "records": "Records",
                "complaints": "Complaint reports",
                "avg_satisfaction": "Avg satisfaction (1–5)",
            },
        )
        fig_map.update_layout(
            paper_bgcolor="#FFFFFF",
            margin=dict(l=0, r=0, t=5, b=0),
            font=dict(family="DM Sans, sans-serif", color=INK),
            coloraxis_colorbar=dict(title=map_metric),
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with map_right:
        st.markdown("### Location comparison")
        compare_metric = st.selectbox(
            "Compare locations by",
            ["Complaint rate (%)", "Average download speed (Mbps)", "Average latency (ms)", "Average satisfaction"],
            key="geo_compare_metric",
        )
        compare_cols = {
            "Complaint rate (%)": "complaint_rate_pct",
            "Average download speed (Mbps)": "avg_download_mbps",
            "Average latency (ms)": "avg_latency_ms",
            "Average satisfaction": "avg_satisfaction",
        }
        compare_col = compare_cols[compare_metric]
        compare = geo_summary.sort_values(compare_col, ascending=(compare_col in ["complaint_rate_pct", "avg_latency_ms"]))
        fig_compare = px.bar(
            compare,
            x=compare_col,
            y="location",
            orientation="h",
            text=compare_col,
            color=compare_col,
            color_continuous_scale=["#DCD5FF", PURPLE, ROYAL_BLUE],
            labels={compare_col: compare_metric, "location": "Location"},
        )
        fig_compare.update_traces(textposition="outside", cliponaxis=False)
        fig_compare.update_layout(coloraxis_showscale=False)
        st.plotly_chart(style_chart(fig_compare, 500), use_container_width=True)

    st.markdown("### Geographic summary table")
    st.dataframe(
        geo_summary[
            ["location", "records", "complaints", "complaint_rate_pct", "avg_download_mbps", "avg_latency_ms", "avg_satisfaction"]
        ].rename(columns={
            "location": "Location",
            "records": "Records",
            "complaints": "Complaint reports",
            "complaint_rate_pct": "Complaint rate (%)",
            "avg_download_mbps": "Avg download (Mbps)",
            "avg_latency_ms": "Avg latency (ms)",
            "avg_satisfaction": "Avg satisfaction (1–5)",
        }),
        use_container_width=True,
        hide_index=True,
    )
    st.download_button(
        "Download geographic summary CSV",
        geo_summary.to_csv(index=False).encode("utf-8"),
        "telecominsight_geographic_summary.csv",
        "text/csv",
    )

# ------------------------------------------------------------
# Existing charts and records
# ------------------------------------------------------------
c1, c2 = st.columns(2, gap="large")
with c1:
    st.markdown("### Most reported issues")
    st.caption("Number of records by issue type")
    issue_counts = filtered.groupby("issue_type", as_index=False).size().rename(columns={"size": "records"}).sort_values("records", ascending=True)
    fig = px.bar(issue_counts, x="records", y="issue_type", orientation="h", text="records", color="records",
                 color_continuous_scale=["#DCD5FF", PURPLE], labels={"issue_type": "Issue type", "records": "Records"})
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig, 340), use_container_width=True)

with c2:
    st.markdown("### Complaint reports by provider")
    st.caption("Total complaint reports in the selected records")
    provider_counts = filtered.groupby("provider", as_index=False)["complaint_reported"].sum().sort_values("complaint_reported", ascending=True)
    fig = px.bar(provider_counts, x="complaint_reported", y="provider", orientation="h", text="complaint_reported",
                 color="complaint_reported", color_continuous_scale=["#CFE0FF", ROYAL_BLUE],
                 labels={"provider": "Provider", "complaint_reported": "Complaint reports"})
    fig.update_traces(textposition="outside", cliponaxis=False)
    fig.update_layout(coloraxis_showscale=False)
    st.plotly_chart(style_chart(fig, 340), use_container_width=True)

st.markdown("### Network performance trend")
st.caption("Daily averages across the selected records")
metric_choice = st.radio("Metric", ["Download speed (Mbps)", "Latency (ms)"], horizontal=True, label_visibility="collapsed")
daily = filtered.assign(day=filtered["date"].dt.date).groupby("day", as_index=False).agg(
    download_mbps=("download_mbps", "mean"), latency_ms=("latency_ms", "mean")
)
if metric_choice.startswith("Download"):
    fig = px.line(daily, x="day", y="download_mbps", markers=True, labels={"day": "Date", "download_mbps": "Average download (Mbps)"})
    fig.update_traces(line=dict(color=PURPLE, width=3), marker=dict(size=7, color=ROYAL_BLUE))
else:
    fig = px.line(daily, x="day", y="latency_ms", markers=True, labels={"day": "Date", "latency_ms": "Average latency (ms)"})
    fig.update_traces(line=dict(color=ROYAL_BLUE, width=3), marker=dict(size=7, color=PURPLE))
st.plotly_chart(style_chart(fig, 360), use_container_width=True)

issue_counts_for_insight = filtered["issue_type"].value_counts()
top_issue_text = issue_counts_for_insight.index[0] if not issue_counts_for_insight.empty else "No issue data"
avg_satisfaction = filtered["satisfaction"].mean()
satisfaction_text = f"{avg_satisfaction:.1f}/5" if pd.notna(avg_satisfaction) else "Not available"
st.markdown(
    f'<div class="info-banner"><strong>QUICK INSIGHT</strong> · The most frequently recorded issue in this selection is <strong>{top_issue_text}</strong>. Average customer satisfaction is <strong>{satisfaction_text}</strong>. These are observations about the selected dataset, not conclusions about all telecom users or providers.</div>',
    unsafe_allow_html=True,
)

with st.expander("View filtered records and export data", expanded=False):
    display_df = filtered.sort_values("date", ascending=False).copy()
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    st.download_button("Download filtered data as CSV", display_df.to_csv(index=False).encode("utf-8"), "telecominsight_filtered_data.csv", "text/csv")

st.markdown('<div class="footer-note">TELECOMINSIGHT BW · Service-quality analytics prototype · Validate data before making decisions</div>', unsafe_allow_html=True)
