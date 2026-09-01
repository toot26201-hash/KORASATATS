import os
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from mplsoccer import Pitch

# Page Configuration
st.set_page_config(page_title="Half-Space Passing Analytics", layout="wide")

st.title("⚽ Football Half-Space Passing & Spatial Analytics")

# ---------------------------------------------------------
# 1. File Upload Section
# ---------------------------------------------------------
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader(
    "Upload Players CSV File:", type=["csv"]
)


@st.cache_data
def load_data(file):
    return pd.read_csv(file)


if uploaded_file is None:
    st.info(
        "👋 Please upload your data file (`PlayersData_2215.csv`) from the sidebar to view half-space passing analytics."
    )
    st.stop()

df = load_data(uploaded_file)

# ---------------------------------------------------------
# 2. Player Selection & Spatial Filters
# ---------------------------------------------------------
selected_team = st.sidebar.selectbox(
    "Select Team:", sorted(df["Team"].dropna().unique())
)
team_players = df[df["Team"] == selected_team]

selected_player = st.sidebar.selectbox(
    "Select Player:", sorted(team_players["Full Name"].dropna().unique())
)
p_data = df[df["Full Name"] == selected_player].iloc[0]

st.sidebar.markdown("---")
st.sidebar.header("📐 Spatial Passing Filter")
pass_spatial_type = st.sidebar.radio(
    "Filter Pass Direction:",
    [
        "All Passes",
        "Passes INTO Half-Spaces",
        "Passes OUT OF Half-Spaces",
    ],
)

# ---------------------------------------------------------
# 3. Position Pitch Mapping Setup
# ---------------------------------------------------------
position_zones = {
    "GK": {"x": (5, 20), "y": (25, 55)},
    "CB": {"x": (20, 45), "y": (20, 60)},
    "LB": {"x": (25, 65), "y": (5, 25)},
    "RB": {"x": (25, 65), "y": (55, 75)},
    "DM": {"x": (35, 60), "y": (25, 55)},
    "CM": {"x": (45, 75), "y": (20, 60)},
    "LM": {"x": (50, 90), "y": (5, 25)},
    "RM": {"x": (50, 90), "y": (55, 75)},
    "AM": {"x": (65, 95), "y": (20, 60)},
    "LW": {"x": (70, 110), "y": (5, 30)},
    "RW": {"x": (70, 110), "y": (50, 75)},
    "CF": {"x": (80, 112), "y": (20, 60)},
    "ST": {"x": (80, 112), "y": (20, 60)},
}

pos = p_data.get("Primary Position", "CM")
zone = position_zones.get(pos, {"x": (40, 80), "y": (20, 60)})

np.random.seed(int(p_data["ID"]))

# ---------------------------------------------------------
# 4. Black Pitch Setup with Half-Space Vertical Lines
# ---------------------------------------------------------
pitch = Pitch(half=False, pitch_color="#000000", line_color="#ffffff")
fig, ax = pitch.draw(figsize=(13, 9))
fig.patch.set_facecolor("#000000")

# Draw Vertical Lines demarcating 5 Channels (Half-Spaces Y: 18 to 30 & 50 to 62)
# StatsBomb Pitch Y-bounds: 0 to 80
ax.axhline(18, color="#555555", linestyle="--", linewidth=1.2, zorder=2)
ax.axhline(30, color="#555555", linestyle="--", linewidth=1.2, zorder=2)
ax.axhline(50, color="#555555", linestyle="--", linewidth=1.2, zorder=2)
ax.axhline(62, color="#555555", linestyle="--", linewidth=1.2, zorder=2)

# Label Channels
ax.text(
    10,
    9,
    "Left Wing",
    color="#777777",
    fontsize=9,
    ha="center",
    fontweight="bold",
)
ax.text(
    10,
    24,
    "Left Half-Space",
    color="#00ff66",
    fontsize=9,
    ha="center",
    fontweight="bold",
)
ax.text(
    10,
    40,
    "Central Zone 14",
    color="#777777",
    fontsize=9,
    ha="center",
    fontweight="bold",
)
ax.text(
    10,
    56,
    "Right Half-Space",
    color="#00ff66",
    fontsize=9,
    ha="center",
    fontweight="bold",
)
ax.text(
    10,
    71,
    "Right Wing",
    color="#777777",
    fontsize=9,
    ha="center",
    fontweight="bold",
)

