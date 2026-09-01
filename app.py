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
        "↗️ Open Play Crosses (عرضيات اللعب المفتوح)",
        "🚩 Set-Piece & Corner Crosses (الركنيات والضربات الثابتة)",
        "🎯 All Passes Map (كافة التمريرات)",
        "📐 Short Passes Map (التمريرات القصيرة)",
        "📏 Long Passes Map (التمريرات الطويلة)",
        "📥 Passes INTO Half-Spaces",
        "📤 Passes OUT OF Half-Spaces",
        "🛡️ Ball Recovery Zones (Points Only)",
        "🔥 Team Recovery Heatmap (Density Only)",
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
    f"{team_name.upper()} - {tactical_view.split(' (')[0].upper()}",
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

# MODE 1: OPEN PLAY CROSSES (عرضيات اللعب المفتوح فقط)
if tactical_view == "↗️ Open Play Crosses (عرضيات اللعب المفتوح)":
    op_succ = int(team_data.get("OpenPlayCross Success", 4))
    op_tot = int(team_data.get("OpenPlayCross Total", 20))
    op_fail = max(0, op_tot - op_succ)

    # Completed Open Play Crosses (Green Arrows - 4)
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

    # Incomplete Open Play Crosses (Red Arrows - 16)
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
            width=2,
            headwidth=4,
            headlength=4,
            alpha=0.75,
            ax=ax,
            label=f"Open Play Incomplete ({op_fail})",
            zorder=4,
        )

# MODE 2: SET-PIECE & CORNER CROSSES (الركنيات والضربات الثابتة)
elif tactical_view == "🚩 Set-Piece & Corner Crosses (الركنيات والضربات الثابتة)":
    sp_succ = int(team_data.get("SetPieceCross Success", 6))
    sp_tot = int(team_data.get("SetPieceCross Total", 14))
    sp_fail = max(0, sp_tot - sp_succ)

    # Completed Set-Piece & Corners (Purple Arrows - 6)
    if sp_succ > 0:
        sp_sx1 = np.random.choice([114, 114, 6, 6], sp_succ)  # Corner Flags
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

    # Incomplete Set-Piece & Corners (Orange Arrows - 8)
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

# MODE 3: ALL PASSES
elif tactical_view == "🎯 All Passes Map (كافة التمريرات)":
    pass_tot = int(team_data.get("Pass Total", 1545))
    pass_succ = int(team_data.get("Pass Success", 1251))
    pass_fail = max(0, pass_tot - pass_succ)

    if pass_succ > 0:
        px1 = np.random.uniform(5, 105, pass_succ)
        py1 = np.random.uniform(2, 78, pass_succ)
        px2 = np.clip(px1 + np.random.uniform(-15, 35, pass_succ), 5, 115)
        py2 = np.clip(py1 + np.random.uniform(-25, 25, pass_succ), 2, 78)
        pitch.arrows(
            px1,
            py1,
            px2,
            py2,
            color="#00ff66",
            width=1.2,
            headwidth=2.5,
            headlength=2.5,
            alpha=0.25,
            ax=ax,
            label=f"Successful Passes ({pass_succ})",
            zorder=3,
        )

    if pass_fail > 0:
        fx1 = np.random.uniform(10, 105, pass_fail)
        fy1 = np.random.uniform(5, 75, pass_fail)
        fx2 = np.clip(fx1 + np.random.uniform(-15, 35, pass_fail), 5, 115)
        fy2 = np.clip(fy1 + np.random.uniform(-25, 25, pass_fail), 5, 75)
        pitch.arrows(
            fx1,
            fy1,
            fx2,
            fy2,
            color="#ff3333",
            width=1.2,
            headwidth=2.5,
            headlength=2.5,
            alpha=0.4,
            ax=ax,
            label=f"Failed Passes ({pass_fail})",
            zorder=4,
        )

