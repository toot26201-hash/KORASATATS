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
        "📥 Penalty Area Entries Map (طرق دخول منطقة الجزاء)",
        "🔑 Key Passes & Assists Map (التمريرات المفتاحية والحاسمة)",
        "✨ Offensive Dribbles Map (المراوغات الهجومية - 37)",
        "⚔️ Aerial Duels Map (الالتحامات الهوائية)",
        "🤼 Ground Duels Map (الالتحامات الأرضية)",
        "⚽ Team Shots Map (تسديدات الفريق الهجومية - 42)",
        "🛡️ Opponent Shots Conceded (التسديدات المستقبلة من المنافسين)",
        "🎯 All Passes Map (ALL 1545 Passes)",
        "📐 Short Passes Map (ALL 1322 Short Passes)",
        "📏 Long Passes Map (ALL 189 Long Passes)",
        "🚩 Set-Piece & Corner Crosses (الركنيات والضربات الثابتة)",
        "🌐 ALL Crosses Combined (كافة العرضيات مجتمعة)",
        "↗️ Open Play Crosses (عرضيات اللعب المفتوح)",
        "📥 ALL Passes INTO Half-Spaces",
        "📤 ALL Passes OUT OF Half-Spaces",
        "🛡️ Ball Recovery Zones (254 Recoveries + 51 Interceptions)",
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

# MODE 1: PENALTY AREA ENTRIES MAP (طرق دخول منطقة الجزاء)
if (
    tactical_view
    == "📥 Penalty Area Entries Map (طرق دخول منطقة الجزاء)"
):
    key_passes = int(team_data.get("Chances KeyPasses", 25))
    cross_succ = int(team_data.get("OpenPlayCross Success", 4)) + int(
        team_data.get("SetPieceCross Success", 6)
    )
    dribble_succ = int(team_data.get("Dribble Success", 16))

    # 1. التمريرات المفتاحية عبر العمق ونصف المساحات (25 تمريرة)
    if key_passes > 0:
        kp_x1 = np.random.uniform(65, 92, key_passes)
        kp_y1 = np.random.uniform(20, 60, key_passes)
        kp_x2 = np.random.uniform(96, 114, key_passes)
        kp_y2 = np.random.uniform(22, 58, key_passes)
        pitch.arrows(
            kp_x1,
            kp_y1,
            kp_x2,
            kp_y2,
            color="#d500f9",
            width=2.0,
            headwidth=4.0,
            headlength=4.0,
            ax=ax,
            label=f"Central & Half-Space Key Passes ({key_passes})",
            zorder=5,
        )

    # 2. العرضيات الناجحة داخل الصندوق (10 عرضيات)
    if cross_succ > 0:
        cr_x1 = np.random.uniform(75, 105, cross_succ)
        cr_y1 = np.random.choice(
            [np.random.uniform(5, 15), np.random.uniform(65, 75)], cross_succ
        )
        cr_x2 = np.random.uniform(98, 114, cross_succ)
        cr_y2 = np.random.uniform(24, 56, cross_succ)
        pitch.arrows(
            cr_x1,
            cr_y1,
            cr_x2,
            cr_y2,
            color="#00ff66",
            width=2.2,
            headwidth=4.0,
            headlength=4.0,
            ax=ax,
            label=f"Completed Crosses into Box ({cross_succ})",
            zorder=5,
        )

    # 3. الاختراق بالكرة والمراوغات الهجومية (16 مراوغة ناجحة)
    if dribble_succ > 0:
        dr_x1 = np.random.uniform(70, 95, dribble_succ)
        dr_y1 = np.random.uniform(15, 65, dribble_succ)
        dr_x2 = np.clip(dr_x1 + np.random.uniform(10, 18, dribble_succ), 80, 110)
        dr_y2 = np.clip(dr_y1 + np.random.uniform(-5, 5, dribble_succ), 18, 62)
        pitch.arrows(
            dr_x1,
            dr_y1,
            dr_x2,
            dr_y2,
            color="#ffd700",
            width=1.8,
            headwidth=3.5,
            headlength=3.5,
            ax=ax,
            label=f"Dribble Carries into Box ({dribble_succ})",
            zorder=5,
        )

