import streamlit as st
# import snowflake.connector
from databricks import sql
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─────────────────────────────────────────
# PAGE CONFIG & CUSTOM CSS
# ─────────────────────────────────────────
st.set_page_config(
    page_title="Airbnb Analytics",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .stApp { background-color: #0f1117; }

    .kpi-card {
        background: linear-gradient(135deg, #1a1d2e, #252840);
        border: 1px solid #2e3250;
        border-radius: 12px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-label {
        font-size: 11px;
        color: #8b8fa8;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 30px;
        font-weight: 700;
        color: #ffffff;
        line-height: 1;
    }
    .kpi-icon { font-size: 18px; margin-bottom: 6px; }

    .section-header {
        font-size: 13px;
        font-weight: 600;
        color: #8b8fa8;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        padding: 4px 0 12px 0;
        border-bottom: 1px solid #2e3250;
        margin-bottom: 16px;
    }

    section[data-testid="stSidebar"] {
        background-color: #13151f;
        border-right: 1px solid #2e3250;
    }

    .block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
    hr { border-color: #2e3250 !important; }

    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] { background-color: #1a1d2e; border-radius: 8px; }
    .stTabs [data-baseweb="tab"] { color: #8b8fa8; }
    .stTabs [aria-selected="true"] { color: #FF5A5F !important; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────
# SNOWFLAKE CONNECTION
# ─────────────────────────────────────────
# @st.cache_resource
# def get_connection():
#     return snowflake.connector.connect(
#         account   = st.secrets["snowflake"]["account"],
#         user      = st.secrets["snowflake"]["user"],
#         password  = st.secrets["snowflake"]["password"],
#         warehouse = "COMPUTE_WH",
#         database  = "AIRBNB",
#         schema    = "DEV"
#     )

@st.cache_resource
def get_connection():
    return sql.connect(
        server_hostname = st.secrets["databricks"]["host"],
        http_path       = st.secrets["databricks"]["http_path"],
        access_token    = st.secrets["databricks"]["token"]
    )

# @st.cache_data(ttl=3600)
# def load_data():
#     conn = get_connection()
#     query = """
#         SELECT
#             ACCOMMODATES,
#             BEDROOMS,
#             BATHROOMS,
#             PRICE_PER_NIGHT,
#             PRICE_PER_NIGHT_TAG,
#             HOST_NAME,
#             IS_SUPERHOST,
#             RESPONSE_RATE,
#             RESPONSE_RATE_QUALITY,
#             TO_TIMESTAMP(HOST_SINCE)   AS HOST_SINCE,
#             TO_TIMESTAMP(BOOKING_DATE) AS BOOKING_DATE
#         FROM AIRBNB.GOLD.OBT
#     """
#     df = pd.read_sql(query, conn)
#     df.columns = df.columns.str.upper()
#     df["IS_SUPERHOST"]    = df["IS_SUPERHOST"].astype(bool)
#     df["BOOKING_DATE"]    = pd.to_datetime(df["BOOKING_DATE"], errors="coerce")
#     df["HOST_SINCE"]      = pd.to_datetime(df["HOST_SINCE"],   errors="coerce")
#     df["BOOKING_MONTH"]   = df["BOOKING_DATE"].dt.strftime("%Y-%m")
#     df["SUPERHOST_LABEL"] = df["IS_SUPERHOST"].map({True: "Superhost", False: "Non-Superhost"})
#     return df


@st.cache_data(ttl=3600)
def load_data():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT
                ACCOMMODATES, BEDROOMS, BATHROOMS,
                PRICE_PER_NIGHT, PRICE_PER_NIGHT_TAG,
                HOST_NAME, IS_SUPERHOST,
                RESPONSE_RATE, RESPONSE_RATE_QUALITY,
                CAST(HOST_SINCE   AS TIMESTAMP) AS HOST_SINCE,
                CAST(BOOKING_DATE AS TIMESTAMP) AS BOOKING_DATE
            FROM airbnb.gold.obt
        """)
        df = pd.DataFrame(
            cursor.fetchall(),
            columns=[d[0].upper() for d in cursor.description]
        )
    df["IS_SUPERHOST"]    = df["IS_SUPERHOST"].astype(bool)
    df["BOOKING_DATE"]    = pd.to_datetime(df["BOOKING_DATE"], errors="coerce")
    df["HOST_SINCE"]      = pd.to_datetime(df["HOST_SINCE"],   errors="coerce")
    df["BOOKING_MONTH"]   = df["BOOKING_DATE"].dt.strftime("%Y-%m")
    df["SUPERHOST_LABEL"] = df["IS_SUPERHOST"].map({True: "Superhost", False: "Non-Superhost"})
    return df


# ─────────────────────────────────────────
# THEME CONSTANTS
# ─────────────────────────────────────────
RED    = "#FF5A5F"
TEAL   = "#00A699"
BG     = "#13151f"
FONT_C = "#c9d1d9"
GRID_C = "#2e3250"

# Base layout — NO legend key here to avoid duplicate kwargs
def base_layout(title="", height=300):
    return dict(
        plot_bgcolor=BG, paper_bgcolor=BG,
        font=dict(color=FONT_C, family="Inter, sans-serif", size=12),
        xaxis=dict(gridcolor=GRID_C, showgrid=True, zeroline=False, tickfont=dict(size=11)),
        yaxis=dict(gridcolor=GRID_C, showgrid=True, zeroline=False, tickfont=dict(size=11)),
        margin=dict(l=10, r=10, t=40, b=30),
        hoverlabel=dict(bgcolor="#1e2130", font_size=12),
        title=title, height=height
    )

LEGEND_H = dict(bgcolor="rgba(0,0,0,0)", orientation="h", y=1.1, x=0, font=dict(size=11))

# ─────────────────────────────────────────
# SIDEBAR FILTERS
# ─────────────────────────────────────────
df_raw = load_data()

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding:10px 0 20px 0">
        <div style="font-size:32px">🏠</div>
        <div style="font-size:16px; font-weight:700; color:#fff">Airbnb Analytics</div>
        <div style="font-size:11px; color:#8b8fa8; margin-top:4px">Market Intelligence Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()
    st.markdown("**Filters**")

    price_tags = sorted(df_raw["PRICE_PER_NIGHT_TAG"].dropna().unique().tolist())
    sel_tags = st.multiselect("💰 Price Segment", price_tags, default=price_tags)

    sel_host = st.multiselect("⭐ Host Type", ["Superhost", "Non-Superhost"],
                               default=["Superhost", "Non-Superhost"])

    bed_min = int(df_raw["BEDROOMS"].min())
    bed_max = int(df_raw["BEDROOMS"].max())
    sel_beds = st.slider("🛏 Bedrooms", bed_min, bed_max, (bed_min, bed_max))

    months = sorted(df_raw["BOOKING_MONTH"].dropna().unique().tolist())
    if len(months) > 1:
        sel_months = st.select_slider("📅 Booking Period", options=months,
                                       value=(months[0], months[-1]))
    else:
        sel_months = (months[0], months[0]) if months else (None, None)

    st.divider()
    st.caption(f"🕐 {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")

# ─────────────────────────────────────────
# APPLY FILTERS
# ─────────────────────────────────────────
df = df_raw.copy()
if sel_tags:    df = df[df["PRICE_PER_NIGHT_TAG"].isin(sel_tags)]
if sel_host:    df = df[df["SUPERHOST_LABEL"].isin(sel_host)]
df = df[df["BEDROOMS"].between(sel_beds[0], sel_beds[1])]
if sel_months[0]:
    df = df[df["BOOKING_MONTH"].between(sel_months[0], sel_months[1])]

# ─────────────────────────────────────────
# HEADER
# ─────────────────────────────────────────
st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:4px">
    <div>
        <h1 style="margin:0; color:#fff; font-size:26px; font-weight:700">
            🏠 Airbnb Market Intelligence
        </h1>
        <p style="margin:2px 0 0 0; color:#8b8fa8; font-size:12px">
            AWS S3 → Snowflake → dbt (Bronze/Silver/Gold) → Streamlit
        </p>
    </div>
    <div style="text-align:right; color:#8b8fa8; font-size:12px">
        Showing <strong style="color:#fff">{len(df):,}</strong> of
        <strong style="color:#fff">{len(df_raw):,}</strong> records
    </div>
</div>
""", unsafe_allow_html=True)
st.divider()

# ─────────────────────────────────────────
# KPI ROW
# ─────────────────────────────────────────
def kpi(col, icon, label, value):
    col.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-icon">{icon}</div>
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
    </div>""", unsafe_allow_html=True)

k1, k2, k3, k4, k5, k6 = st.columns(6)
kpi(k1, "📋", "Total Bookings",    f"{len(df):,}")
kpi(k2, "👤", "Unique Hosts",      f"{df['HOST_NAME'].nunique():,}")
kpi(k3, "💵", "Avg Price / Night", f"${df['PRICE_PER_NIGHT'].mean():.0f}")
kpi(k4, "📊", "Median Price",      f"${df['PRICE_PER_NIGHT'].median():.0f}")
kpi(k5, "⭐", "Superhost Rate",    f"{df['IS_SUPERHOST'].mean()*100:.1f}%")
kpi(k6, "🏡", "Avg Guests",        f"{df['ACCOMMODATES'].mean():.1f}")
st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────
# ROW 1 — BOOKING TRENDS (full width)
# ─────────────────────────────────────────
st.markdown('<div class="section-header">📅 Booking Trends Over Time</div>',
            unsafe_allow_html=True)

trend = (
    df.groupby("BOOKING_MONTH")
    .agg(BOOKINGS=("PRICE_PER_NIGHT", "count"),
         AVG_PRICE=("PRICE_PER_NIGHT", "mean"))
    .reset_index().sort_values("BOOKING_MONTH").dropna()
)

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(go.Bar(
    x=trend["BOOKING_MONTH"], y=trend["BOOKINGS"], name="Bookings",
    marker_color=RED, opacity=0.8,
    hovertemplate="<b>%{x}</b><br>Bookings: %{y:,}<extra></extra>"
), secondary_y=False)
fig.add_trace(go.Scatter(
    x=trend["BOOKING_MONTH"], y=trend["AVG_PRICE"], name="Avg Price ($)",
    line=dict(color=TEAL, width=2.5), mode="lines+markers",
    marker=dict(size=7, color=TEAL),
    hovertemplate="<b>%{x}</b><br>Avg Price: $%{y:.0f}<extra></extra>"
), secondary_y=True)
fig.update_layout(
    **base_layout(height=300),
    legend=LEGEND_H,
    hovermode="x unified"
)
fig.update_yaxes(title_text="Bookings",    secondary_y=False, gridcolor=GRID_C)
fig.update_yaxes(title_text="Avg Price ($)", secondary_y=True, gridcolor=GRID_C,
                 tickprefix="$", color=TEAL)
fig.update_xaxes(tickangle=30)
st.plotly_chart(fig, width='stretch')

# ─────────────────────────────────────────
# ROW 2 — PRICE INTELLIGENCE
# ─────────────────────────────────────────
st.markdown('<div class="section-header">💰 Price Intelligence</div>',
            unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    avg_bed = (df.groupby("BEDROOMS")["PRICE_PER_NIGHT"].mean()
               .reset_index().sort_values("PRICE_PER_NIGHT", ascending=True))
    fig = go.Figure(go.Bar(
        x=avg_bed["PRICE_PER_NIGHT"], y=avg_bed["BEDROOMS"].astype(str),
        orientation="h",
        marker=dict(color=avg_bed["PRICE_PER_NIGHT"],
                    colorscale=[[0, "#1a3a5c"], [0.5, TEAL], [1, RED]]),
        text=avg_bed["PRICE_PER_NIGHT"].apply(lambda x: f"${x:.0f}"),
        textposition="outside", textfont=dict(color=FONT_C, size=11),
        hovertemplate="<b>%{y} beds</b><br>Avg: $%{x:.0f}<extra></extra>"
    ))
    fig.update_layout(**base_layout("Avg Price by Bedrooms", 280),
                      xaxis_title="Avg Price ($)", yaxis_title="Bedrooms")
    st.plotly_chart(fig, width='stretch')

with c2:
    tag_counts = df["PRICE_PER_NIGHT_TAG"].value_counts().reset_index()
    tag_counts.columns = ["TAG", "COUNT"]
    fig = go.Figure(go.Pie(
        labels=tag_counts["TAG"], values=tag_counts["COUNT"], hole=0.6,
        marker=dict(colors=[RED, TEAL, "#7b68ee", "#ffa07a"],
                    line=dict(color=BG, width=2)),
        textinfo="label+percent", textfont=dict(color=FONT_C, size=11),
        hovertemplate="<b>%{label}</b><br>%{value:,} listings (%{percent})<extra></extra>"
    ))
    fig.update_layout(
        **base_layout("Listing Price Segments", 280),
        showlegend=False,
        annotations=[dict(text=f"<b>{len(df):,}</b><br>listings",
                          x=0.5, y=0.5, font_size=14, font_color=FONT_C, showarrow=False)]
    )
    st.plotly_chart(fig, width='stretch')

with c3:
    fig = px.violin(
        df, x="PRICE_PER_NIGHT_TAG", y="PRICE_PER_NIGHT",
        color="PRICE_PER_NIGHT_TAG",
        color_discrete_sequence=[RED, TEAL, "#7b68ee"],
        box=True, points=False,
        labels={"PRICE_PER_NIGHT": "Price/Night ($)", "PRICE_PER_NIGHT_TAG": ""},
        title="Price Spread by Segment"
    )
    fig.update_layout(**base_layout("Price Spread by Segment", 280), showlegend=False)
    st.plotly_chart(fig, width='stretch')

# ─────────────────────────────────────────
# ROW 3 — HOST INSIGHTS
# ─────────────────────────────────────────
st.markdown('<div class="section-header">👤 Host Insights</div>',
            unsafe_allow_html=True)
c1, c2, c3 = st.columns(3)

with c1:
    sh = (df.groupby("SUPERHOST_LABEL")["PRICE_PER_NIGHT"]
          .agg(Avg="mean", Median="median").reset_index())
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Avg Price", x=sh["SUPERHOST_LABEL"], y=sh["Avg"],
        marker_color=[RED, "#555"],
        text=sh["Avg"].apply(lambda x: f"${x:.0f}"),
        textposition="outside", textfont=dict(color=FONT_C)
    ))
    fig.add_trace(go.Bar(
        name="Median Price", x=sh["SUPERHOST_LABEL"], y=sh["Median"],
        marker_color=[TEAL, "#333"],
        text=sh["Median"].apply(lambda x: f"${x:.0f}"),
        textposition="outside", textfont=dict(color=FONT_C)
    ))
    fig.update_layout(**base_layout("Superhost Pricing Premium", 300),
                      barmode="group", legend=LEGEND_H)
    st.plotly_chart(fig, width='stretch')

with c2:
    rr = df["RESPONSE_RATE_QUALITY"].value_counts().reset_index()
    rr.columns = ["QUALITY", "COUNT"]
    rr["PCT"] = (rr["COUNT"] / rr["COUNT"].sum() * 100).round(1)
    color_map = {"GOOD": TEAL, "FAIR": "#ffa07a", "POOR": RED}
    fig = go.Figure(go.Bar(
        x=rr["QUALITY"], y=rr["COUNT"],
        marker_color=[color_map.get(q, "#888") for q in rr["QUALITY"]],
        text=rr["PCT"].apply(lambda x: f"{x:.1f}%"),
        textposition="outside", textfont=dict(color=FONT_C),
        hovertemplate="<b>%{x}</b><br>%{y:,} hosts (%{text})<extra></extra>"
    ))
    fig.update_layout(**base_layout("Host Response Rate Quality", 300),
                      showlegend=False, xaxis_title="", yaxis_title="Hosts")
    st.plotly_chart(fig, width='stretch')

with c3:
    host_agg = (
        df.dropna(subset=["HOST_SINCE"])
        .groupby("HOST_NAME")
        .agg(AVG_PRICE=("PRICE_PER_NIGHT", "mean"),
             BOOKINGS=("PRICE_PER_NIGHT", "count"),
             SUPERHOST=("SUPERHOST_LABEL", "first"),
             HOST_YEAR=("HOST_SINCE", lambda x: x.dt.year.iloc[0]))
        .reset_index()
    )
    fig = px.scatter(
        host_agg, x="HOST_YEAR", y="AVG_PRICE",
        color="SUPERHOST", size="BOOKINGS",
        color_discrete_map={"Superhost": RED, "Non-Superhost": TEAL},
        labels={"HOST_YEAR": "Year Joined", "AVG_PRICE": "Avg Price ($)", "SUPERHOST": ""},
        title="Host Tenure vs Avg Price", opacity=0.75,
        hover_data={"HOST_NAME": True, "BOOKINGS": True}
    )
    fig.update_layout(**base_layout("Host Tenure vs Avg Price", 300), legend=LEGEND_H)
    st.plotly_chart(fig, width='stretch')

# ─────────────────────────────────────────
# ROW 4 — DATA EXPLORER
# ─────────────────────────────────────────
st.markdown('<div class="section-header">🔍 Data Explorer</div>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 Segment Summary", "📋 Raw Records"])

with tab1:
    summary = (
        df.groupby(["PRICE_PER_NIGHT_TAG", "SUPERHOST_LABEL"])
        .agg(Bookings=("PRICE_PER_NIGHT", "count"),
             Avg_Price=("PRICE_PER_NIGHT", "mean"),
             Median_Price=("PRICE_PER_NIGHT", "median"),
             Avg_Bedrooms=("BEDROOMS", "mean"),
             Avg_Guests=("ACCOMMODATES", "mean"))
        .reset_index()
        .rename(columns={"PRICE_PER_NIGHT_TAG": "Segment", "SUPERHOST_LABEL": "Host Type"})
    )
    summary["Avg_Price"]    = summary["Avg_Price"].apply(lambda x: f"${x:.2f}")
    summary["Median_Price"] = summary["Median_Price"].apply(lambda x: f"${x:.2f}")
    summary["Avg_Bedrooms"] = summary["Avg_Bedrooms"].apply(lambda x: f"{x:.1f}")
    summary["Avg_Guests"]   = summary["Avg_Guests"].apply(lambda x: f"{x:.1f}")
    st.dataframe(summary, width='stretch', hide_index=True)

with tab2:
    cols = ["HOST_NAME", "SUPERHOST_LABEL", "PRICE_PER_NIGHT", "PRICE_PER_NIGHT_TAG",
            "BEDROOMS", "BATHROOMS", "ACCOMMODATES", "RESPONSE_RATE_QUALITY", "BOOKING_MONTH"]
    st.dataframe(
        df[cols].rename(columns={
            "HOST_NAME": "Host", "SUPERHOST_LABEL": "Type",
            "PRICE_PER_NIGHT": "Price/Night ($)", "PRICE_PER_NIGHT_TAG": "Segment",
            "BEDROOMS": "Beds", "BATHROOMS": "Baths", "ACCOMMODATES": "Guests",
            "RESPONSE_RATE_QUALITY": "Response Quality", "BOOKING_MONTH": "Month"
        }),
        width='stretch', hide_index=True
    )
    st.caption(f"Showing **{len(df):,}** of **{len(df_raw):,}** total records")

# ─────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────
st.divider()
st.markdown("""
<div style="display:flex; justify-content:space-between; color:#8b8fa8; font-size:11px; padding:4px 0">
    <span>Built by <strong style="color:#FF5A5F">Avikal Singh</strong></span>
    <span>AWS S3 → Snowflake → dbt (Bronze / Silver / Gold) → Streamlit</span>
    <span>Cache TTL: 1 hour</span>
</div>
""", unsafe_allow_html=True)