# MODE 4: SHORT PASSES
elif tactical_view == "📐 Short Passes Map (التمريرات القصيرة)":
    sp_tot = int(team_data.get("ShortPass Total", 1322))
    sp_succ = int(team_data.get("ShortPass Success", 1165))
    sp_fail = max(0, sp_tot - sp_succ)

    if sp_succ > 0:
        px1 = np.random.uniform(10, 100, sp_succ)
        py1 = np.random.uniform(2, 78, sp_succ)
        px2 = np.clip(px1 + np.random.uniform(-10, 20, sp_succ), 5, 115)
        py2 = np.clip(py1 + np.random.uniform(-15, 15, sp_succ), 2, 78)
        pitch.arrows(
            px1,
            py1,
            px2,
            py2,
            color="#00e5ff",
            width=1.2,
            headwidth=2.5,
            headlength=2.5,
            alpha=0.25,
            ax=ax,
            label=f"Short Success ({sp_succ})",
            zorder=3,
        )

    if sp_fail > 0:
        fx1 = np.random.uniform(10, 100, sp_fail)
        fy1 = np.random.uniform(5, 75, sp_fail)
        fx2 = np.clip(fx1 + np.random.uniform(-10, 20, sp_fail), 5, 115)
        fy2 = np.clip(fy1 + np.random.uniform(-15, 15, sp_fail), 5, 75)
        pitch.arrows(
            fx1,
            fy1,
            fx2,
            fy2,
            color="#ff3333",
            width=1.2,
            headwidth=2.5,
            headlength=2.5,
            alpha=0.5,
            ax=ax,
            label=f"Short Failed ({sp_fail})",
            zorder=4,
        )

# MODE 5: LONG PASSES
elif tactical_view == "📏 Long Passes Map (التمريرات الطويلة)":
    lp_tot = int(team_data.get("LongPass Total", 189))
    lp_succ = int(team_data.get("LongPass Success", 76))
    lp_fail = max(0, lp_tot - lp_succ)

    if lp_succ > 0:
        px1 = np.random.uniform(5, 65, lp_succ)
        py1 = np.random.uniform(5, 75, lp_succ)
        px2 = np.clip(px1 + np.random.uniform(35, 70, lp_succ), 5, 115)
        py2 = np.clip(
            py1
            + np.random.choice(
                [np.random.uniform(20, 50), np.random.uniform(-50, -20)],
                lp_succ,
            ),
            2,
            78,
        )
        pitch.arrows(
            px1,
            py1,
            px2,
            py2,
            color="#d500f9",
            width=2,
            headwidth=4,
            headlength=4,
            alpha=0.7,
            ax=ax,
            label=f"Long Success ({lp_succ})",
            zorder=4,
        )

    if lp_fail > 0:
        fx1 = np.random.uniform(5, 65, lp_fail)
        fy1 = np.random.uniform(5, 75, lp_fail)
        fx2 = np.clip(fx1 + np.random.uniform(35, 70, lp_fail), 5, 115)
        fy2 = np.clip(
            fy1
            + np.random.choice(
                [np.random.uniform(20, 50), np.random.uniform(-50, -20)],
                lp_fail,
            ),
            2,
            78,
        )
        pitch.arrows(
            fx1,
            fy1,
            fx2,
            fy2,
            color="#ffab00",
            width=2,
            headwidth=4,
            headlength=4,
            alpha=0.7,
            ax=ax,
            label=f"Long Failed ({lp_fail})",
            zorder=3,
        )

