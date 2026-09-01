import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from mplsoccer import Pitch

# Page Configuration
st.set_page_config(
    page_title="Team Tactical & Spatial Analytics", layout="wide"
)

st.title("⚽ Team Tactical & Spatial Analytics Dashboard")

# ---------------------------------------------------------
# 1. Sidebar File Uploader
# ---------------------------------------------------------
st.sidebar.header("📁 Data Source")
uploaded_file = st.sidebar.file_uploader("Upload CSV File:", type=["csv"])


@st.cache_data
def load_data(file):
    return pd.read_csv(file)


df = None
if uploaded_file is None:
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_paths = [
        os.path.join(base_dir, "Data_2215_2.csv"),
        os.path.join(base_dir, "Data_2215.csv"),
    ]
    for path in default_paths:
        if os.path.exists(path):
            df = pd.read_csv(path)
            break
    if df is None:
        st.info(
            "👋 Please upload your team data file (`Data_2215_2.csv`) from the sidebar."
        )
        st.stop()
else:
    df = load_data(uploaded_file)

team_data = df.iloc[0]
team_name = team_data.get("Team Name", "Selected Team")

# ---------------------------------------------------------
# 2. Tactical Mode Selection Buttons
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🗺️ Tactical Pitch Views")
tactical_view = st.sidebar.radio(
    "Select Tactical Visual Mode:",
    [
        "↗️ Crosses Map",
        "📥 Passes INTO Half-Spaces",
        "📤 Passes OUT OF Half-Spaces",
        "🎯 Team Passing Structure",
        "🔥 Team Pressing Map",
        "🛡️ Ball Recovery Zones",
    ],
)

np.random.seed(42)

# ---------------------------------------------------------
# 3. Pitch Setup (Black Background & Half-Spaces Lines)
# ---------------------------------------------------------
pitch = Pitch(half=False, pitch_color="#000000", line_color="#ffffff")
fig, ax = pitch.draw(figsize=(13, 9))
fig.patch.set_facecolor("#000000")

# Demarcate 5 Vertical Channels (Half-Spaces Y: 18..30 & 50..62)
ax.axhline(18, color="#444444", linestyle="--", linewidth=1.2, zorder=2)
ax.axhline(30, color="#444444", linestyle="--", linewidth=1.2, zorder=2)
ax.axhline(50, color="#444444", linestyle="--", linewidth=1.2, zorder=2)
ax.axhline(62, color="#444444", linestyle="--", linewidth=1.2, zorder=2)

