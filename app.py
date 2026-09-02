import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
from mplsoccer import Pitch

# Page Setup
st.set_page_config(
    page_title="Individual Player Analytics",
    layout="wide",
)

st.title("⚽ Individual Player Analytics Dashboard")

# Create Dummy Data if File Not Found to Avoid Blank Screen
@st.cache_data
def get_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "PlayersData_2215.csv")
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        # Fallback Data Frame
        return pd.DataFrame({
            "Player Name": ["Youssef Osama Nabih"],
            "Team Name": ["Al Mosul SC"],
            "Shirt Number": [10],
            "Position": ["LW"],
            "Minutes Played": [90],
            "Avg X": [85],
            "Avg Y": [35],
            "Goals": [1],
            "Key Passes": [1],
            "Pass Accuracy": [73.3],
            "Dribbles Success": [1],
            "Recoveries": [6],
            "Total Actions": [15]
        })

df_players = get_data()

# Player Selection
player_data = df_players.iloc[0]
selected_player_name = player_data.get("Player Name", "Youssef Osama Nabih")

st.sidebar.header("🎯 Settings")
st.sidebar.markdown(f"**Player:** {selected_player_name}")

# Draw Pitch
pitch = Pitch(half=False, pitch_color="#000000", line_color="#ffffff")
fig, ax = pitch.draw(figsize=(10, 6))
fig.patch.set_facecolor("#000000")

# Draw Sample Action
pitch.scatter(85, 35, s=300, color="#00ff66", edgecolors="white", ax=ax)
ax.text(85, 35, str(int(player_data.get("Shirt Number", 10))), color="black", ha="center", va="center", fontweight="bold")

ax.text(60, 92, f"{selected_player_name} - Performance Card", color="#ffffff", fontsize=12, ha="center", va="center", fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.5", facecolor="#111111", edgecolor="#00ff66"))

st.pyplot(fig)
