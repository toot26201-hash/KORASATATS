import os
import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns
import streamlit as st
from mplsoccer import Pitch

# Page Configuration
st.set_page_config(
    page_title="Football Analytics Dashboard", layout="wide"
)

st.title("⚽ Football Data Analytics Dashboard")

# ---------------------------------------------------------
# 1. Sidebar File Uploader (مرن للملفين)
# ---------------------------------------------------------
st.sidebar.header("📁 Upload Data")
uploaded_file = st.sidebar.file_uploader(
    "Upload CSV File (Players or Team Data):", type=["csv"]
)


@st.cache_data
def load_data(file):
    return pd.read_csv(file)


df = None

# التحقق من الملف المرفوع أو البحث عن الملف المحتفظ به محلية
if uploaded_file is not None:
    df = load_data(uploaded_file)
else:
    # محاولة قراءة الملف الافتراضي إن وجد على GitHub
    base_dir = os.path.dirname(os.path.abspath(__file__))
    players_path = os.path.join(base_dir, "PlayersData_2215.csv")
    team_path = os.path.join(base_dir, "Data_2215.csv")

    if os.path.exists(players_path):
        df = pd.read_csv(players_path)
    elif os.path.exists(team_path):
        df = pd.read_csv(team_path)
    else:
        st.info(
            "👋 Welcome! Please upload your data file (`PlayersData_2215.csv` or `Data_2215.csv`) from the sidebar to begin."
        )
        st.stop()

# ---------------------------------------------------------
# 2. تحديد نوع الملف المرفوع تلقائياً (Player File vs Team File)
# ---------------------------------------------------------
is_team_file = "Team Name" in df.columns and "Full Name" not in df.columns

# =========================================================
# TYPE A: TEAM REPORT DASHBOARD (في حالة رفع Data_2215.csv)
# =========================================================
if is_team_file:
    team_data = df.iloc[0]
    st.header(f"🛡️ Team Executive Overview: {team_data['Team Name']}")

    # KPIs Row
    k1, k2, k3, k4, k5 = st.columns(5)
    k1.metric("Matches Played", int(team_data.get("Admin MatchesPlayed", 0)))
    k2.metric(
        "Record (W-D-L)",
        f"{int(team_data.get('Admin Win', 0))}-{int(team_data.get('Admin Draw', 0))}-{int(team_data.get('Admin Lost', 0))}",
    )
    k3.metric(
        "Goals (Scored/Conceded)",
        f"{int(team_data.get('GoalsScored Total', 0))} / {int(team_data.get('GoalsConceded Total', 0))}",
    )
    k4.metric("Expected Goals (xG)", team_data.get("GoalsScored XG", 0))
    k5.metric(
        "Avg Possession",
        f"{team_data.get('Possession_TimePercent Average', 0)*100:.1f}%",
    )

    st.markdown("---")

    # Possession Interval Chart
    st.subheader("⏱️ Possession & Dominance Timeline (15-min Intervals)")
    pos_intervals = {
        "0-15m": team_data.get("Possession_TimePercent T_0_15", 0) * 100,
        "15-30m": team_data.get("Possession_TimePercent T_15_30", 0) * 100,
        "30-45m": team_data.get("Possession_TimePercent T_30_45", 0) * 100,
        "45-60m": team_data.get("Possession_TimePercent T_45_60", 0) * 100,
        "60-75m": team_data.get("Possession_TimePercent T_60_75", 0) * 100,
        "75-90m": team_data.get("Possession_TimePercent T_75_90", 0) * 100,
    }
    pos_df = pd.DataFrame(
        list(pos_intervals.items()), columns=["Interval", "Possession %"]
    )
    fig_pos = px.line(
        pos_df,
        x="Interval",
        y="Possession %",
        markers=True,
        title="Possession Percentage Across Match Intervals",
    )
    fig_pos.update_traces(line_color="#00e676", line_width=3)
    st.plotly_chart(fig_pos, use_container_width=True)

    # Ball Recoveries
    st.subheader("🛡️ Ball Recovery & Defensive Actions")
    rec_data = {
        "Ball Recoveries": team_data.get("BallWon BallRecover", 0),
        "Interceptions": team_data.get("BallWon InterceptionWon", 0),
        "Tackles Won": team_data.get("BallWon TackleWon", 0),
        "Aerial Duels Won": team_data.get("BallWon Aerial", 0),
    }
    rec_df = pd.DataFrame(
        list(rec_data.items()), columns=["Action Type", "Count"]
    )
    fig_rec = px.bar(
        rec_df,
        x="Action Type",
        y="Count",
        color="Action Type",
        title="Team Ball Recovery Breakdown",
    )
    st.plotly_chart(fig_rec, use_container_width=True)

