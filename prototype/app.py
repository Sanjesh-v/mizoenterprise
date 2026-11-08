import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# ==========================================
# MIZOENTERPRISE - VERSION 1.0 MVP
# ==========================================

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

st.set_page_config(
    page_title="MizoEnterprise",
    page_icon="🏭",
    layout="wide"
)

@st.cache_data
def load_csv(filename):
    path = DATA / filename
    if not path.exists():
        raise FileNotFoundError(f"Missing dataset: {path}")
    return pd.read_csv(path)

enterprises = load_csv("enterprises.csv")
buyers = load_csv("buyers.csv")
diagnostics = load_csv("diagnostics.csv")

st.markdown("""
<style>
.stApp {
    background-color: #F7F8F4;
    color: #26352B;
}
h1, h2, h3 {
    color: #174D35 !important;
}
[data-testid="stSidebar"] {
    background-color: #174D35;
}
[data-testid="stSidebar"] * {
    color: white !important;
}
[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #DCE7DC;
    padding: 16px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("🏭 MizoEnterprise")
st.subheader(
    "Rural MSME Development and Market Linkage Platform"
)

st.write(
    "Mapping rural enterprises, understanding business "
    "constraints and exploring market opportunities."
)

st.warning(
    "DEMONSTRATION MODE: All enterprise records, capacity "
    "figures, buyer profiles and diagnostic scores are synthetic. "
    "They are not verified business observations."
)

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Enterprise Directory",
        "Business Diagnostics",
        "Buyer Discovery",
        "Cluster Insights",
        "About & Methodology"
    ]
)

# ------------------------------------------
# DASHBOARD
# ------------------------------------------

if page == "Dashboard":

    st.header("Rural Enterprise Overview")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Sample Enterprises", len(enterprises))
    c2.metric("Clusters Represented", enterprises["village"].nunique())
    c3.metric("Industries", enterprises["industry"].nunique())
    c4.metric("Sample Buyers", len(buyers))

    st.divider()

    left, right = st.columns(2)

    with left:
        industry_counts = (
            enterprises.groupby("industry")
            .size()
            .reset_index(name="count")
        )

        fig = px.bar(
            industry_counts,
            x="industry",
            y="count",
            color="industry",
            title="Illustrative Enterprise Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        village_counts = (
            enterprises.groupby("village")
            .size()
            .reset_index(name="count")
        )

        fig = px.pie(
            village_counts,
            names="village",
            values="count",
            title="Illustrative Cluster Distribution"
        )
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Sample Enterprise Records")
    st.dataframe(enterprises, use_container_width=True, hide_index=True)

# ------------------------------------------
# ENTERPRISE DIRECTORY
# ------------------------------------------

elif page == "Enterprise Directory":

    st.header("Enterprise Directory")

    industries = st.multiselect(
        "Select industries",
        sorted(enterprises["industry"].unique()),
        default=sorted(enterprises["industry"].unique())
    )

    villages = st.multiselect(
        "Select clusters",
        sorted(enterprises["village"].unique()),
        default=sorted(enterprises["village"].unique())
    )

    filtered = enterprises[
        enterprises["industry"].isin(industries)
        & enterprises["village"].isin(villages)
    ]

    st.metric("Matching Sample Enterprises", len(filtered))

    st.dataframe(filtered, use_container_width=True, hide_index=True)

# ------------------------------------------
# BUSINESS DIAGNOSTICS
# ------------------------------------------

elif page == "Business Diagnostics":

    st.header("Business Diagnostics")

    st.write(
        "Explore illustrative categories for assessing "
        "operational and market-access challenges."
    )

    fig = px.bar(
        diagnostics,
        x="enterprise_id",
        y="illustrative_severity",
        color="challenge_category",
        title="Synthetic Diagnostic Scores",
        labels={
            "enterprise_id": "Enterprise",
            "illustrative_severity": "Illustrative Score"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(
        diagnostics,
        use_container_width=True,
        hide_index=True
    )

    st.info(
        "Scores are synthetic placeholders, not actual business "
        "assessments. A real diagnostic framework must be "
        "developed and validated with enterprise owners."
    )

# ------------------------------------------
# BUYER DISCOVERY
# ------------------------------------------

elif page == "Buyer Discovery":

    st.header("Buyer Discovery")

    industry = st.selectbox(
        "Select industry",
        ["All"] + sorted(buyers["interested_industry"].unique())
    )

    if industry == "All":
        filtered = buyers.copy()
    else:
        filtered = buyers[
            buyers["interested_industry"] == industry
        ]

    st.dataframe(filtered, use_container_width=True, hide_index=True)

    st.info(
        "Buyer profiles are fictional examples. Real buyer "
        "information requires verification and appropriate consent."
    )

# ------------------------------------------
# CLUSTER INSIGHTS
# ------------------------------------------

elif page == "Cluster Insights":

    st.header("Cluster Insights")

    fig = px.bar(
        enterprises,
        x="village",
        y="monthly_capacity_units",
        color="industry",
        barmode="group",
        title="Illustrative Enterprise Capacity"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Questions for Field Investigation")

    st.markdown("""
    - Which enterprises are concentrated in each cluster?
    - What are their production constraints?
    - How do they source raw materials?
    - Which buyer segments offer realistic opportunities?
    - Could shared facilities reduce operating constraints?
    - Which government schemes are relevant and accessible?
    """)

    st.warning(
        "These are research questions, not verified conclusions."
    )

# ------------------------------------------
# ABOUT AND METHODOLOGY
# ------------------------------------------

elif page == "About & Methodology":

    st.header("About MizoEnterprise")

    st.write("""
    MizoEnterprise is a proposed rural enterprise-development
    initiative focused on understanding the operational and
    market-access challenges of traditional industries and MSMEs
    in Mizoram.
    """)

    st.subheader("Research Methodology")

    st.markdown("""
    1. Review secondary reports and government information.
    2. Map selected rural enterprise clusters.
    3. Interview enterprise owners and artisans.
    4. Consult buyers, retailers and wholesalers.
    5. Analyse business and market-access constraints.
    6. Validate proposed interventions with stakeholders.
    """)

    st.subheader("Proposed Research Clusters")

    st.markdown("""
    - Baktawng: Furniture and carpentry
    - Thenzawl: Handloom
    - Reiek: Turmeric processing
    - Bamboo-based enterprises: To be identified
    """)

    st.info(
        "Current status: Concept development and demonstration "
        "MVP. Primary field validation is pending."
    )

    st.caption(
        "MizoEnterprise | Version 1.0 MVP | IIT Madras | "
        "New India Internship proposal"
    )
