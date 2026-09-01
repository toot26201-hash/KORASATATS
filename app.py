import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
from mplsoccer import Pitch, VerticalPitch

# ضبط إعدادات الصفحة
st.set_page_config(page_title="Football Pitch Data Maps", layout="wide")

st.title("⚽ خريطة أداء وإحصائيات اللاعبين على الملعب (Pitch Map)")

# ---------------------------------------------------------
# 1. مكان رفع الملفات
# ---------------------------------------------------------
st.sidebar.header("📁 بيانات اللاعبين")
uploaded_file = st.sidebar.file_uploader("قم برفع ملف البيانات (CSV):", type=["csv"])

@st.cache_data
def load_data(file):
    return pd.read_csv(file)

if uploaded_file is None:
    st.info("👋 يرجى رفع ملف البيانات (`PlayersData_2215.csv`) من القائمة الجانبية لبدء التحليل.")
    st.stop()

df = load_data(uploaded_file)

# ---------------------------------------------------------
# 2. فلاتر اختيار اللاعبين والمؤشرات
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🔍 إعدادات الخريطة والتمركؤ")

# اختيار الفريق واللاعب
selected_team = st.sidebar.selectbox("اختر الفريق:", sorted(df["Team"].dropna().unique()))
team_players = df[df["Team"] == selected_team]

selected_player = st.sidebar.selectbox("اختر اللاعب:", sorted(team_players["Full Name"].dropna().unique()))
player_data = df[df["Full Name"] == selected_player].iloc[0]

# إظهار بطاقة معلومات اللاعب السريعة
st.sidebar.markdown("---")
st.sidebar.write(f"**المركز:** {player_data['Primary Position']}")
st.sidebar.write(f"**رقم القميص:** {player_data['Number']}")
st.sidebar.write(f"**الدقائق الملعوبة:** {player_data['Admin MinutesPlayed']}")

# ---------------------------------------------------------
# 3. عرض إحصائيات اللاعب الرئيسية على الملعب التكتيكي
# ---------------------------------------------------------
st.subheader(f"📊 الخريطة التكتيكية والإحصائية على الملعب: {player_data['Full Name']}")

# إنشاء تخطيط الملعب باستخدام mplsoccer
pitch = Pitch(pitch_type='statsbomb', pitch_color='#22312b', line_color='#c7d5cc')
fig, ax = pitch.draw(figsize=(10, 7))

# تعيين موقع تقديري على الملعب حسب مركز اللاعب الرئيسي (Primary Position)
pos_coords = {
    'GK': (10, 40),
    'CB': (30, 40), 'LCB': (30, 25), 'RCB': (30, 55),
    'LB': (40, 10), 'RB': (40, 70), 'LWB': (50, 10), 'RWB': (50, 70),
    'DM': (50, 40), 'CDM': (50, 40),
    'CM': (65, 40), 'LCM': (65, 25), 'RCM': (65, 55),
    'AM': (80, 40), 'CAM': (80, 40), 'LM': (75, 15), 'RM': (75, 65),
    'LW': (95, 15), 'RW': (95, 65),
    'CF': (105, 40), 'ST': (105, 40)
}

# الحصول على الإحداثيات التقريبية للمركز
pos = player_data['Primary Position']
x, y = pos_coords.get(pos, (60, 40))

# رسم دائرة تمثل مركز اللاعب
pitch.scatter(x, y, s=600, color='#e74c3c', edgecolors='white', linewidth=2, ax=ax, zorder=3)

# إضافة نص اسم اللاعب وركمه
ax.text(x, y, str(int(player_data['Number'])), color='white', fontsize=12, ha='center', va='center', fontweight='bold', zorder=4)

# تجهيز نصوص الإحصائيات لعرضها في مناطق الملعب المختلفة
stat_text = (
    f"🏆 الأهداف: {player_data.get('GoalsScored Total', 0)}\n"
    f"🅰️ التمريرات الحاسمة: {player_data.get('Chances Assists', 0)}\n"
    f"🎯 دقة التمرير: {player_data.get('Pass Accuracy', 0)*100:.1f}%\n"
    f"⚡ المراوغات الناجحة: {player_data.get('Dribble Success', 0)}\n"
    f"🛡️ استعادة الكرة: {player_data.get('BallWon Total', 0)}"
)

# عرض صندوق الإحصائيات على الملعب
ax.text(
    x, y - 12, stat_text,
    color='black', fontsize=11, ha='center', va='top',
    bbox=dict(boxstyle='round,pad=0.5', facecolor='#ffffff', alpha=0.85, edgecolor='#e74c3c'),
    zorder=5
)

st.pyplot(fig)

# ---------------------------------------------------------
# 4. مقارنة خطوط وزوايا الملعب (الخريطة الحرارية للمراكز)
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📌 توزيع إحصائيات الفريق كاملاً على مراكز الملعب")

# عرض خريطة الملعب مع توزيع جميع لاعبي الفريق المختار
fig2, ax2 = pitch.draw(figsize=(12, 8))

for idx, p in team_players.iterrows():
    p_pos = p['Primary Position']
    px, py = pos_coords.get(p_pos, (60, 40))
    
    # رسم كل لاعب في الفريق
    pitch.scatter(px, py, s=450, color='#3498db', edgecolors='white', linewidth=1.5, ax=ax2, zorder=3)
    ax2.text(px, py, str(int(p['Number'])), color='white', fontsize=10, ha='center', va='center', fontweight='bold', zorder=4)
    ax2.text(px, py + 4, str(p['Nickname'] if pd.notna(p['Nickname']) else p['Full Name'].split()[0]), 
             color='white', fontsize=9, ha='center', va='bottom', zorder=4)

st.pyplot(fig2)