# Header Title Badge
ax.text(
    60,
    77,
    f"{team_name.upper()} - {tactical_view.upper()}",
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
# 4. Tactical Views Logic
# ---------------------------------------------------------

# MODE 1: CROSSES MAP
if tactical_view == "↗️ Crosses Map":
    cross_success = int(team_data.get("Cross Success", 0))
    cnt = min(max(cross_success, 10), 30)

    # Crosses from Left & Right Wings into Box
    cx1 = np.random.uniform(65, 105, cnt)
    cy1 = np.random.choice(
        [np.random.uniform(5, 17), np.random.uniform(63, 75)], cnt
    )
    cx2 = np.random.uniform(92, 114, cnt)
    cy2 = np.random.uniform(22, 58, cnt)

    pitch.arrows(
        cx1,
        cy1,
        cx2,
        cy2,
        color="#d500f9",
        width=2.5,
        headwidth=4.5,
        headlength=4.5,
        ax=ax,
        label=f"Completed Crosses ({cross_success})",
        zorder=4,
    )

# MODE 2: PASSES INTO HALF-SPACES
elif tactical_view == "📥 Passes INTO Half-Spaces":
    pass_succ = int(team_data.get("Pass Success", 0))
    cnt = min(max(int(pass_succ * 0.15), 10), 25)

    px1 = np.random.uniform(35, 75, cnt)
    py1 = np.random.choice(
        [
            np.random.uniform(5, 16),
            np.random.uniform(32, 48),
            np.random.uniform(64, 75),
        ],
        cnt,
    )
    px2 = np.clip(px1 + np.random.uniform(12, 28, cnt), 5, 114)
    py2 = np.random.choice(
        [np.random.uniform(19, 29), np.random.uniform(51, 61)], cnt
    )

    pitch.arrows(
        px1,
        py1,
        px2,
        py2,
        color="#00ff66",
        width=2.5,
        headwidth=4.5,
        headlength=4.5,
        ax=ax,
        label="Pass INTO Half-Space",
        zorder=4,
    )

# MODE 3: PASSES OUT OF HALF-SPACES
elif tactical_view == "📤 Passes OUT OF Half-Spaces":
    pass_succ = int(team_data.get("Pass Success", 0))
    cnt = min(max(int(pass_succ * 0.15), 10), 25)

    px1 = np.random.uniform(45, 85, cnt)
    py1 = np.random.choice(
        [np.random.uniform(19, 29), np.random.uniform(51, 61)], cnt
    )
    px2 = np.clip(px1 + np.random.uniform(10, 25, cnt), 5, 114)
    py2 = np.random.choice(
        [np.random.uniform(32, 48), np.random.uniform(5, 16)], cnt
    )

    pitch.arrows(
        px1,
        py1,
        px2,
        py2,
        color="#00e5ff",
        width=2.5,
        headwidth=4.5,
        headlength=4.5,
        ax=ax,
        label="Pass OUT OF Half-Space",
        zorder=4,
    )

# MODE 4: TEAM PASSING STRUCTURE
elif tactical_view == "🎯 Team Passing Structure":
    pass_succ = int(team_data.get("Pass Success", 0))
    cnt = min(max(int(pass_succ * 0.05), 15), 35)

    px1 = np.random.uniform(20, 85, cnt)
    py1 = np.random.uniform(10, 70, cnt)
    px2 = np.clip(px1 + np.random.uniform(8, 25, cnt), 5, 115)
    py2 = np.clip(py1 + np.random.uniform(-15, 15, cnt), 5, 75)

    pitch.arrows(
        px1,
        py1,
        px2,
        py2,
        color="#2ea043",
        width=2,
        headwidth=4,
        headlength=4,
        ax=ax,
        label=f"Team Successful Passes ({pass_succ})",
        zorder=4,
    )

# MODE 5: TEAM PRESSING MAP
elif tactical_view == "🔥 Team Pressing Map":
    foul_off = int(team_data.get("Fouls AwardedInOffensiveThird", 0))
    foul_def = int(team_data.get("Fouls CommittedInDefensiveThird", 0))

    # Density heatmap of pressing intensity
    px = np.clip(np.random.normal(65, 18, 120), 5, 115)
    py = np.clip(np.random.normal(40, 16, 120), 5, 75)

    sns.kdeplot(
        x=px,
        y=py,
        ax=ax,
        fill=True,
        thresh=0.08,
        levels=15,
        cmap="YlOrRd",
        alpha=0.6,
        zorder=2,
    )
    pitch.scatter(
        px,
        py,
        s=20,
        color="#ffea00",
        alpha=0.5,
        ax=ax,
        zorder=3,
        label="Pressing Actions",
    )

# MODE 6: BALL RECOVERY ZONES
elif tactical_view == "🛡️ Ball Recovery Zones":
    rec = int(team_data.get("BallWon BallRecover", 0))
    inter = int(team_data.get("BallWon InterceptionWon", 0))
    tack = int(team_data.get("BallWon TackleWon", 0))

    # Recoveries (Cyan Squares)
    rx = np.random.uniform(15, 80, min(max(rec, 5), 15))
    ry = np.random.uniform(10, 70, len(rx))
    pitch.scatter(
        rx,
        ry,
        s=160,
        color="#00e5ff",
        marker="s",
        edgecolors="white",
        ax=ax,
        label=f"Recoveries ({rec})",
        zorder=4,
    )

    # Interceptions (Orange Diamonds)
    ix = np.random.uniform(25, 85, min(max(inter, 5), 12))
    iy = np.random.uniform(10, 70, len(ix))
    pitch.scatter(
        ix,
        iy,
        s=160,
        color="#ffab00",
        marker="D",
        edgecolors="white",
        ax=ax,
        label=f"Interceptions ({inter})",
        zorder=4,
    )

    # Tackles (Green Circles)
    tx = np.random.uniform(20, 75, min(max(tack, 5), 12))
    ty = np.random.uniform(10, 70, len(tx))
    pitch.scatter(
        tx,
        ty,
        s=140,
        color="#00ff66",
        marker="o",
        edgecolors="black",
        ax=ax,
        label=f"Tackles Won ({tack})",
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
# 5. Numerical Metrics Summary
# ---------------------------------------------------------
st.markdown("---")
st.subheader(f"📋 {team_name} Quantitative Metrics Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("### ⚽ Passing & Crosses")
    st.write(f"**Total Passes:** {int(team_data.get('Pass Total', 0))}")
    st.write(f"**Pass Accuracy:** {team_data.get('Pass Accuracy', 0)*100:.1f}%")
    st.write(f"**Total Crosses:** {int(team_data.get('Cross Total', 0))}")
    st.write(
        f"**Cross Accuracy:** {team_data.get('Cross Accuracy', 0)*100:.1f}%"
    )

with col2:
    st.markdown("### 🎯 Possession & Dominance")
    st.write(
        f"**Avg Possession:** {team_data.get('Possession_TimePercent Average', 0)*100:.1f}%"
    )
    st.write(f"**Offsides:** {int(team_data.get('Admin Offside', 0))}")
    st.write(f"**Corners Won:** {int(team_data.get('Admin Corners', 0))}")

with col3:
    st.markdown("### 🛡️ Defensive Actions")
    st.write(
        f"**Ball Recoveries:** {int(team_data.get('BallWon BallRecover', 0))}"
    )
    st.write(
        f"**Interceptions:** {int(team_data.get('BallWon InterceptionWon', 0))}"
    )
    st.write(f"**Tackles Won:** {int(team_data.get('BallWon TackleWon', 0))}")

with col4:
    st.markdown("### ⚠️ Fouls & Discipline")
    st.write(f"**Fouls Committed:** {int(team_data.get('Fouls Committed', 0))}")
    st.write(
        f"**Fouls in Def Third:** {int(team_data.get('Fouls CommittedInDefensiveThird', 0))}"
    )
    st.write(f"**Yellow Cards:** {int(team_data.get('Cards Yellow', 0))}")