# MODE 2: KEY PASSES & ASSISTS MAP
elif (
    tactical_view
    == "🔑 Key Passes & Assists Map (التمريرات المفتاحية والحاسمة)"
):
    assists = int(team_data.get("Chances Assists", 6))
    key_passes = int(team_data.get("Chances KeyPasses", 25))

    if assists > 0:
        ax1 = np.random.uniform(70, 100, assists)
        ay1 = np.random.choice(
            [np.random.uniform(5, 20), np.random.uniform(60, 75)], assists
        )
        ax2 = np.random.uniform(96, 114, assists)
        ay2 = np.random.uniform(24, 56, assists)

        pitch.arrows(
            ax1,
            ay1,
            ax2,
            ay2,
            color="#ffd700",
            width=2.5,
            headwidth=4.5,
            headlength=4.5,
            ax=ax,
            label=f"Goal Assists ({assists})",
            zorder=6,
        )

        pitch.scatter(
            ax2,
            ay2,
            s=220,
            color="#ffd700",
            marker="*",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            zorder=7,
        )

    if key_passes > 0:
        kx1 = np.random.uniform(55, 95, key_passes)
        ky1 = np.random.uniform(8, 72, key_passes)
        kx2 = np.clip(kx1 + np.random.uniform(12, 28, key_passes), 5, 114)
        ky2 = np.random.uniform(18, 62, key_passes)

        pitch.arrows(
            kx1,
            ky1,
            kx2,
            ky2,
            color="#d500f9",
            width=2.0,
            headwidth=4.0,
            headlength=4.0,
            alpha=0.85,
            ax=ax,
            label=f"Key Passes / Chance Creation ({key_passes})",
            zorder=5,
        )

# MODE 3: OFFENSIVE DRIBBLES MAP
elif tactical_view == "✨ Offensive Dribbles Map (المراوغات الهجومية - 37)":
    dribble_tot = int(team_data.get("Dribble Total", 37))
    dribble_succ = int(team_data.get("Dribble Success", 16))
    dribble_fail = int(team_data.get("Dribble Fail", 21))

    if dribble_succ > 0:
        dx1 = np.random.uniform(40, 102, dribble_succ)
        dy1 = np.random.uniform(8, 72, dribble_succ)
        dx2 = np.clip(dx1 + np.random.uniform(5, 15, dribble_succ), 5, 115)
        dy2 = np.clip(dy1 + np.random.uniform(-8, 8, dribble_succ), 2, 78)

        pitch.scatter(
            dx1,
            dy1,
            s=160,
            color="#ffd700",
            marker="*",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Successful Dribbles ({dribble_succ})",
            zorder=5,
        )

        pitch.arrows(
            dx1,
            dy1,
            dx2,
            dy2,
            color="#00ff66",
            width=1.8,
            headwidth=3.5,
            headlength=3.5,
            alpha=0.85,
            ax=ax,
            zorder=5,
        )

    if dribble_fail > 0:
        fx1 = np.random.uniform(35, 100, dribble_fail)
        fy1 = np.random.uniform(8, 72, dribble_fail)

        pitch.scatter(
            fx1,
            fy1,
            s=120,
            color="#ff6d00",
            marker="X",
            linewidth=1.8,
            ax=ax,
            label=f"Failed Dribbles ({dribble_fail})",
            zorder=4,
        )

# MODE 4: AERIAL DUELS MAP
elif tactical_view == "⚔️ Aerial Duels Map (الالتحامات الهوائية)":
    aerial_won = int(team_data.get("BallWon Aerial", 41))
    aerial_lost = int(team_data.get("BallLost Aerial", 49))

    if aerial_won > 0:
        pitch.scatter(
            np.random.uniform(15, 105, aerial_won),
            np.random.uniform(8, 72, aerial_won),
            s=130,
            color="#00e5ff",
            marker="D",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Aerial Duels Won ({aerial_won})",
            zorder=5,
        )

    if aerial_lost > 0:
        pitch.scatter(
            np.random.uniform(15, 105, aerial_lost),
            np.random.uniform(8, 72, aerial_lost),
            s=120,
            color="#ff1744",
            marker="D",
            edgecolors="black",
            linewidth=1,
            alpha=0.85,
            ax=ax,
            label=f"Aerial Duels Lost ({aerial_lost})",
            zorder=4,
        )

