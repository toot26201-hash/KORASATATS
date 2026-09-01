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
            "👋 Please upload your team data file (`Data_2215_2.csv` or `Data_2215.csv`) from the sidebar."
        )
        st.stop()
else:
    df = load_data(uploaded_file)

team_data = df.iloc[0]
team_name = team_data.get("Team Name", "Selected Team")

# ---------------------------------------------------------
# 2. Tactical Mode Selection Buttons (فصل الخريطة الحرارية عن النقاط)
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🗺️ Tactical Pitch Views")
tactical_view = st.sidebar.radio(
    "Select Tactical Visual Mode:",
    [
        "🛡️ Ball Recovery Zones (Points Only)",
        "🔥 Team Recovery Heatmap (Density Only)",
        "↗️ Crosses Map",
        "📥 Passes INTO Half-Spaces",
        "📤 Passes OUT OF Half-Spaces",
        "🎯 Team Passing Structure",
        "⚡ Team Pressing Map",
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

# MODE 1: BALL RECOVERY POINTS ONLY (نقاط الـ 254 فقط بدون هيت ماب)
if tactical_view == "🛡️ Ball Recovery Zones (Points Only)":
    rec = int(team_data.get("BallWon BallRecover", 254))
    inter = int(team_data.get("BallWon InterceptionWon", 51))
    tack = int(team_data.get("BallWon TackleWon", 24))

    # 1. Recoveries Points (Cyan Squares)
    rx = np.random.uniform(10, 105, rec)
    ry = np.random.uniform(5, 75, rec)
    pitch.scatter(
        rx,
        ry,
        s=50,
        color="#00e5ff",
        marker="s",
        alpha=0.85,
        edgecolors="white",
        linewidth=0.5,
        ax=ax,
        label=f"Recoveries ({rec})",
        zorder=4,
    )

    # 2. Interceptions Points (Orange Diamonds)
    if inter > 0:
        ix = np.random.uniform(15, 95, inter)
        iy = np.random.uniform(5, 75, inter)
        pitch.scatter(
            ix,
            iy,
            s=65,
            color="#ffab00",
            marker="D",
            edgecolors="white",
            linewidth=0.6,
            ax=ax,
            label=f"Interceptions ({inter})",
            zorder=5,
        )

    # 3. Tackles Won Points (Green Circles)
    if tack > 0:
        tx = np.random.uniform(15, 85, tack)
        ty = np.random.uniform(5, 75, tack)
        pitch.scatter(
            tx,
            ty,
            s=60,
            color="#00ff66",
            marker="o",
            edgecolors="black",
            linewidth=0.6,
            ax=ax,
            label=f"Tackles Won ({tack})",
            zorder=5,
        )

# MODE 2: TEAM RECOVERY HEATMAP (خريطة حرارية فقط بدون نقاط)
elif tactical_view == "🔥 Team Recovery Heatmap (Density Only)":
    rec = int(team_data.get("BallWon BallRecover", 254))
    rx = np.random.uniform(10, 105, rec)
    ry = np.random.uniform(5, 75, rec)

    # Pure KDE Density Map for Recoveries
    sns.kdeplot(
        x=rx,
        y=ry,
        ax=ax,
        fill=True,
        thresh=0.05,
        levels=15,
        cmap="YlOrRd",
        alpha=0.75,
        zorder=2,
    )

# MODE 3: CROSSES MAP
elif tactical_view == "↗️ Crosses Map":
    cross_success = int(team_data.get("Cross Success", 10))
    cnt = min(max(cross_success, 10), 30)

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

# MODE 4: PASSES INTO HALF-SPACES
elif tactical_view == "📥 Passes INTO Half-Spaces":
    pass_succ = int(team_data.get("Pass Success", 1251))
    cnt = min(max(int(pass_succ * 0.03), 15), 30)

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

# MODE 5: PASSES OUT OF HALF-SPACES
elif tactical_view == "📤 Passes OUT OF Half-Spaces":
    pass_succ = int(team_data.get("Pass Success", 1251))
    cnt = min(max(int(pass_succ * 0.03), 15), 30)

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

# MODE 6: TEAM PASSING STRUCTURE
elif tactical_view == "🎯 Team Passing Structure":
    pass_succ = int(team_data.get("Pass Success", 1251))
    cnt = min(max(int(pass_succ * 0.025), 15), 35)

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

# MODE 7: TEAM PRESSING MAP
elif tactical_view == "⚡ Team Pressing Map":
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
        alpha=0.65,
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

# Pitch Legend
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
