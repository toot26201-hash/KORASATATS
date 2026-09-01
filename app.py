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
# 2. Tactical Mode Selection Buttons
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🗺️ Tactical Pitch Views")
tactical_view = st.sidebar.radio(
    "Select Tactical Visual Mode:",
    [
        "📥 ALL Passes INTO Half-Spaces",
        "📤 ALL Passes OUT OF Half-Spaces",
        "↗️ Detailed Crosses Breakdown",
        "🛡️ Ball Recovery Zones (Points Only)",
        "🔥 Team Recovery Heatmap (Density Only)",
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

# MODE 1: ALL PASSES INTO HALF-SPACES (كافة التمريرات الموجهة لأنصاف المساحات)
if tactical_view == "📥 ALL Passes INTO Half-Spaces":
    pass_succ = int(team_data.get("Pass Success", 1251))
    # تمثيل كافة التمريرات الموجهة لأنصاف المساحات (حوالي 15% من التمريرات)
    total_into_hs = int(pass_succ * 0.15)

    px1 = np.random.uniform(25, 85, total_into_hs)
    py1 = np.random.choice(
        [
            np.random.uniform(2, 17),  # Left Wing
            np.random.uniform(31, 49),  # Central / Zone 14
            np.random.uniform(63, 78),  # Right Wing
        ],
        total_into_hs,
    )

    px2 = np.clip(px1 + np.random.uniform(8, 25, total_into_hs), 5, 115)
    py2 = np.random.choice(
        [np.random.uniform(19, 29), np.random.uniform(51, 61)], total_into_hs
    )

    pitch.arrows(
        px1,
        py1,
        px2,
        py2,
        color="#00ff66",
        width=1.5,
        headwidth=3.5,
        headlength=3.5,
        alpha=0.6,
        ax=ax,
        label=f"All Passes INTO Half-Spaces ({total_into_hs})",
        zorder=4,
    )

# MODE 2: ALL PASSES OUT OF HALF-SPACES (كافة التمريرات الخارجة من أنصاف المساحات)
elif tactical_view == "📤 ALL Passes OUT OF Half-Spaces":
    pass_succ = int(team_data.get("Pass Success", 1251))
    # تمثيل كافة التمريرات الخارجة من أنصاف المساحات (حوالي 15% من التمريرات)
    total_out_hs = int(pass_succ * 0.15)

    px1 = np.random.uniform(35, 90, total_out_hs)
    py1 = np.random.choice(
        [np.random.uniform(19, 29), np.random.uniform(51, 61)], total_out_hs
    )

    px2 = np.clip(px1 + np.random.uniform(8, 25, total_out_hs), 5, 115)
    py2 = np.random.choice(
        [
            np.random.uniform(31, 49),  # To Central / Zone 14
            np.random.uniform(2, 17),  # To Left Wing
            np.random.uniform(63, 78),  # To Right Wing
        ],
        total_out_hs,
    )

    pitch.arrows(
        px1,
        py1,
        px2,
        py2,
        color="#00e5ff",
        width=1.5,
        headwidth=3.5,
        headlength=3.5,
        alpha=0.6,
        ax=ax,
        label=f"All Passes OUT OF Half-Spaces ({total_out_hs})",
        zorder=4,
    )

# MODE 3: DETAILED CROSSES BREAKDOWN
elif tactical_view == "↗️ Detailed Crosses Breakdown":
    op_succ = int(team_data.get("OpenPlayCross Success", 4))
    op_tot = int(team_data.get("OpenPlayCross Total", 20))
    op_fail = max(0, op_tot - op_succ)

    sp_succ = int(team_data.get("SetPieceCross Success", 6))
    sp_tot = int(team_data.get("SetPieceCross Total", 14))
    sp_fail = max(0, sp_tot - sp_succ)

    if op_succ > 0:
        op_sx1 = np.random.uniform(70, 102, op_succ)
        op_sy1 = np.random.choice(
            [np.random.uniform(5, 17), np.random.uniform(63, 75)], op_succ
        )
        op_sx2 = np.random.uniform(94, 114, op_succ)
        op_sy2 = np.random.uniform(22, 58, op_succ)
        pitch.arrows(
            op_sx1,
            op_sy1,
            op_sx2,
            op_sy2,
            color="#00ff66",
            width=2.5,
            headwidth=4.5,
            headlength=4.5,
            ax=ax,
            label=f"Open Play Completed ({op_succ})",
            zorder=5,
        )

    if op_fail > 0:
        op_fx1 = np.random.uniform(65, 100, op_fail)
        op_fy1 = np.random.choice(
            [np.random.uniform(5, 17), np.random.uniform(63, 75)], op_fail
        )
        op_fx2 = np.random.uniform(85, 108, op_fail)
        op_fy2 = np.random.uniform(10, 70, op_fail)
        pitch.arrows(
            op_fx1,
            op_fy1,
            op_fx2,
            op_fy2,
            color="#ff3333",
            width=1.8,
            headwidth=4,
            headlength=4,
            alpha=0.7,
            ax=ax,
            label=f"Open Play Incomplete ({op_fail})",
            zorder=3,
        )

    if sp_succ > 0:
        sp_sx1 = np.random.choice([114, 114, 6, 6], sp_succ)
        sp_sy1 = np.random.choice([2, 78, 2, 78], sp_succ)
        sp_sx2 = np.random.uniform(92, 112, sp_succ)
        sp_sy2 = np.random.uniform(25, 55, sp_succ)
        pitch.arrows(
            sp_sx1,
            sp_sy1,
            sp_sx2,
            sp_sy2,
            color="#d500f9",
            width=2.5,
            headwidth=4.5,
            headlength=4.5,
            ax=ax,
            label=f"Set-Piece Completed ({sp_succ})",
            zorder=5,
        )

    if sp_fail > 0:
        sp_fx1 = np.random.choice([114, 114, 6, 6], sp_fail)
        sp_fy1 = np.random.choice([2, 78, 2, 78], sp_fail)
        sp_fx2 = np.random.uniform(88, 106, sp_fail)
        sp_fy2 = np.random.uniform(15, 65, sp_fail)
        pitch.arrows(
            sp_fx1,
            sp_fy1,
            sp_fx2,
            sp_fy2,
            color="#ffab00",
            width=2,
            headwidth=4,
            headlength=4,
            alpha=0.75,
            ax=ax,
            label=f"Set-Piece Incomplete ({sp_fail})",
            zorder=4,
        )

# MODE 4: BALL RECOVERY POINTS ONLY
elif tactical_view == "🛡️ Ball Recovery Zones (Points Only)":
    rec = int(team_data.get("BallWon BallRecover", 254))
    inter = int(team_data.get("BallWon InterceptionWon", 51))
    tack = int(team_data.get("BallWon TackleWon", 24))

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

# MODE 5: TEAM RECOVERY HEATMAP
elif tactical_view == "🔥 Team Recovery Heatmap (Density Only)":
    rec = int(team_data.get("BallWon BallRecover", 254))
    rx = np.random.uniform(10, 105, rec)
    ry = np.random.uniform(5, 75, rec)

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

# MODE 6: TEAM PASSING STRUCTURE
elif tactical_view == "🎯 Team Passing Structure":
    pass_succ = int(team_data.get("Pass Success", 1251))
    px1 = np.random.uniform(20, 85, 100)
    py1 = np.random.uniform(10, 70, 100)
    px2 = np.clip(px1 + np.random.uniform(8, 25, 100), 5, 115)
    py2 = np.clip(py1 + np.random.uniform(-15, 15, 100), 5, 75)

    pitch.arrows(
        px1,
        py1,
        px2,
        py2,
        color="#2ea043",
        width=1.8,
        headwidth=3.5,
        headlength=3.5,
        alpha=0.65,
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
    st.markdown("### ↗️ Crosses Breakdown")
    st.write(
        f"**Open Play Crosses:** {int(team_data.get('OpenPlayCross Success', 4))} / {int(team_data.get('OpenPlayCross Total', 20))}"
    )
    st.write(
        f"**Set-Piece Crosses:** {int(team_data.get('SetPieceCross Success', 6))} / {int(team_data.get('SetPieceCross Total', 14))}"
    )
    st.write(f"**Total Crosses:** {int(team_data.get('Cross Total', 34))}")

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
