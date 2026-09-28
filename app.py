import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ---------------------------------------------------------------- page setup
st.set_page_config(page_title="NIL Earnings Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("Athletes_Earnings_Estimates.csv")

df = load_data()

# ---------------------------------------------------------------- sidebar controls
st.sidebar.header("Filter & Sort Controls")

selected_genders = st.sidebar.multiselect(
    "Filter by Gender",
    options=sorted(df["Gender"].unique()),
    default=sorted(df["Gender"].unique())
)

selected_categories = st.sidebar.multiselect(
    "Filter by Sport Category",
    options=sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

sort_option = st.sidebar.radio(
    "Sort Order",
    options=["Highest to Lowest", "Lowest to Highest", "Alphabetical (A-Z)"],
    index=0
)

# Apply filters
filtered_df = df[
    (df["Gender"].isin(selected_genders)) & 
    (df["Category"].isin(selected_categories))
]

# Apply sorting logic
if sort_option == "Highest to Lowest":
    major = filtered_df[filtered_df["Panel"] == "Major"].sort_values(["Earnings", "Sport"], ascending=True)
    nonrev = filtered_df[filtered_df["Panel"] == "Nonrevenue"].sort_values(["Earnings", "Sport"], ascending=True)
elif sort_option == "Lowest to Highest":
    major = filtered_df[filtered_df["Panel"] == "Major"].sort_values(["Earnings", "Sport"], ascending=False)
    nonrev = filtered_df[filtered_df["Panel"] == "Nonrevenue"].sort_values(["Earnings", "Sport"], ascending=False)
else:
    major = filtered_df[filtered_df["Panel"] == "Major"].sort_values("Sport", ascending=False)
    nonrev = filtered_df[filtered_df["Panel"] == "Nonrevenue"].sort_values("Sport", ascending=False)

# ---------------------------------------------------------------- gender KPI subtotals
st.markdown("### Gender Earnings Overview")

col1, col2, col3 = st.columns(3)

def get_gender_stats(data, gender_name):
    subset = data[data["Gender"] == gender_name]
    if len(subset) == 0:
        return "$0", "0 sports"
    avg_val = subset["Earnings"].mean()
    count = len(subset)
    return f"${avg_val:,.0f}", f"{count} sports tracked"

mens_avg, mens_count = get_gender_stats(filtered_df, "Men's")
womens_avg, womens_count = get_gender_stats(filtered_df, "Women's")
coed_avg, coed_count = get_gender_stats(filtered_df, "Coed / Open")

with col1:
    st.metric("Men's Average Earnings", mens_avg, mens_count)
with col2:
    st.metric("Women's Average Earnings", womens_avg, womens_count)
with col3:
    st.metric("Coed / Open Average Earnings", coed_avg, coed_count)

# Detailed Gender Subtotals Breakdown
with st.expander("View Subtotals Breakdown by Gender"):
    if not filtered_df.empty:
        gender_summary = filtered_df.groupby("Gender").agg(
            Sports_Count=("Sport", "count"),
            Average_Earnings=("Earnings", "mean"),
            Median_Earnings=("Earnings", "median"),
            Total_Earnings=("Earnings", "sum")
        ).reset_index()

        gender_summary["Average_Earnings"] = gender_summary["Average_Earnings"].apply(lambda x: f"${x:,.0f}")
        gender_summary["Median_Earnings"] = gender_summary["Median_Earnings"].apply(lambda x: f"${x:,.0f}")
        gender_summary["Total_Earnings"] = gender_summary["Total_Earnings"].apply(lambda x: f"${x:,.0f}")
        
        st.dataframe(gender_summary, width="stretch")
    else:
        st.info("No data available for the selected filters.")

# ---------------------------------------------------------------- figure setup
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.45, 0.55],
    subplot_titles=(
        "<b>Average earnings of college athletes in major sports</b>",
        '<b>Average earnings of college athletes in "nonrevenue" sports</b>'
    ),
    horizontal_spacing=0.12
)

