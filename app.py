import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

# Page Configuration
st.set_page_config(
    page_title="Single-Pitch All Events Action Map", layout="wide"
)

st.title("⚽ Complete Single-Pitch Action Map (All Events Combined)")

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
        "👋 Please upload your data file (`PlayersData_2215.csv`) from the sidebar to display the single-pitch action map."
    )
    st.stop()

df = load_data(uploaded_file)

# ---------------------------------------------------------
# 2. Player Selection & Event Sidebar Toggles
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
st.sidebar.header("🎨 Toggle Visible Events")

show_passes = st.sidebar.checkbox("🎯 Passes (Green / Red Arrows)", value=True)
show_goals = st.sidebar.checkbox("⚽ Goals (Gold Star)", value=True)
show_assists = st.sidebar.checkbox(
    "🔑 Key Passes & Assists (Orange Plus)", value=True
)
show_crosses = st.sidebar.checkbox(
    "↗️ Successful Crosses (Purple Triangle)", value=True
)
show_dribbles = st.sidebar.checkbox(
    "⚡ Successful Dribbles (Yellow Circle)", value=True
)
show_ball_won = st.sidebar.checkbox(
    "🛡️ Recoveries & Tackles (Cyan Square)", value=True
)
show_clearances = st.sidebar.checkbox(
    "🧱 Clearances & Blocks (Gray Diamond)", value=True
)
show_fouls = st.sidebar.checkbox(
    "⚠️ Fouls & Cards (Red / Yellow Hexagons)", value=True
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
# 4. Single Pitch All Events Visualization
# ---------------------------------------------------------
st.subheader(
    f"📊 All Match Actions on Single Pitch: {p_data['Full Name']} ({pos})"
)

pitch = Pitch(half=False)
fig, ax = pitch.draw(figsize=(13, 9))

# A. Pass Vectors (Completed vs Incomplete Arrows)
if show_passes:
    pass_success = p_data.get("Pass Success", 0)
    pass_total = p_data.get("Pass Total", 0)
    pass_failed = max(0, pass_total - pass_success)

    # Successful Passes (Green Arrows)
    s_cnt = min(int(pass_success), 20)
    if s_cnt > 0:
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
            label=f"Completed Pass ({int(pass_success)})",
            zorder=3,
        )

    # Incomplete Passes (Red Arrows)
    f_cnt = min(int(pass_failed), 10)
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
            color="#da3633",
            width=2,
            headwidth=4,
            headlength=4,
            ax=ax,
            label=f"Incomplete Pass ({int(pass_failed)})",
            zorder=3,
        )

# B. Successful Crosses (Purple Triangles)
if show_crosses:
    cross_cnt = p_data.get("Cross Success", 0)
    if cross_cnt > 0:
        cx = np.random.uniform(
            max(zone["x"][0], 50), 105, min(int(cross_cnt), 12)
        )
        cy = np.random.uniform(5, 25, len(cx))
        pitch.scatter(
            cx,
            cy,
            s=160,
            color="#8a2be2",
            marker="^",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Completed Cross ({int(cross_cnt)})",
            zorder=4,
        )

# C. Key Passes & Assists (Orange Plus)
if show_assists:
    key_passes = p_data.get("Chances KeyPasses", 0) + p_data.get(
        "Chances Assists", 0
    )
    if key_passes > 0:
        kx = np.random.uniform(
            zone["x"][0], min(zone["x"][1] + 10, 110), min(int(key_passes), 12)
        )
        ky = np.random.uniform(zone["y"][0], zone["y"][1], len(kx))
        pitch.scatter(
            kx,
            ky,
            s=200,
            color="#ff8c00",
            marker="P",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Key Pass / Assist ({int(key_passes)})",
            zorder=5,
        )

# D. Successful Dribbles (Yellow Circles)
if show_dribbles:
    dribbles_cnt = p_data.get("Dribble Success", 0)
    if dribbles_cnt > 0:
        dx = np.random.uniform(
            zone["x"][0], zone["x"][1], min(int(dribbles_cnt), 12)
        )
        dy = np.random.uniform(zone["y"][0], zone["y"][1], len(dx))
        pitch.scatter(
            dx,
            dy,
            s=140,
            color="#ffeb3b",
            marker="o",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Successful Dribble ({int(dribbles_cnt)})",
            zorder=4,
        )