# Render Player Title
player_name_str = (
    f"{p_data['Full Name'].upper()} ({p_data['Team']}) - {pos} [{pass_spatial_type}]"
)
ax.text(
    60,
    77,
    player_name_str,
    color="#ffffff",
    fontsize=15,
    ha="center",
    va="center",
    fontweight="bold",
    zorder=10,
    bbox=dict(
        boxstyle="round,pad=0.4",
        facecolor="#1e1e1e",
        edgecolor="#00ff66",
        alpha=0.85,
    ),
)

# ---------------------------------------------------------
# 5. Generate Directional Half-Space Pass Vectors
# ---------------------------------------------------------
pass_success = int(p_data.get("Pass Success", 0))
s_cnt = min(pass_success, 30)

if s_cnt > 0:
    # 1. Passes INTO Half-Space (Start outside, End inside Y=18..30 or Y=50..62)
    if pass_spatial_type == "Passes INTO Half-Spaces":
        sx1 = np.random.uniform(zone["x"][0], zone["x"][1], s_cnt)
        sy1 = np.random.choice(
            [
                np.random.uniform(2, 16),
                np.random.uniform(32, 48),
                np.random.uniform(64, 78),
            ],
            s_cnt,
        )

        sx2 = np.clip(sx1 + np.random.uniform(10, 25, s_cnt), 5, 115)
        sy2 = np.random.choice(
            [np.random.uniform(19, 29), np.random.uniform(51, 61)], s_cnt
        )

        pitch.arrows(
            sx1,
            sy1,
            sx2,
            sy2,
            color="#00ff66",
            width=2.5,
            headwidth=4.5,
            headlength=4.5,
            ax=ax,
            label=f"Pass INTO Half-Space ({s_cnt})",
            zorder=4,
        )

    # 2. Passes OUT OF Half-Space (Start inside Y=18..30 or Y=50..62, End outside)
    elif pass_spatial_type == "Passes OUT OF Half-Spaces":
        sx1 = np.random.uniform(zone["x"][0], zone["x"][1], s_cnt)
        sy1 = np.random.choice(
            [np.random.uniform(19, 29), np.random.uniform(51, 61)], s_cnt
        )

        sx2 = np.clip(sx1 + np.random.uniform(10, 25, s_cnt), 5, 115)
        sy2 = np.random.choice(
            [np.random.uniform(32, 48), np.random.uniform(2, 16)], s_cnt
        )

        pitch.arrows(
            sx1,
            sy1,
            sx2,
            sy2,
            color="#00e5ff",
            width=2.5,
            headwidth=4.5,
            headlength=4.5,
            ax=ax,
            label=f"Pass OUT OF Half-Space ({s_cnt})",
            zorder=4,
        )

    # 3. All Passes Mode
    else:
        sx1 = np.random.uniform(zone["x"][0], zone["x"][1], s_cnt)
        sy1 = np.random.uniform(zone["y"][0], zone["y"][1], s_cnt)
        sx2 = np.clip(sx1 + np.random.uniform(8, 25, s_cnt), 5, 115)
        sy2 = np.clip(sy1 + np.random.uniform(-15, 15, s_cnt), 5, 75)

        pitch.arrows(
            sx1,
            sy1,
            sx2,
            sy2,
            color="#2ea043",
            width=2,
            headwidth=4,
            headlength=4,
            ax=ax,
            label=f"All Passes ({s_cnt})",
            zorder=4,
        )

# Pitch Legend Styling
ax.legend(
    facecolor="#1e1e1e",
    edgecolor="#ffffff",
    fontsize=10,
    labelcolor="white",
    loc="upper left",
)
st.pyplot(fig)

# ---------------------------------------------------------
# 6. Half-Space Metrics Overview
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 Passing Distribution Metrics")

col1, col2, col3 = st.columns(3)
col1.metric("Total Successful Passes", pass_success)
col2.metric("Pass Accuracy", f"{p_data.get('Pass Accuracy', 0)*100:.1f}%")
col3.metric("Key Passes Created", int(p_data.get("Chances KeyPasses", 0)))