# Panel 1: Major Sports
fig.add_trace(
    go.Bar(
        x=major["Earnings"],
        y=major["Sport"],
        orientation="h",
        marker=dict(color="white", line=dict(color="#333333", width=1)),
        hovertemplate="<b>%{y}</b><br>Gender: %{customdata[0]}<br>Category: %{customdata[1]}<br>Average Earnings: $%{x:,.0f}<extra></extra>",
        customdata=major[["Gender", "Category"]],
        name="",
        showlegend=False
    ),
    row=1, col=1
)

# Panel 2: Nonrevenue Sports (Highlighting Track/Cross Country)
nonrev_colors = [
    "#f16a5f" if "track/cross country" in s.lower() else "white"
    for s in nonrev["Sport"]
]

fig.add_trace(
    go.Bar(
        x=nonrev["Earnings"],
        y=nonrev["Sport"],
        orientation="h",
        marker=dict(color=nonrev_colors, line=dict(color="#333333", width=1)),
        hovertemplate="<b>%{y}</b><br>Gender: %{customdata[0]}<br>Category: %{customdata[1]}<br>Average Earnings: $%{x:,.0f}<extra></extra>",
        customdata=nonrev[["Gender", "Category"]],
        name="",
        showlegend=False
    ),
    row=1, col=2
)

# Narrative annotation for Olympic Track & Field impact
if "Men's track/cross country" in nonrev["Sport"].values:
    fig.add_annotation(
        text=(
            "Both men's and women's<br>track and field athletes<br>"
            "saw large increases in<br>expected earnings this<br>"
            "year, thanks in part to the<br>added exposure for these<br>"
            "sports at the Olympics<br>this year."
        ),
        xref="x2", yref="y2",
        x=14500, y="Men's track/cross country",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1,
        arrowcolor="#666666",
        ax=60, ay=180,
        font=dict(size=11, color="#333333", family="Helvetica, Arial, sans-serif"),
        align="left"
    )

# ---------------------------------------------------------------- layout & axis styling
fig.update_layout(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Helvetica, Arial, sans-serif", size=12, color="#333333"),
    height=950,
    bargap=0.38,
    margin=dict(l=20, r=20, t=120, b=40)
)

fig.update_xaxes(
    side="top", showgrid=True, gridcolor="#d9d9d9", zeroline=False,
    tickformat="$,d", tickvals=[200000, 400000, 600000], range=[0, 700000],
    tickfont=dict(color="#666666", size=11, family="Helvetica, Arial, sans-serif"),
    row=1, col=1
)

fig.update_yaxes(
    showline=True, linecolor="#333333", linewidth=1, gridcolor="rgba(0,0,0,0)",
    range=[-21.5, 3.5] if len(major) < 25 else None,
    tickfont=dict(color="#333333", size=11, family="Helvetica, Arial, sans-serif"),
    row=1, col=1
)

fig.update_xaxes(
    side="top", showgrid=True, gridcolor="#d9d9d9", zeroline=False,
    tickformat="$,d", tickvals=[5000, 10000, 15000, 20000], range=[0, 24000],
    tickfont=dict(color="#666666", size=11, family="Helvetica, Arial, sans-serif"),
    row=1, col=2
)

fig.update_yaxes(
    showline=True, linecolor="#333333", linewidth=1, gridcolor="rgba(0,0,0,0)",
    tickfont=dict(color="#333333", size=11, family="Helvetica, Arial, sans-serif"),
    row=1, col=2
)

for i in range(len(fig.layout.annotations)):
    if "Average earnings" in fig.layout.annotations[i].text:
        fig.layout.annotations[i].font.size = 13
        fig.layout.annotations[i].font.color = "#000000"
        fig.layout.annotations[i].xanchor = "left"
        fig.layout.annotations[i].x = 0 if i == 0 else 0.50
        fig.layout.annotations[i].y = 1.04

st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

st.caption(
    "Source: Opendorse. Data is based on N.I.L. transactions disclosed through or processed by "
    "Opendorse between July 1, 2021, and June 30, 2024. Note: To be included in the calculations, "
    "players' expected annual earnings must rank in the top 25 at their position. The Track/Cross "
    "Country category includes athletes in track and field. Values estimated from the published bars."
)

with st.expander("Full Data Table"):
    st.dataframe(filtered_df, width="stretch")