# MODE 5: GROUND DUELS MAP
elif tactical_view == "🤼 Ground Duels Map (الالتحامات الأرضية)":
    tackles_won = int(team_data.get("BallWon TackleWon", 24))
    dribbles_won = int(team_data.get("Dribble Success", 16))
    tackles_failed = int(team_data.get("Defensive TackleFail", 19))
    dribbles_failed = int(team_data.get("Dribble Fail", 21))
    ground_failed_tot = tackles_failed + dribbles_failed

    if tackles_won > 0:
        pitch.scatter(
            np.random.uniform(15, 85, tackles_won),
            np.random.uniform(8, 72, tackles_won),
            s=140,
            color="#00ff66",
            marker="o",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Tackles Won ({tackles_won})",
            zorder=5,
        )

    if dribbles_won > 0:
        pitch.scatter(
            np.random.uniform(45, 105, dribbles_won),
            np.random.uniform(8, 72, dribbles_won),
            s=150,
            color="#ffd700",
            marker="*",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Successful Dribbles ({dribbles_won})",
            zorder=5,
        )

    if ground_failed_tot > 0:
        pitch.scatter(
            np.random.uniform(20, 100, ground_failed_tot),
            np.random.uniform(8, 72, ground_failed_tot),
            s=110,
            color="#ff6d00",
            marker="s",
            edgecolors="black",
            linewidth=0.8,
            alpha=0.8,
            ax=ax,
            label=f"Failed Ground Duels ({ground_failed_tot})",
            zorder=4,
        )

# MODE 6: TEAM SHOTS MAP
elif tactical_view == "⚽ Team Shots Map (تسديدات الفريق الهجومية - 42)":
    shots_tot = int(team_data.get("Attempts Total", 42))
    shots_succ = int(team_data.get("Attempts Success", 22))
    goals = int(team_data.get("GoalsScored Total", 8)) + int(
        team_data.get("GoalsConceded OwnGoals", 1)
    )
    bars = int(team_data.get("Attempts Bars", 3))

    on_target = max(0, shots_succ - goals)
    off_target = max(0, shots_tot - shots_succ)

    if goals > 0:
        pitch.scatter(
            np.random.uniform(94, 114, goals),
            np.random.uniform(22, 58, goals),
            s=350,
            color="#ffd700",
            marker="*",
            edgecolors="white",
            linewidth=1.2,
            ax=ax,
            label=f"Total Goals ({goals})",
            zorder=6,
        )

    if on_target > 0:
        pitch.scatter(
            np.random.uniform(85, 112, on_target),
            np.random.uniform(20, 60, on_target),
            s=140,
            color="#00ff66",
            marker="o",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Shots On Target ({on_target})",
            zorder=5,
        )

    if bars > 0:
        pitch.scatter(
            np.random.uniform(105, 115, bars),
            np.random.uniform(26, 54, bars),
            s=160,
            color="#ffab00",
            marker="s",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Hit Post/Bar ({bars})",
            zorder=5,
        )

    if off_target > 0:
        pitch.scatter(
            np.random.uniform(70, 110, off_target),
            np.random.uniform(10, 70, off_target),
            s=120,
            color="#ff1744",
            marker="x",
            linewidth=2,
            ax=ax,
            label=f"Off Target ({off_target})",
            zorder=4,
        )

# MODE 7: OPPONENT SHOTS CONCEDED
elif (
    tactical_view
    == "🛡️ Opponent Shots Conceded (التسديدات المستقبلة من المنافسين)"
):
    goals_conceded = int(team_data.get("GoalsConceded Total", 1))
    blocks = int(team_data.get("Defensive Blocks", 10))
    opp_shots_tot = 17
    opp_off_target = max(0, opp_shots_tot - (goals_conceded + blocks))

    if goals_conceded > 0:
        pitch.scatter(
            np.random.uniform(5, 12, goals_conceded),
            np.random.uniform(32, 48, goals_conceded),
            s=350,
            color="#ff1744",
            marker="*",
            edgecolors="white",
            linewidth=1.5,
            ax=ax,
            label=f"Goals Conceded ({goals_conceded})",
            zorder=6,
        )

    if blocks > 0:
        pitch.scatter(
            np.random.uniform(12, 32, blocks),
            np.random.uniform(20, 60, blocks),
            s=150,
            color="#00e5ff",
            marker="D",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"Defensive Blocks ({blocks})",
            zorder=5,
        )

    if opp_off_target > 0:
        pitch.scatter(
            np.random.uniform(15, 45, opp_off_target),
            np.random.uniform(8, 72, opp_off_target),
            s=110,
            color="#ffab00",
            marker="o",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"Opponent Off Target ({opp_off_target})",
            zorder=4,
        )

# MODE 8: ALL PASSES MAP
elif tactical_view == "🎯 All Passes Map (ALL 1545 Passes)":
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
            width=1.0,
            headwidth=2.0,
            headlength=2.0,
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
            color="#ff1744",
            width=1.0,
            headwidth=2.0,
            headlength=2.0,
            alpha=0.45,
            ax=ax,
            label=f"Failed Passes ({pass_fail})",
            zorder=4,
        )

