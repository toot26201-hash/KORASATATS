import os
import pandas as pd
import streamlit as st

# ---------------------------------------------------------
# تحميل البيانات المجمعة للاعبين
# ---------------------------------------------------------
@st.cache_data
def load_players_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "PlayersData_2215.csv")
    
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # بيانات افتراضية تجنباً لخطأ الشاشة السوداء في حال عدم وجود الملف
        return pd.DataFrame([
            {"Team Name": "Al Mosul SC", "Player Name": "Youssef Osama Nabih", "Position": "LW", "Shirt Number": 10},
            {"Team Name": "Al Mosul SC", "Player Name": "Ali Shakhowan Omar", "Position": "CM", "Shirt Number": 8},
            {"Team Name": "Al-Zawraa SC", "Player Name": "Hasan Abdulkareem", "Position": "AM", "Shirt Number": 10},
            {"Team Name": "Al-Zawraa SC", "Player Name": "Maicol Cabrera", "Position": "LW", "Shirt Number": 11},
        ])

df_players = load_players_data()

# ---------------------------------------------------------
# قسم اختيار الأندية واللاعبين في الـ Sidebar
# ---------------------------------------------------------
st.sidebar.header("📁 Data & Filter Controls")

# 1. قائمة اختيار النادي/الفريق
if "Team Name" in df_players.columns:
    teams_list = sorted(df_players["Team Name"].dropna().unique().tolist())
    selected_team = st.sidebar.selectbox("🏟️ Select Team (اختر النادي):", teams_list)
    
    # تصفية اللاعبين بناءً على النادي المختار
    filtered_team_df = df_players[df_players["Team Name"] == selected_team]
else:
    filtered_team_df = df_players
    selected_team = "Selected Team"

# 2. قائمة اختيار اللاعبين بناءً على النادي المختار
if "Player Name" in filtered_team_df.columns:
    players_list = sorted(filtered_team_df["Player Name"].dropna().unique().tolist())
    selected_player = st.sidebar.selectbox("👤 Select Player (اختر اللاعب):", players_list)
    
    # صف بيانات اللاعب المحدد
    player_data = filtered_team_df[filtered_team_df["Player Name"] == selected_player].iloc[0]
else:
    player_data = filtered_team_df.iloc[0]
    selected_player = "Player"

# 3. استخراج تفاصيل اللاعب الأساسية لاستخدامها في العنوان والخرائط
player_pos = player_data.get("Position", "LW")
player_num = player_data.get("Shirt Number", 10)

st.sidebar.markdown("---")
st.sidebar.subheader("📌 Selected Profile Info")
st.sidebar.write(f"**Name:** {selected_player}")
st.sidebar.write(f"**Team:** {selected_team}")
st.sidebar.write(f"**Position:** {player_pos} | **Number:** #{player_num}")
