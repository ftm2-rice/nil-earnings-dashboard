import streamlit as st
import pandas as pd
import plotly.express as px

# Page Setup
st.set_page_config(page_title="NIL Earnings Dashboard", layout="wide")
st.title("College Athlete N.I.L. Earnings Estimates")

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("Athletes_Earnings_Estimates.csv")

df = load_data()

# Split panels
major_df = df[df['Panel'] == 'Major'].sort_values(by='Earnings', ascending=True)
nonrev_df = df[df['Panel'] == 'Nonrevenue'].sort_values(by='Earnings', ascending=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Average earnings of college athletes in major sports")
    fig1 = px.bar(
        major_df, 
        x='Earnings', 
        y='Sport', 
        orientation='h',
        text_auto='.2s',
        labels={'Earnings': 'Expected Annual Earnings ($)', 'Sport': ''}
    )
    fig1.update_traces(
        marker_color='white', 
        marker_line_color='#888888', 
        marker_line_width=1.5,
        hovertemplate="<b>%{y}</b><br>Average Earnings: $%{x:,.0f}<extra></extra>"
    )
    fig1.update_layout(
        xaxis_tickformat="$",
        xaxis=dict(side="top"),
        plot_bgcolor="white",
        xaxis_gridcolor="#d3d3d3",
        height=700
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader('Average earnings of college athletes in "nonrevenue" sports')
    
    # Highlight Track & Field
    colors = ['#d9534f' if 'track' in sport.lower() else 'white' for sport in nonrev_df['Sport']]
    
    fig2 = px.bar(
        nonrev_df, 
        x='Earnings', 
        y='Sport', 
        orientation='h',
        text_auto='.2s',
        labels={'Earnings': 'Expected Annual Earnings ($)', 'Sport': ''}
    )
    fig2.update_traces(
        marker_color=colors, 
        marker_line_color='#888888', 
        marker_line_width=1.5,
        hovertemplate="<b>%{y}</b><br>Average Earnings: $%{x:,.0f}<extra></extra>"
    )
    fig2.update_layout(
        xaxis_tickformat="$",
        xaxis=dict(side="top"),
        plot_bgcolor="white",
        xaxis_gridcolor="#d3d3d3",
        height=700
    )
    st.plotly_chart(fig2, use_container_width=True)

# Footer Source Text
st.caption(
    "Source: Opendorse. N.I.L. transactions disclosed through or processed by Opendorse between July 1, 2021 - June 30, 2024. "
    "Players' expected annual earnings must rank in the top 25 at their position. Track/Cross Country includes track and field. "
    "Values estimated from the published bars."
)