# E. Ball Recoveries & Tackles (Cyan Squares)
if show_ball_won:
    tackles_cnt = p_data.get("BallWon Total", 0)
    if tackles_cnt > 0:
        bx = np.random.uniform(
            max(zone["x"][0] - 15, 5), zone["x"][1], min(int(tackles_cnt), 12)
        )
        by = np.random.uniform(zone["y"][0], zone["y"][1], len(bx))
        pitch.scatter(
            bx,
            by,
            s=150,
            color="#00bcd4",
            marker="s",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Ball Recovery ({int(tackles_cnt)})",
            zorder=4,
        )

# F. Clearances & Blocks (Gray Diamonds)
if show_clearances:
    def_cnt = p_data.get("Defensive Clear", 0) + p_data.get(
        "Defensive Blocks", 0
    )
    if def_cnt > 0:
        cl_x = np.random.uniform(
            max(zone["x"][0] - 20, 5), zone["x"][1], min(int(def_cnt), 10)
        )
        cl_y = np.random.uniform(15, 65, len(cl_x))
        pitch.scatter(
            cl_x,
            cl_y,
            s=160,
            color="#78909c",
            marker="D",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Clearance / Block ({int(def_cnt)})",
            zorder=4,
        )

# G. Fouls Committed (Red Hexagons)
if show_fouls:
    fouls_cnt = p_data.get("Fouls Committed", 0)
    if fouls_cnt > 0:
        fx = np.random.uniform(
            zone["x"][0], zone["x"][1], min(int(fouls_cnt), 8)
        )
        fy = np.random.uniform(zone["y"][0], zone["y"][1], len(fx))
        pitch.scatter(
            fx,
            fy,
            s=170,
            color="#e65100",
            marker="h",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Foul Committed ({int(fouls_cnt)})",
            zorder=4,
        )

# H. Goals Scored (Gold Star)
if show_goals:
    goals_cnt = p_data.get("GoalsScored Total", 0)
    if goals_cnt > 0:
        gx = np.random.uniform(
            max(zone["x"][0], 88), 116, min(int(goals_cnt), 10)
        )
        gy = np.random.uniform(25, 55, len(gx))
        pitch.scatter(
            gx,
            gy,
            s=300,
            color="#ffd700",
            marker="*",
            edgecolors="black",
            linewidth=1.5,
            ax=ax,
            label=f"Goal Scored ({int(goals_cnt)})",
            zorder=6,
        )

# Display Complete Legend
ax.legend(
    facecolor="#ffffff",
    edgecolor="#000000",
    fontsize=10,
    labelcolor="black",
    loc="upper left",
)
st.pyplot(fig)

# ---------------------------------------------------------
# 5. Full Match Actions Data Breakdown
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 Match Actions Quantitative Breakdown")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### ⚽ Goals & Passing")
    st.write(f"**Goals:** {int(p_data.get('GoalsScored Total', 0))}")
    st.write(f"**Passes Completed:** {int(p_data.get('Pass Success', 0))}")
    st.write(
        f"**Failed Passes:** {max(0, int(p_data.get('Pass Total', 0)) - int(p_data.get('Pass Success', 0)))}"
    )

with col2:
    st.markdown("### 🎯 Creation & Dribbles")
    st.write(
        f"**Key Passes / Assists:** {int(p_data.get('Chances KeyPasses', 0) + p_data.get('Chances Assists', 0))}"
    )
    st.write(
        f"**Crosses Completed:** {int(p_data.get('Cross Success', 0))}"
    )
    st.write(
        f"**Dribbles Won:** {int(p_data.get('Dribble Success', 0))}"
    )

with col3:
    st.markdown("### 🛡️ Defensive Work")
    st.write(f"**Ball Recoveries:** {int(p_data.get('BallWon Total', 0))}")
    st.write(
        f"**Clearances:** {int(p_data.get('Defensive Clear', 0))}"
    )
    st.write(f"**Blocks:** {int(p_data.get('Defensive Blocks', 0))}")

with col4:
    st.markdown("### ⚠️ Discipline & Cards")
    st.write(
        f"**Fouls Committed:** {int(p_data.get('Fouls Committed', 0))}"
    )
    st.write(f"**Yellow Cards:** {int(p_data.get('Cards Yellow', 0))}")
    st.write(f"**Red Cards:** {int(p_data.get('Cards Red', 0))}")
