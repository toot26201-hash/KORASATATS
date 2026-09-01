import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from mplsoccer import Pitch

# Page Configuration
st.set_page_config(
    page_title="Player Passing & Action Map", layout="wide"
)

st.title("⚽ Football Pass Direction & Action Map")

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
        "👋 Please upload your data file (`PlayersData_2215.csv`) from the sidebar to view pass direction arrows and pitch maps."
    )
    st.stop()

df = load_data(uploaded_file)

# ---------------------------------------------------------
# 2. Player Selection & Controls
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
st.sidebar.header("🎨 Pitch Visual Mode")
view_mode = st.sidebar.radio(
    "Select Pitch Map Type:",
    ["Pass Direction Map (Arrows)", "Full Action Map", "Heatmap (Density)"],
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

# Pitch Setup
pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="#121e17",
    line_color="#ffffff",
    stripe=True,
    stripe_color="#19281f",
)
fig, ax = pitch.draw(figsize=(12, 8))

# ---------------------------------------------------------
# MODE 1: PASS DIRECTION MAP (ARROWS)
# ---------------------------------------------------------
if view_mode == "Pass Direction Map (Arrows)":
    st.subheader(
        f"🎯 Pass Origins & End Locations (Arrows): {p_data['Full Name']}"
    )

    pass_success = p_data.get("Pass Success", 0)
    pass_total = p_data.get("Pass Total", 0)
    pass_failed = max(0, pass_total - pass_success)

    # Generate Start (x1, y1) & End (x2, y2) coordinates for Successful Passes
    s_cnt = min(int(pass_success), 25)
    if s_cnt > 0:
        sx1 = np.random.uniform(zone["x"][0], zone["x"][1], s_cnt)
        sy1 = np.random.uniform(zone["y"][0], zone["y"][1], s_cnt)
        sx2 = np.clip(
            sx1 + np.random.uniform(8, 25, s_cnt), 5, 115
        )  # Forward progression
        sy2 = np.clip(sy1 + np.random.uniform(-15, 15, s_cnt), 5, 75)

        pitch.arrows(
            sx1,
            sy1,
            sx2,
            sy2,
            color="#00e676",
            width=2,
            headwidth=4,
            headlength=4,
            ax=ax,
            label=f"Completed Pass ({int(pass_success)})",
            zorder=4,
        )

    # Generate Start (x1, y1) & End (x2, y2) coordinates for Incomplete Passes
    f_cnt = min(int(pass_failed), 12)
    if f_cnt > 0:
        fx1 = np.random.uniform(zone["x"][0], zone["x"][1], f_cnt)
        fy1 = np.random.uniform(zone["y"][0], zone["y"][1], f_cnt)
        fx2 = np.clip(fx1 + np.random.uniform(10, 25, f_cnt), 5, 115)
        fy2 = np.clip(fy1 + np.random.uniform(-20, 20, f_cnt), 5, 75)

        pitch.arrows(
            fx1,
            fy1,
            fx2,
            fy2,
            color="#ff1744",
            width=2,
            headwidth=4,
            headlength=4,
            ax=ax,
            label=f"Incomplete Pass ({int(pass_failed)})",
            zorder=3,
        )

    ax.legend(
        facecolor="#1e1e1e",
        edgecolor="#ffffff",
        fontsize=10,
        labelcolor="white",
        loc="upper left",
    )
    st.pyplot(fig)

# ---------------------------------------------------------
# MODE 2: HEATMAP
# ---------------------------------------------------------
elif view_mode == "Heatmap (Density)":
    st.subheader(f"🔥 Position Heatmap: {p_data['Full Name']} ({pos})")

    total_actions = int(
        p_data.get("Pass Total", 0)
        + p_data.get("Dribble Total", 0)
        + p_data.get("BallWon Total", 0)
    )
    sample_size = max(min(total_actions, 150), 40)

    hx = np.clip(
        np.random.normal(
            loc=(zone["x"][0] + zone["x"][1]) / 2, scale=12, size=sample_size
        ),
        2,
        118,
    )
    hy = np.clip(
        np.random.normal(
            loc=(zone["y"][0] + zone["y"][1]) / 2, scale=10, size=sample_size
        ),
        2,
        78,
    )

    sns.kdeplot(
        x=hx,
        y=hy,
        ax=ax,
        fill=True,
        thresh=0.05,
        levels=15,
        cmap="YlOrRd",
        alpha=0.6,
        zorder=2,
    )
    pitch.scatter(
        hx,
        hy,
        s=15,
        color="white",
        alpha=0.3,
        ax=ax,
        zorder=3,
        label="Touch Points",
    )

    ax.legend(
        facecolor="#1e1e1e",
        edgecolor="#ffffff",
        fontsize=10,
        labelcolor="white",
        loc="upper left",
    )
    st.pyplot(fig)

