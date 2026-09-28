import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

# ---------------------------------------------------------------- page setup
st.set_page_config(page_title="NIL Earnings Dashboard", layout="wide")

# Load dataset
@st.cache_data
def load_data():
    return pd.read_csv("Athletes_Earnings_Estimates.csv")

df = load_data()

# Sort ascending with tie-breaker
major = df[df["Panel"] == "Major"].sort_values(["Earnings", "Sport"], ascending=True)
nonrev = df[df["Panel"] == "Nonrevenue"].sort_values(["Earnings", "Sport"], ascending=True)

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
        marker=dict(
            color="white",
            line=dict(color="#333333", width=1)
        ),
        hovertemplate="<b>%{y}</b><br>Average Earnings: $%{x:,.0f}<extra></extra>",
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
        marker=dict(
            color=nonrev_colors,
            line=dict(color="#333333", width=1)
        ),
        hovertemplate="<b>%{y}</b><br>Average Earnings: $%{x:,.0f}<extra></extra>",
        name="",
        showlegend=False
    ),
    row=1, col=2
)

# Narrative annotation for Olympic Track & Field impact
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

# Customize Left Panel X-Axis & Y-Axis
fig.update_xaxes(
    side="top",
    showgrid=True,
    gridcolor="#d9d9d9",
    zeroline=False,
    tickformat="$,d",
    tickvals=[200000, 400000, 600000],
    range=[0, 700000],
    row=1, col=1
)

fig.update_yaxes(
    showline=True, 
    linecolor="#333333", 
    linewidth=1, 
    gridcolor="rgba(0,0,0,0)", 
    range=[-21.5, 3.5], 
    row=1, col=1
)

# Customize Right Panel X-Axis & Y-Axis
fig.update_xaxes(
    side="top",
    showgrid=True,
    gridcolor="#d9d9d9",
    zeroline=False,
    tickformat="$,d",
    tickvals=[5000, 10000, 15000, 20000],
    range=[0, 24000],
    row=1, col=2
)

fig.update_yaxes(
    showline=True, 
    linecolor="#333333", 
    linewidth=1, 
    gridcolor="rgba(0,0,0,0)", 
    row=1, col=2
)

# Subtitle styling adjustment
for i in range(len(fig.layout.annotations)):
    if "Average earnings" in fig.layout.annotations[i].text:
        fig.layout.annotations[i].font.size = 13
        fig.layout.annotations[i].font.color = "#000000"
        fig.layout.annotations[i].xanchor = "left"
        fig.layout.annotations[i].x = 0 if i == 0 else 0.50
        fig.layout.annotations[i].y = 1.04

# Render dynamic plot in Streamlit
st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

# Footer Source Text
st.caption(
    "Source: Opendorse. Data is based on N.I.L. transactions disclosed through or processed by "
    "Opendorse between July 1, 2021, and June 30, 2024. Note: To be included in the calculations, "
    "players' expected annual earnings must rank in the top 25 at their position. The Track/Cross "
    "Country category includes athletes in track and field. Values estimated from the published bars."
)

with st.expander("Data Table"):
    st.dataframe(df, width="stretch")
