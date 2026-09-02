import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

# 1. إعدادات الصفحة
st.set_page_config(page_title="Tactical Analytics Dashboard", layout="wide")

# ---------------------------------------------------------
# 2. تحميل البيانات وتأمينها
# ---------------------------------------------------------
@st.cache_data
def load_players_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "PlayersData_2215.csv")

    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # بيانات افتراضية مؤمنة في حالة عدم وجود الملف
        return pd.DataFrame([
            {
                "Team Name": "Al Mosul SC",
                "Player Name": "Youssef Osama Nabih",
                "Position": "LW",
                "Shirt Number": 10,
                "Pass Success": 11,
                "Pass Fail": 4,
            },
            {
                "Team Name": "Al Mosul SC",
                "Player Name": "Ali Shakhowan Omar",
                "Position": "CM",
                "Shirt Number": 8,
                "Pass Success": 109,
                "Pass Fail": 16,
            },
            {
                "Team Name": "Al-Zawraa SC",
                "Player Name": "Hasan Abdulkareem",
                "Position": "AM",
                "Shirt Number": 10,
                "Pass Success": 45,
                "Pass Fail": 8,
            },
        ])


df_players = load_players_data()

# ---------------------------------------------------------
# 3. الـ Sidebar الاختيارات
# ---------------------------------------------------------
st.sidebar.header("📁 Data & Filter Controls")

# اختيار النادي
if "Team Name" in df_players.columns:
    teams_list = sorted(df_players["Team Name"].dropna().unique().tolist())
    selected_team = st.sidebar.selectbox(
        "🏟️ Select Team (اختر النادي):", teams_list
    )
    filtered_team_df = df_players[df_players["Team Name"] == selected_team]
else:
    filtered_team_df = df_players
    selected_team = "Al Mosul SC"

# اختيار اللاعب
if "Player Name" in filtered_team_df.columns:
    players_list = sorted(
        filtered_team_df["Player Name"].dropna().unique().tolist()
    )
    selected_player = st.sidebar.selectbox(
        "👤 Select Player (اختر اللاعب):", players_list
    )
    player_data = filtered_team_df[
        filtered_team_df["Player Name"] == selected_player
    ].iloc[0]
else:
    player_data = filtered_team_df.iloc[0]
    selected_player = "Youssef Osama Nabih"

player_pos = player_data.get("Position", "LW")
player_num = int(player_data.get("Shirt Number", 10))

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Selected Profile Info")
st.sidebar.write(f"**Name:** {selected_player}")
st.sidebar.write(f"**Team:** {selected_team}")
st.sidebar.write(f"**Position:** {player_pos} | **Number:** #{player_num}")

# ---------------------------------------------------------
# 4. رسم الملعب الرئيسي (Main Pitch View)
# ---------------------------------------------------------
st.title(f"⚽ {selected_player} - Tactical Passing Map")

np.random.seed(player_num)

pitch = Pitch(half=False, pitch_color="#000000", line_color="#ffffff")
fig, ax = pitch.draw(figsize=(13, 8.5))
fig.patch.set_facecolor("#000000")

# إحداثيات التمريرات
num_completed = int(player_data.get("Pass Success", 109))
num_incomp = int(player_data.get("Pass Fail", 16))

# رسم التمريرات الناجحة (Completed)
if num_completed > 0:
    pass_comp_x1 = np.clip(np.random.normal(62, 14, num_completed), 15, 105)
    pass_comp_y1 = np.clip(np.random.normal(38, 16, num_completed), 8, 72)
    pass_comp_x2 = np.clip(
        pass_comp_x1 + np.random.uniform(-5, 25, num_completed), 10, 115
    )
    pass_comp_y2 = np.clip(
        pass_comp_y1 + np.random.uniform(-18, 18, num_completed), 5, 75
    )

    pitch.arrows(
        pass_comp_x1,
        pass_comp_y1,
        pass_comp_x2,
        pass_comp_y2,
        color="#00ff66",
        width=1.1,
        headwidth=2.8,
        headlength=2.8,
        alpha=0.45,
        ax=ax,
        label=f"Completed Pass ({num_completed})",
        zorder=3,
    )

# رسم التمريرات الخاطئة (Incomplete)
if num_incomp > 0:
    pass_inc_x1 = np.clip(np.random.normal(58, 12, num_incomp), 20, 95)
    pass_inc_y1 = np.clip(np.random.normal(40, 15, num_incomp), 8, 72)
    pass_inc_x2 = np.clip(
        pass_inc_x1 + np.random.uniform(5, 30, num_incomp), 10, 115
    )
    pass_inc_y2 = np.clip(
        pass_inc_y1 + np.random.uniform(-22, 22, num_incomp), 5, 75
    )

    pitch.arrows(
        pass_inc_x1,
        pass_inc_y1,
        pass_inc_x2,
        pass_inc_y2,
        color="#ff3333",
        width=1.2,
        headwidth=3.0,
        headlength=3.0,
        alpha=0.75,
        ax=ax,
        label=f"Incomplete Pass ({num_incomp})",
        zorder=4,
    )

# العرضيات والكرة المباشرة
pitch.scatter(
    [88],
    [18],
    s=180,
    color="#e040fb",
    marker="^",
    edgecolors="white",
    ax=ax,
    label="Completed Cross (1)",
    zorder=5,
)
pitch.scatter(
    [82, 85],
    [32, 56],
    s=220,
    color="#ff9100",
    marker="P",
    edgecolors="black",
    ax=ax,
    label="Key Pass / Assist (2)",
    zorder=5,
)
pitch.scatter(
    np.random.uniform(30, 85, 6),
    np.random.uniform(10, 70, 6),
    s=110,
    color="#00e5ff",
    marker="s",
    edgecolors="white",
    ax=ax,
    label="Ball Recovery (6)",
    zorder=5,
)

# الشارات والمفتاح
ax.text(
    60,
    92,
    f"{selected_player} ({selected_team}) - {player_pos}",
    color="#ffffff",
    fontsize=14,
    ha="center",
    va="center",
    fontweight="bold",
    bbox=dict(
        boxstyle="round,pad=0.6", facecolor="#111111", edgecolor="#00ff66"
    ),
)

ax.legend(
    facecolor="#000000",
    edgecolor="#ffffff",
    fontsize=10,
    labelcolor="white",
    loc="upper left",
)

# عرض الملعب على Streamlit
st.pyplot(fig)
