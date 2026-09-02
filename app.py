import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

# 1. إعدادات الصفحة
st.set_page_config(
    page_title="TootScouting - Universal Player Dashboard", layout="wide"
)

st.title("⚽ Universal Player Tactical & Spatial Analytics")

# ---------------------------------------------------------
# 2. قراءة بيانات جميع اللاعبين ديناميكياً
# ---------------------------------------------------------
@st.cache_data
def load_all_players():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "PlayersData_2215.csv")

    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # بيانات نمطية مؤمنة كبديل في حال عدم رفع الملف
        return pd.DataFrame([
            {
                "Team Name": "Al Mosul SC",
                "Player Name": "Youssef Osama Nabih",
                "Position": "LW",
                "Shirt Number": 10,
                "Pass Success": 11,
                "Pass Fail": 4,
                "Recoveries": 6,
                "Key Passes": 1,
            },
            {
                "Team Name": "Al Mosul SC",
                "Player Name": "Ali Shakhowan Omar",
                "Position": "CM",
                "Shirt Number": 8,
                "Pass Success": 109,
                "Pass Fail": 16,
                "Recoveries": 21,
                "Key Passes": 3,
            },
            {
                "Team Name": "Al Mosul SC",
                "Player Name": "Cedric Ngah",
                "Position": "CB",
                "Shirt Number": 4,
                "Pass Success": 88,
                "Pass Fail": 24,
                "Recoveries": 42,
                "Key Passes": 0,
            },
            {
                "Team Name": "Al-Zawraa SC",
                "Player Name": "Hasan Abdulkareem",
                "Position": "AM",
                "Shirt Number": 10,
                "Pass Success": 45,
                "Pass Fail": 8,
                "Recoveries": 12,
                "Key Passes": 4,
            },
        ])

df_players = load_all_players()

# ---------------------------------------------------------
# 3. الـ Sidebar - اختيار أي نادي وأي لاعب ديناميكياً
# ---------------------------------------------------------
st.sidebar.header("📁 Data & Filter Controls")

# اختيار النادي
if "Team Name" in df_players.columns:
    teams_list = sorted(df_players["Team Name"].dropna().unique().tolist())
    selected_team = st.sidebar.selectbox("🏟️ Select Team (اختر النادي):", teams_list)
    filtered_team_df = df_players[df_players["Team Name"] == selected_team]
else:
    filtered_team_df = df_players
    selected_team = "Selected Team"

# اختيار اللاعب
if "Player Name" in filtered_team_df.columns:
    players_list = sorted(filtered_team_df["Player Name"].dropna().unique().tolist())
    selected_player = st.sidebar.selectbox("👤 Select Player (اختر اللاعب):", players_list)
    player_data = filtered_team_df[filtered_team_df["Player Name"] == selected_player].iloc[0]
else:
    player_data = filtered_team_df.iloc[0]
    selected_player = "Selected Player"

# استخراج خصائص اللاعب المحدد ديناميكياً
player_pos = str(player_data.get("Position", "CM"))
player_num = int(player_data.get("Shirt Number", player_data.get("Number", 10)))
num_completed = int(player_data.get("Pass Success", player_data.get("Completed Passes", 30)))
num_incomp = int(player_data.get("Pass Fail", player_data.get("Incomplete Passes", 5)))
num_recoveries = int(player_data.get("Recoveries", player_data.get("Ball Recoveries", 6)))
num_key_passes = int(player_data.get("Key Passes", 1))

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Selected Profile Info")
st.sidebar.write(f"**Name:** {selected_player}")
st.sidebar.write(f"**Team:** {selected_team}")
st.sidebar.write(f"**Position:** {player_pos} | **Number:** #{player_num}")
st.sidebar.write(f"**Completed Passes:** {num_completed}")
st.sidebar.write(f"**Incomplete Passes:** {num_incomp}")

# ---------------------------------------------------------
# 4. محرك الرسم التكتيكي الديناميكي لكل لاعب
# ---------------------------------------------------------
np.random.seed(player_num)

pitch = Pitch(half=False, pitch_color="#000000", line_color="#ffffff")
fig, ax = pitch.draw(figsize=(13, 8.5))
fig.patch.set_facecolor("#000000")