# MODE 6: PASSES INTO HALF-SPACES
elif tactical_view == "📥 Passes INTO Half-Spaces":
    pass_succ = int(team_data.get("Pass Success", 1251))
    total_into_hs = int(pass_succ * 0.15)
    px1 = np.random.uniform(25, 85, total_into_hs)
    py1 = np.random.choice(
        [
            np.random.uniform(2, 17),
            np.random.uniform(31, 49),
            np.random.uniform(63, 78),
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
        label=f"Passes INTO Half-Spaces ({total_into_hs})",
        zorder=4,
    )

# MODE 7: PASSES OUT OF HALF-SPACES
elif tactical_view == "📤 Passes OUT OF Half-Spaces":
    pass_succ = int(team_data.get("Pass Success", 1251))
    total_out_hs = int(pass_succ * 0.15)
    px1 = np.random.uniform(35, 90, total_out_hs)
    py1 = np.random.choice(
        [np.random.uniform(19, 29), np.random.uniform(51, 61)], total_out_hs
    )
    px2 = np.clip(px1 + np.random.uniform(8, 25, total_out_hs), 5, 115)
    py2 = np.random.choice(
        [
            np.random.uniform(31, 49),
            np.random.uniform(2, 17),
            np.random.uniform(63, 78),
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
        label=f"Passes OUT OF Half-Spaces ({total_out_hs})",
        zorder=4,
    )

# MODE 8: BALL RECOVERY POINTS ONLY
elif tactical_view == "🛡️ Ball Recovery Zones (Points Only)":
    rec = int(team_data.get("BallWon BallRecover", 254))
    inter = int(team_data.get("BallWon InterceptionWon", 51))
    tack = int(team_data.get("BallWon TackleWon", 24))

    pitch.scatter(
        np.random.uniform(10, 105, rec),
        np.random.uniform(5, 75, rec),
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
        pitch.scatter(
            np.random.uniform(15, 95, inter),
            np.random.uniform(5, 75, inter),
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
        pitch.scatter(
            np.random.uniform(15, 85, tack),
            np.random.uniform(5, 75, tack),
            s=60,
            color="#00ff66",
            marker="o",
            edgecolors="black",
            linewidth=0.6,
            ax=ax,
            label=f"Tackles Won ({tack})",
            zorder=5,
        )

# MODE 9: TEAM RECOVERY HEATMAP
elif tactical_view == "🔥 Team Recovery Heatmap (Density Only)":
    rec = int(team_data.get("BallWon BallRecover", 254))
    sns.kdeplot(
        x=np.random.uniform(10, 105, rec),
        y=np.random.uniform(5, 75, rec),
        ax=ax,
        fill=True,
        thresh=0.05,
        levels=15,
        cmap="YlOrRd",
        alpha=0.75,
        zorder=2,
    )

# MODE 10: TEAM PRESSING MAP
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
        f"**Set-Piece & Corners:** {int(team_data.get('SetPieceCross Success', 6))} / {int(team_data.get('SetPieceCross Total', 14))}"
    )
    st.write(f"**Total Crosses:** {int(team_data.get('Cross Total', 34))}")

with col2:
    st.markdown("### ⚽ Passing Metrics")
    st.write(
        f"**Total Passes:** {int(team_data.get('Pass Total', 0))} ({int(team_data.get('Pass Success', 0))} Succ.)"
    )
    st.write(
        f"**Short Passes:** {int(team_data.get('ShortPass Total', 0))} ({int(team_data.get('ShortPass Success', 0))} Succ.)"
    )
    st.write(
        f"**Long Passes:** {int(team_data.get('LongPass Total', 0))} ({int(team_data.get('LongPass Success', 0))} Succ.)"
    )

with col3:
    st.markdown("### 🎯 Possession & Dominance")
    st.write(
        f"**Avg Possession:** {team_data.get('Possession_TimePercent Average', 0)*100:.1f}%"
    )
    st.write(f"**Offsides:** {int(team_data.get('Admin Offside', 0))}")
    st.write(f"**Corners Won:** {int(team_data.get('Admin Corners', 0))}")

with col4:
    st.markdown("### 🛡️ Defensive Actions")
    st.write(
        f"**Ball Recoveries:** {int(team_data.get('BallWon BallRecover', 0))}"
    )
    st.write(
        f"**Interceptions:** {int(team_data.get('BallWon InterceptionWon', 0))}"
    )
    st.write(f"**Tackles Won:** {int(team_data.get('BallWon TackleWon', 0))}")
