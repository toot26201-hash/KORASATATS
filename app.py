import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from mplsoccer import Pitch

# Page Configuration
st.set_page_config(
    page_title="Player Performance & Heatmap Analytics", layout="wide"
)

st.title("⚽ Advanced Pitch Analytics & Heatmap Visualization")

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
        "👋 Please upload your data file (`PlayersData_2215.csv`) from the sidebar to view pitch actions and heatmaps."
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
    ["Action Map (Markers)", "Heatmap (Density)"],
)

# ---------------------------------------------------------
# 3. Position Pitch Mapping
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


def generate_coords(count, x_range, y_range, max_display=35):
    if count <= 0 or pd.isna(count):
        return np.array([]), np.array([])
    display_count = min(int(count), max_display)
    xs = np.random.uniform(x_range[0], x_range[1], display_count)
    ys = np.random.uniform(y_range[0], y_range[1], display_count)
    return xs, ys


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
# MODE 1: HEATMAP
# ---------------------------------------------------------
if view_mode == "Heatmap (Density)":
    st.subheader(f"🔥 Position Heatmap: {p_data['Full Name']} ({pos})")

    # Generate synthetic activity cloud around player's operational field zone
    total_actions = int(
        p_data.get("Pass Total", 0)
        + p_data.get("Dribble Total", 0)
        + p_data.get("BallWon Total", 0)
    )
    sample_size = max(min(total_actions, 150), 40)

    hx = np.random.normal(
        loc=(zone["x"][0] + zone["x"][1]) / 2, scale=12, size=sample_size
    )
    hy = np.random.normal(
        loc=(zone["y"][0] + zone["y"][1]) / 2, scale=10, size=sample_size
    )

    # Clip coordinates to pitch dimensions
    hx = np.clip(hx, 2, 118)
    hy = np.clip(hy, 2, 78)

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
# MODE 2: ACTION MARKERS MAP
# ---------------------------------------------------------
else:
    st.subheader(
        f"⚽ Action Map (Passes, Crosses & Shots): {p_data['Full Name']}"
    )

    # 1. Successful Passes (Short / Long)
    short_pass = p_data.get("ShortPass Success", 0)
    long_pass = p_data.get("LongPass Success", 0)
    px, py = generate_coords(short_pass + long_pass, zone["x"], zone["y"], 30)
    if len(px) > 0:
        pitch.scatter(
            px,
            py,
            s=120,
            color="#00e676",
            marker="o",
            edgecolors="black",
            linewidth=0.8,
            ax=ax,
            label=f"Completed Passes ({int(short_pass + long_pass)})",
            zorder=3,
        )

    # 2. Successful Crosses
    cross_cnt = p_data.get("Cross Success", 0)
    side_y = (5, 25) if random.random() > 0.5 else (55, 75)
    cx, cy = generate_coords(cross_cnt, (max(zone["x"][0], 50), 105), side_y, 20)
    if len(cx) > 0:
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

    # 3. Key Passes & Assists
    key_passes = p_data.get("Chances KeyPasses", 0) + p_data.get(
        "Chances Assists", 0
    )
    k_x, k_y = generate_coords(
        key_passes, (zone["x"][0], min(zone["x"][1] + 10, 110)), zone["y"], 15
    )
    if len(k_x) > 0:
        pitch.scatter(
            k_x,
            k_y,
            s=200,
            color="#ffab00",
            marker="P",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Key Passes / Assists ({int(key_passes)})",
            zorder=5,
        )

    # 4. Ball Recoveries
    tackles_cnt = p_data.get("BallWon Total", 0)
    bx, by = generate_coords(
        tackles_cnt,
        (max(zone["x"][0] - 15, 5), zone["x"][1]),
        zone["y"],
        20,
    )
    if len(bx) > 0:
        pitch.scatter(
            bx,
            by,
            s=140,
            color="#00b0ff",
            marker="s",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Ball Recoveries ({int(tackles_cnt)})",
            zorder=3,
        )

    # 5. Goals
    goals_cnt = p_data.get("GoalsScored Total", 0)
    gx, gy = generate_coords(
        goals_cnt, (max(zone["x"][0], 88), 116), (25, 55), 10
    )
    if len(gx) > 0:
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
# 4. Detailed Passing & Crossing Statistics Grid
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 Complete Passing & Crossing Breakdown")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### ⚽ Passes Overview")
    st.write(f"**Total Passes:** {int(p_data.get('Pass Total', 0))}")
    st.write(f"**Passes Completed:** {int(p_data.get('Pass Success', 0))}")
    st.write(f"**Pass Accuracy:** {p_data.get('Pass Accuracy', 0)*100:.1f}%")

with col2:
    st.markdown("### 📐 Short vs Long Passes")
    st.write(
        f"**Short Pass Completed:** {int(p_data.get('ShortPass Success', 0))} / {int(p_data.get('ShortPass Total', 0))}"
    )
    st.write(
        f"**Short Pass Accuracy:** {p_data.get('ShortPass Accuracy', 0)*100:.1f}%"
    )
    st.write(
        f"**Long Pass Completed:** {int(p_data.get('LongPass Success', 0))} / {int(p_data.get('LongPass Total', 0))}"
    )
    st.write(
        f"**Long Pass Accuracy:** {p_data.get('LongPass Accuracy', 0)*100:.1f}%"
    )

with col3:
    st.markdown("### ↗️ Crosses Analytics")
    st.write(
        f"**Total Crosses:** {int(p_data.get('Cross Total', 0))}"
    )
    st.write(
        f"**Crosses Completed:** {int(p_data.get('Cross Success', 0))}"
    )
    st.write(
        f"**Cross Accuracy:** {p_data.get('Cross Accuracy', 0)*100:.1f}%"
    )

with col4:
    st.markdown("### 🎯 Play Types & Key Passes")
    st.write(
        f"**Open Play Crosses:** {int(p_data.get('OpenPlayCross Success', 0))}"
    )
    st.write(
        f"**Set Piece Crosses:** {int(p_data.get('SetPieceCross Success', 0))}"
    )
    st.write(f"**Key Passes Created:** {int(p_data.get('Chances KeyPasses', 0))}")
