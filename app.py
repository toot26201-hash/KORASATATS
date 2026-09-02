import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

# 1. إعداد الصفحة
st.set_page_config(page_title="Tactical Analytics", layout="wide")

st.title("⚽ Tactical Analytics Dashboard")

# 2. تحميل البيانات بأمان بدون توقف
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "PlayersData_2215.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # بيانات احتياطية لضمان عمل الواجهة وعدم اختفائها
        return pd.DataFrame({
            "Player Name": ["ALI SHAKHOWAN OMAR"],
            "Team Name": ["Al Mosul SC"],
            "Position": ["CM"]
        })

df = load_data()

# 3. القائمة الجانبية
st.sidebar.header("🎯 Player Selection")
player_name = df["Player Name"].iloc[0]
st.sidebar.markdown(f"**Selected Player:** {player_name}")

# 4. رسم الملعب
np.random.seed(42)
pitch = Pitch(half=False, pitch_color="#000000", line_color="#ffffff")
fig, ax = pitch.draw(figsize=(12, 7.5))
fig.patch.set_facecolor("#000000")

# رسم كرات وتمريرات نموذجية
num_completed = 109
pass_comp_x1 = np.clip(np.random.normal(58, 12, num_completed), 20, 105)
pass_comp_y1 = np.clip(np.random.normal(40, 15, num_completed), 10, 70)
pass_comp_x2 = np.clip(pass_comp_x1 + np.random.uniform(-5, 25, num_completed), 10, 115)
pass_comp_y2 = np.clip(pass_comp_y1 + np.random.uniform(-18, 18, num_completed), 5, 75)

pitch.arrows(
    pass_comp_x1, pass_comp_y1, pass_comp_x2, pass_comp_y2,
    color="#00ff66", width=1.1, headwidth=2.8, headlength=2.8, alpha=0.45,
    ax=ax, label=f"Completed Pass ({num_completed})"
)

ax.text(
    60, 92, f"{player_name} (Al Mosul SC) - CM",
    color="#ffffff", fontsize=13, ha="center", va="center", fontweight="bold",
    bbox=dict(boxstyle="round,pad=0.5", facecolor="#111111", edgecolor="#00ff66")
)

ax.legend(facecolor="#000000", edgecolor="#ffffff", fontsize=9, labelcolor="white", loc="upper left")

# عرض الرسم المباشر في Streamlit
st.pyplot(fig)
