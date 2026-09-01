import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

# Page Configuration
st.set_page_config(
    page_title="Player Action Maps | Match Analytics", layout="wide"
)

st.title("⚽ Football Player Action Map & Pitch Analytics")

# ---------------------------------------------------------
# 1. File Upload Section
# ---------------------------------------------------------
st.sidebar.header("📁 Data Upload")
uploaded_file = st.sidebar.file_uploader(
    "Upload Players CSV File:", type=["csv"]
)


@st.cache_data
def load_data(file):
    return pd.read_csv(file)


if uploaded_file is None:
    st.info(
        "👋 Please upload your data file (`PlayersData_2215.csv`) from the sidebar to start displaying action maps."
    )
    st.stop()

df = load_data(uploaded_file)

# ---------------------------------------------------------
# 2. Player Selection & Filters
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
st.sidebar.header("🎨 Action Filters")

# Toggle individual actions on the pitch
show_goals = st.sidebar.checkbox("⚽ Goals", value=True)
show_assists = st.sidebar.checkbox("🔑 Key Passes / Assists", value=True)
show_dribbles = st.sidebar.checkbox("⚡ Successful Dribbles", value=True)
show_ball_won = st.sidebar.checkbox("🛡️ Ball Recoveries / Tackles", value=True)
show_crosses = st.sidebar.checkbox("↗️ Successful Crosses", value=True)

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


def generate_coords(count, x_range, y_range):
    if count <= 0 or pd.isna(count):
        return [], []
    display_count = min(int(count), 30)
    xs = np.random.uniform(x_range[0], x_range[1], display_count)
    ys = np.random.uniform(y_range[0], y_range[1], display_count)
    return xs, ys


# Pitch Visual Setup
pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="#121e17",
    line_color="#ffffff",
    stripe=True,
    stripe_color="#19281f",
)
fig, ax = pitch.draw(figsize=(12, 8))

# 1. Goals
if show_goals:
    goals_cnt = p_data.get("GoalsScored Total", 0)
    gx, gy = generate_coords(
        goals_cnt, (max(zone["x"][0], 88), 116), (25, 55)
    )
    if len(gx) > 0:
        pitch.scatter(
            gx,
            gy,
            s=250,
            color="#ff3333",
            marker="*",
            edgecolors="#ffff00",
            linewidth=1.5,
            ax=ax,
            label=f"Goal ({int(goals_cnt)})",
            zorder=5,
        )

# 2. Key Passes / Assists
if show_assists:
    key_passes = p_data.get("Chances KeyPasses", 0) + p_data.get(
        "Chances Assists", 0
    )
    ax_x, ax_y = generate_coords(
        key_passes, (zone["x"][0], min(zone["x"][1] + 10, 110)), zone["y"]
    )
    if len(ax_x) > 0:
        pitch.scatter(
            ax_x,
            ax_y,
            s=180,
            color="#00ff66",
            marker="P",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Key Pass / Assist ({int(key_passes)})",
            zorder=4,
        )

# 3. Successful Dribbles
if show_dribbles:
    dribbles_cnt = p_data.get("Dribble Success", 0)
    dx, dy = generate_coords(dribbles_cnt, zone["x"], zone["y"])
    if len(dx) > 0:
        pitch.scatter(
            dx,
            dy,
            s=150,
            color="#ffcc00",
            marker="o",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Successful Dribble ({int(dribbles_cnt)})",
            zorder=3,
        )

# 4. Ball Recoveries / Tackles
if show_ball_won:
    tackles_cnt = p_data.get("BallWon Total", 0)
    bx, by = generate_coords(
        tackles_cnt, (max(zone["x"][0] - 15, 5), zone["x"][1]), zone["y"]
    )
    if len(bx) > 0:
        pitch.scatter(
            bx,
            by,
            s=160,
            color="#00ccff",
            marker="s",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Ball Recovery ({int(tackles_cnt)})",
            zorder=3,
        )

# 5. Successful Crosses
if show_crosses:
    cross_cnt = p_data.get("Cross Success", 0)
    side_y = (5, 25) if random.random() > 0.5 else (55, 75)
    cx, cy = generate_coords(
        cross_cnt, (max(zone["x"][0], 50), 105), side_y
    )
    if len(cx) > 0:
        pitch.scatter(
            cx,
            cy,
            s=170,
            color="#cc66ff",
            marker="^",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Successful Cross ({int(cross_cnt)})",
            zorder=4,
        )

# Pitch Legend
ax.legend(
    facecolor="#1e1e1e",
    edgecolor="#ffffff",
    fontsize=11,
    labelcolor="white",
    loc="upper left",
)

st.pyplot(fig)

# ---------------------------------------------------------
# 4. Performance Summary Cards
# ---------------------------------------------------------
st.markdown("---")
st.subheader(f"📊 Action Metrics Summary: {p_data['Full Name']}")

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("⚽ Goals", int(p_data.get("GoalsScored Total", 0)))
c2.metric("🔑 Key Passes", int(p_data.get("Chances KeyPasses", 0)))
c3.metric("⚡ Dribbles Won", int(p_data.get("Dribble Success", 0)))
c4.metric("🛡️ Ball Recoveries", int(p_data.get("BallWon Total", 0)))
c5.metric("↗️ Crosses Completed", int(p_data.get("Cross Success", 0)))