# تحديد النطاق المكاني الافتراضي للتمرير حسب مركز اللاعب (CB / CM / LW / ST)
if "CB" in player_pos or "RB" in player_pos or "LB" in player_pos:
    base_x, spread_x = 32, 12
    base_y, spread_y = 40, 20
elif "CM" in player_pos or "DM" in player_pos or "AM" in player_pos:
    base_x, spread_x = 58, 16
    base_y, spread_y = 40, 18
else:  # LW / RW / ST
    base_x, spread_x = 82, 14
    base_y, spread_y = 35, 22

# أ) رسم التمريرات الناجحة (Completed Passes)
if num_completed > 0:
    pass_comp_x1 = np.clip(np.random.normal(base_x, spread_x, num_completed), 10, 105)
    pass_comp_y1 = np.clip(np.random.normal(base_y, spread_y, num_completed), 8, 72)
    pass_comp_x2 = np.clip(pass_comp_x1 + np.random.uniform(-5, 30, num_completed), 10, 115)
    pass_comp_y2 = np.clip(pass_comp_y1 + np.random.uniform(-20, 20, num_completed), 5, 75)

    # لضبط التداخل عند كثرة التمريرات: تقليل السمك والشفافية مع الأعداد الكبيرة
    arrow_width = 0.8 if num_completed > 50 else 1.4
    arrow_alpha = 0.35 if num_completed > 50 else 0.65

    pitch.arrows(
        pass_comp_x1, pass_comp_y1, pass_comp_x2, pass_comp_y2,
        color="#00ff66", width=arrow_width, headwidth=2.5, headlength=2.5,
        alpha=arrow_alpha, ax=ax, label=f"Completed Pass ({num_completed})", zorder=3
    )

# ب) رسم التمريرات الخاطئة (Incomplete Passes)
if num_incomp > 0:
    pass_inc_x1 = np.clip(np.random.normal(base_x - 5, spread_x, num_incomp), 10, 95)
    pass_inc_y1 = np.clip(np.random.normal(base_y, spread_y, num_incomp), 8, 72)
    pass_inc_x2 = np.clip(pass_inc_x1 + np.random.uniform(5, 30, num_incomp), 10, 115)
    pass_inc_y2 = np.clip(pass_inc_y1 + np.random.uniform(-25, 25, num_incomp), 5, 75)

    pitch.arrows(
        pass_inc_x1, pass_inc_y1, pass_inc_x2, pass_inc_y2,
        color="#ff3333", width=0.9, headwidth=2.5, headlength=2.5,
        alpha=0.6, ax=ax, label=f"Incomplete Pass ({num_incomp})", zorder=4
    )

# ج) استعادة الكرة (Ball Recoveries)
if num_recoveries > 0:
    rec_x = np.clip(np.random.normal(base_x - 10, spread_x, num_recoveries), 8, 95)
    rec_y = np.clip(np.random.normal(base_y, spread_y, num_recoveries), 5, 75)
    pitch.scatter(
        rec_x, rec_y, s=80, color="#00e5ff", marker="s", edgecolors="white",
        linewidth=0.6, alpha=0.8, ax=ax, label=f"Ball Recovery ({num_recoveries})", zorder=5
    )

# د) التمريرات المفتاحية (Key Passes)
if num_key_passes > 0:
    kp_x = np.random.uniform(65, 95, num_key_passes)
    kp_y = np.random.uniform(15, 65, num_key_passes)
    pitch.scatter(
        kp_x, kp_y, s=220, color="#ff9100", marker="P", edgecolors="black",
        ax=ax, label=f"Key Pass / Assist ({num_key_passes})", zorder=6
    )

# ---------------------------------------------------------
# 5. الشارات والـ Legend والعرض المباشر
# ---------------------------------------------------------
ax.text(
    60, 92, f"{selected_player} ({selected_team}) - {player_pos}",
    color="#ffffff", fontsize=14, ha="center", va="center", fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.6", facecolor="#111111", edgecolor="#00ff66", alpha=0.95)
)

ax.legend(
    facecolor="#000000", edgecolor="#ffffff", fontsize=10, labelcolor="white",
    loc="upper left", framealpha=0.85
)

# عرض الرسم المباشر في Streamlit بدلاً من plt.show()
st.pyplot(fig)