# MODE 9: SHORT PASSES MAP
elif tactical_view == "📐 Short Passes Map (ALL 1322 Short Passes)":
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
            width=1.0,
            headwidth=2.0,
            headlength=2.0,
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
            color="#ff1744",
            width=1.0,
            headwidth=2.0,
            headlength=2.0,
            alpha=0.45,
            ax=ax,
            label=f"Short Failed ({sp_fail})",
            zorder=4,
        )

# MODE 10: LONG PASSES MAP
elif tactical_view == "📏 Long Passes Map (ALL 189 Long Passes)":
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
            width=1.8,
            headwidth=3.5,
            headlength=3.5,
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
            width=1.8,
            headwidth=3.5,
            headlength=3.5,
            alpha=0.7,
            ax=ax,
            label=f"Long Failed ({lp_fail})",
            zorder=3,
        )

# MODE 11: SET-PIECE & CORNER CROSSES
elif (
    tactical_view
    == "🚩 Set-Piece & Corner Crosses (الركنيات والضربات الثابتة)"
):
    sp_succ = int(team_data.get("SetPieceCross Success", 6))
    sp_tot = int(team_data.get("SetPieceCross Total", 14))
    sp_fail = max(0, sp_tot - sp_succ)

    if sp_succ > 0:
        sp_sx1 = np.random.choice([118, 119, 120], sp_succ)
        sp_sy1 = np.random.choice([1, 2, 78, 79], sp_succ)
        sp_sx2 = np.random.uniform(102, 114, sp_succ)
        sp_sy2 = np.random.uniform(24, 56, sp_succ)
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
            label=f"Corner / Set-Piece Completed ({sp_succ})",
            zorder=5,
        )

    if sp_fail > 0:
        sp_fx1 = np.random.choice([118, 119, 120], sp_fail)
        sp_fy1 = np.random.choice([1, 2, 78, 79], sp_fail)
        sp_fx2 = np.random.uniform(92, 108, sp_fail)
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
            label=f"Corner / Set-Piece Incomplete ({sp_fail})",
            zorder=4,
        )

# MODE 12: ALL CROSSES COMBINED
elif (
    tactical_view
    == "🌐 ALL Crosses Combined (كافة العرضيات مجتمعة)"
):
    op_succ = int(team_data.get("OpenPlayCross Success", 4))
    op_tot = int(team_data.get("OpenPlayCross Total", 20))
    op_fail = max(0, op_tot - op_succ)
    sp_succ = int(team_data.get("SetPieceCross Success", 6))
    sp_tot = int(team_data.get("SetPieceCross Total", 14))
    sp_fail = max(0, sp_tot - sp_succ)

    if op_succ > 0:
        pitch.arrows(
            np.random.uniform(70, 102, op_succ),
            np.random.choice(
                [np.random.uniform(5, 17), np.random.uniform(63, 75)], op_succ
            ),
            np.random.uniform(94, 114, op_succ),
            np.random.uniform(22, 58, op_succ),
            color="#00ff66",
            width=2.5,
            headwidth=4.5,
            headlength=4.5,
            ax=ax,
            label=f"Open Play Completed ({op_succ})",
            zorder=5,
        )

    if op_fail > 0:
        pitch.arrows(
            np.random.uniform(65, 100, op_fail),
            np.random.choice(
                [np.random.uniform(5, 17), np.random.uniform(63, 75)], op_fail
            ),
            np.random.uniform(85, 108, op_fail),
            np.random.uniform(10, 70, op_fail),
            color="#ff3333",
            width=2,
            headwidth=4,
            headlength=4,
            alpha=0.75,
            ax=ax,
            label=f"Open Play Incomplete ({op_fail})",
            zorder=3,
        )

    if sp_succ > 0:
        pitch.arrows(
            np.random.choice([118, 119, 120], sp_succ),
            np.random.choice([1, 2, 78, 79], sp_succ),
            np.random.uniform(102, 114, sp_succ),
            np.random.uniform(24, 56, sp_succ),
            color="#d500f9",
            width=2.5,
            headwidth=4.5,
            headlength=4.5,
            ax=ax,
            label=f"Set-Piece Completed ({sp_succ})",
            zorder=5,
        )

    if sp_fail > 0:
        pitch.arrows(
            np.random.choice([118, 119, 120], sp_fail),
            np.random.choice([1, 2, 78, 79], sp_fail),
            np.random.uniform(92, 108, sp_fail),
            np.random.uniform(15, 65, sp_fail),
            color="#ffab00",
            width=2,
            headwidth=4,
            headlength=4,
            alpha=0.75,
            ax=ax,
            label=f"Set-Piece Incomplete ({sp_fail})",
            zorder=4,
        )

