import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ---------------------------------------------------------------- page setup
st.set_page_config(page_title="NIL Earnings Dashboard", layout="wide")

# NYT-ish typography: first font found on the system wins.
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = [
    "Helvetica Neue", "Helvetica", "Arial", "Liberation Sans", "DejaVu Sans",
]

GRID = "#d9d9d9"
EDGE = "#333333"
HILITE = "#f16a5f"
TEXT = "#333333"
MUTED = "#666666"


@st.cache_data
def load_data():
    return pd.read_csv("Athletes_Earnings_Estimates.csv")


df = load_data()
major = df[df["Panel"] == "Major"].sort_values("Earnings", ascending=False)
nonrev = df[df["Panel"] == "Nonrevenue"].sort_values("Earnings", ascending=False)

N_ROWS = len(nonrev)  # both panels use this row pitch so bars are the same height


def panel(ax, data, title, ticks):
    """Draw one NYT-style horizontal bar panel."""
    d = data.reset_index(drop=True)
    y = range(len(d))
    colors = [
        HILITE if "track/cross country" in s.lower() else "white" for s in d["Sport"]
    ]

    ax.barh(y, d["Earnings"], height=0.62, color=colors,
            edgecolor=EDGE, linewidth=0.9, zorder=3)

    ax.set_yticks(list(y))
    ax.set_yticklabels(d["Sport"], fontsize=9.5, color=TEXT)
    ax.set_ylim(N_ROWS - 0.5, -0.8)          # same pitch in both panels, top-aligned

    ax.set_title(title, loc="left", fontsize=11, fontweight="bold",
                 color="black", pad=22)

    ax.set_xlim(0, max(d["Earnings"].max() * 1.04, ticks[-1] * 1.06))
    ax.set_xticks(ticks)
    ax.xaxis.set_major_formatter("${x:,.0f}")
    ax.xaxis.tick_top()
    ax.tick_params(axis="x", length=0, labelsize=9.5, colors=MUTED, pad=6)
    ax.tick_params(axis="y", length=0, pad=6)

    ax.grid(axis="x", color=GRID, linewidth=0.9, zorder=0)
    ax.set_axisbelow(True)

    for side in ("top", "right", "bottom"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(EDGE)
    ax.spines["left"].set_linewidth(1.0)


# ------------------------------------------------------------------- figure
fig, (ax1, ax2) = plt.subplots(
    1, 2, figsize=(14, 9), gridspec_kw={"width_ratios": [1, 1.15], "wspace": 0.45}
)
fig.patch.set_facecolor("white")

panel(ax1, major, "Average earnings of college athletes in major sports",
      [200_000, 400_000, 600_000])
panel(ax2, nonrev, 'Average earnings of college athletes in "nonrevenue" sports',
      [5_000, 10_000, 15_000, 20_000])

ax2.annotate(
    "Both men's and women's\ntrack and field athletes\nsaw large increases in\n"
    "expected earnings this\nyear, thanks in part to the\nadded exposure for these\n"
    "sports at the Olympics\nthis year.",
    xy=(14_500, 4.45), xytext=(6_800, 14.2),
    fontsize=9, color=TEXT, linespacing=1.45,
    arrowprops=dict(arrowstyle="->", color=MUTED, linewidth=0.9,
                    shrinkA=14, shrinkB=4,
                    connectionstyle="arc3,rad=0.42"),
)

fig.subplots_adjust(top=0.90, bottom=0.10, left=0.13, right=0.97)
fig.text(
    0.02, 0.035,
    "Source: Opendorse. Data is based on N.I.L. transactions disclosed through or processed by "
    "Opendorse between July 1, 2021, and June 30, 2024. Note: To be included in the calculations, "
    "players' expected annual\nearnings must rank in the top 25 at their position. The Track/Cross "
    "Country category includes athletes in track and field. Values estimated from the published bars.",
    fontsize=8.5, color=MUTED, linespacing=1.5,
)

st.pyplot(fig, use_container_width=True)

with st.expander("Data"):
    st.dataframe(df, use_container_width=True)