# =========================================================
# TYPE B: PLAYER PITCH MAPS (في حالة رفع PlayersData_2215.csv)
# =========================================================
else:
    selected_team = st.sidebar.selectbox(
        "Select Team:", sorted(df["Team"].dropna().unique())
    )
    team_players = df[df["Team"] == selected_team]

    selected_player = st.sidebar.selectbox(
        "Select Player:", sorted(team_players["Full Name"].dropna().unique())
    )
    p_data = df[df["Full Name"] == selected_player].iloc[0]

    st.sidebar.markdown("---")
    st.sidebar.header("🗺️ Pitch View Mode")
    pitch_mode = st.sidebar.radio(
        "Choose Visualization Type:",
        ["Action Map Only", "Heatmap Only", "Combined Overlay"],
    )

    if pitch_mode in ["Action Map Only", "Combined Overlay"]:
        st.sidebar.markdown("---")
        st.sidebar.header("🎨 Toggle Visible Events")
        show_passes = st.sidebar.checkbox(
            "🎯 Passes (Green / Red Arrows)", value=True
        )
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
            "⚠️ Fouls & Cards (Red Hexagons)", value=True
        )
    else:
        show_passes = show_goals = show_assists = show_crosses = False
        show_dribbles = show_ball_won = show_clearances = show_fouls = False

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

    # Black Background Pitch Setup
    pitch = Pitch(half=False, pitch_color="#000000", line_color="#ffffff")
    fig, ax = pitch.draw(figsize=(13, 9))
    fig.patch.set_facecolor("#000000")

    player_name_str = (
        f"{p_data['Full Name'].upper()} ({p_data['Team']}) - {pos}"
    )
    ax.text(
        60,
        76,
        player_name_str,
        color="#ffffff",
        fontsize=16,
        ha="center",
        va="center",
        fontweight="bold",
        zorder=10,
        bbox=dict(
            boxstyle="round,pad=0.4",
            facecolor="#1e1e1e",
            edgecolor="#ffffff",
            alpha=0.85,
        ),
    )

    # Draw Heatmap
    if pitch_mode in ["Heatmap Only", "Combined Overlay"]:
        total_actions = int(
            p_data.get("Pass Total", 0)
            + p_data.get("Dribble Total", 0)
            + p_data.get("BallWon Total", 0)
        )
        sample_size = max(min(total_actions, 150), 40)
        hx = np.clip(
            np.random.normal(
                loc=(zone["x"][0] + zone["x"][1]) / 2,
                scale=12,
                size=sample_size,
            ),
            2,
            118,
        )
        hy = np.clip(
            np.random.normal(
                loc=(zone["y"][0] + zone["y"][1]) / 2,
                scale=10,
                size=sample_size,
            ),
            2,
            78,
        )
        alpha_val = 0.7 if pitch_mode == "Heatmap Only" else 0.45
        sns.kdeplot(
            x=hx,
            y=hy,
            ax=ax,
            fill=True,
            thresh=0.08,
            levels=15,
            cmap="YlOrRd",
            alpha=alpha_val,
            zorder=2,
        )

    # Draw Actions
    if pitch_mode in ["Action Map Only", "Combined Overlay"]:
        if show_passes:
            pass_success = p_data.get("Pass Success", 0)
            pass_total = p_data.get("Pass Total", 0)
            pass_failed = max(0, pass_total - pass_success)
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
                    color="#00ff66",
                    width=2,
                    headwidth=4,
                    headlength=4,
                    ax=ax,
                    label=f"Completed Pass ({int(pass_success)})",
                    zorder=4,
                )

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
                    color="#ff3333",
                    width=2,
                    headwidth=4,
                    headlength=4,
                    ax=ax,
                    label=f"Incomplete Pass ({int(pass_failed)})",
                    zorder=3,
                )

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
                    s=320,
                    color="#ffd700",
                    marker="*",
                    edgecolors="white",
                    linewidth=1.5,
                    ax=ax,
                    label=f"Goal Scored ({int(goals_cnt)})",
                    zorder=7,
                )

    ax.legend(
        facecolor="#1e1e1e",
        edgecolor="#ffffff",
        fontsize=10,
        labelcolor="white",
        loc="upper left",
    )
    st.pyplot(fig)