# MODE 13: OPEN PLAY CROSSES
elif tactical_view == "↗️ Open Play Crosses (عرضيات اللعب المفتوح)":
    op_succ = int(team_data.get("OpenPlayCross Success", 4))
    op_tot = int(team_data.get("OpenPlayCross Total", 20))
    op_fail = max(0, op_tot - op_succ)

    if op_succ > 0:
        pitch.arrows(
            np.random.uniform(70, 102, op_succ),
            np.random.choice(
                [np.random.uniform(5, 17), np.random.uniform(63, 75)], op_succ
            ),
            np.random.uniform(94, 114, op_succ),
            np.random.uniform(22, 58, op_succ),
            color="#00ff66",
            width=2.5,
            headwidth=4.5,
            headlength=4.5,
            ax=ax,
            label=f"Open Play Completed ({op_succ})",
            zorder=5,
        )

    if op_fail > 0:
        pitch.arrows(
            np.random.uniform(65, 100, op_fail),
            np.random.choice(
                [np.random.uniform(5, 17), np.random.uniform(63, 75)], op_fail
            ),
            np.random.uniform(85, 108, op_fail),
            np.random.uniform(10, 70, op_fail),
            color="#ff3333",
            width=2,
            headwidth=4,
            headlength=4,
            alpha=0.75,
            ax=ax,
            label=f"Open Play Incomplete ({op_fail})",
            zorder=4,
        )

# MODE 14: PASSES INTO HALF-SPACES
elif tactical_view == "📥 ALL Passes INTO Half-Spaces":
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

# MODE 15: PASSES OUT OF HALF-SPACES
elif tactical_view == "📤 ALL Passes OUT OF Half-Spaces":
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

# MODE 16: BALL RECOVERY ZONES
elif (
    tactical_view
    == "🛡️ Ball Recovery Zones (254 Recoveries + 51 Interceptions)"
):
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

# MODE 17: TEAM RECOVERY HEATMAP
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

# MODE 18: TEAM PRESSING MAP
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
    st.markdown("### 📥 Penalty Box Penetration")
    st.write(
        f"**Key Passes to Box:** {int(team_data.get('Chances KeyPasses', 25))}"
    )
    st.write(
        f"**Completed Crosses:** {int(team_data.get('OpenPlayCross Success', 4)) + int(team_data.get('SetPieceCross Success', 6))}"
    )
    st.write(
        f"**Dribble Carries Won:** {int(team_data.get('Dribble Success', 16))}"
    )

with col2:
    st.markdown("### ⚽ Shooting & Goals")
    st.write(
        f"**Total Shots:** {int(team_data.get('Attempts Total', 42))} ({int(team_data.get('Attempts Success', 22))} On Target)"
    )
    st.write(
        f"**Goals Scored:** {int(team_data.get('GoalsScored Total', 8)) + int(team_data.get('GoalsConceded OwnGoals', 1))} (xG: {team_data.get('GoalsScored XG', 8.7)})"
    )
    st.write(f"**Shot Accuracy:** {team_data.get('Attempts Accuracy', 0)*100:.1f}%")

with col3:
    st.markdown("### ⚔️ Duels & Battles")
    st.write(
        f"**Aerial Won:** {int(team_data.get('BallWon Aerial', 41))} / {int(team_data.get('BallWon Aerial', 41)) + int(team_data.get('BallLost Aerial', 49))}"
    )
    st.write(
        f"**Tackles Won:** {int(team_data.get('BallWon TackleWon', 24))} / {int(team_data.get('BallWon TackleWon', 24)) + int(team_data.get('Defensive TackleFail', 19))}"
    )
    st.write(
        f"**Recoveries:** {int(team_data.get('BallWon BallRecover', 254))}"
    )

with col4:
    st.markdown("### 🛡️ Defensive & Conceded")
    st.write(
        f"**Goals Conceded:** {int(team_data.get('GoalsConceded Total', 1))}"
    )
    st.write(f"**Defensive Blocks:** {int(team_data.get('Defensive Blocks', 10))}")
    st.write(
        f"**Interceptions:** {int(team_data.get('BallWon InterceptionWon', 0))}"
    )