# ---------------------------------------------------------
# MODE 3: FULL ACTION MAP
# ---------------------------------------------------------
else:
    st.subheader(
        f"⚽ Action Map (Crosses, Shots & Recovery): {p_data['Full Name']}"
    )

    # 1. Successful Crosses
    cross_cnt = p_data.get("Cross Success", 0)
    if cross_cnt > 0:
        cx = np.random.uniform(
            max(zone["x"][0], 50), 105, min(int(cross_cnt), 15)
        )
        cy = np.random.uniform(5, 25, len(cx))
        pitch.scatter(
            cx,
            cy,
            s=170,
            color="#d500f9",
            marker="^",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Completed Crosses ({int(cross_cnt)})",
            zorder=4,
        )

    # 2. Key Passes
    key_passes = p_data.get("Chances KeyPasses", 0) + p_data.get(
        "Chances Assists", 0
    )
    if key_passes > 0:
        kx = np.random.uniform(
            zone["x"][0], min(zone["x"][1] + 10, 110), min(int(key_passes), 15)
        )
        ky = np.random.uniform(zone["y"][0], zone["y"][1], len(kx))
        pitch.scatter(
            kx,
            ky,
            s=200,
            color="#ffab00",
            marker="P",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Key Passes / Assists ({int(key_passes)})",
            zorder=5,
        )

    # 3. Goals
    goals_cnt = p_data.get("GoalsScored Total", 0)
    if goals_cnt > 0:
        gx = np.random.uniform(
            max(zone["x"][0], 88), 116, min(int(goals_cnt), 10)
        )
        gy = np.random.uniform(25, 55, len(gx))
        pitch.scatter(
            gx,
            gy,
            s=260,
            color="#ff1744",
            marker="*",
            edgecolors="#ffff00",
            linewidth=1.5,
            ax=ax,
            label=f"Goals ({int(goals_cnt)})",
            zorder=6,
        )

    ax.legend(
        facecolor="#1e1e1e",
        edgecolor="#ffffff",
        fontsize=10,
        labelcolor="white",
        loc="upper left",
    )
    st.pyplot(fig)

# ---------------------------------------------------------
# 4. Passing Breakdown Grid
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 Passing & Crossing Precision Breakdown")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### 🟢 Completed Passes")
    st.write(f"**Successful Passes:** {int(p_data.get('Pass Success', 0))}")
    st.write(f"**Pass Accuracy:** {p_data.get('Pass Accuracy', 0)*100:.1f}%")

with col2:
    st.markdown("### 🔴 Incomplete Passes")
    failed_p = max(
        0,
        int(p_data.get("Pass Total", 0)) - int(p_data.get("Pass Success", 0)),
    )
    st.write(f"**Failed Passes:** {failed_p}")
    st.write(f"**Total Attempted:** {int(p_data.get('Pass Total', 0))}")

with col3:
    st.markdown("### ↗️ Crosses")
    st.write(f"**Successful Crosses:** {int(p_data.get('Cross Success', 0))}")
    st.write(
        f"**Cross Accuracy:** {p_data.get('Cross Accuracy', 0)*100:.1f}%"
    )

with col4:
    st.markdown("### 🎯 Key Opportunities")
    st.write(f"**Assists:** {int(p_data.get('Chances Assists', 0))}")
    st.write(f"**Key Passes:** {int(p_data.get('Chances KeyPasses', 0))}")
