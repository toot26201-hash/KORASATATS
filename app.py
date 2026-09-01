import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

# ضبط إعدادات الصفحة
st.set_page_config(
    page_title="Football Player Action Map", layout="wide"
)

st.title("⚽ خريطة أحداث اللاعب التفصيلية على الملعب (Action Map)")

# ---------------------------------------------------------
# 1. رفع وتمرير الملفات
# ---------------------------------------------------------
st.sidebar.header("📁 رفع الملف والتحكم")
uploaded_file = st.sidebar.file_uploader(
    "قم برفع ملف البيانات (CSV):", type=["csv"]
)


@st.cache_data
def load_data(file):
    return pd.read_csv(file)


if uploaded_file is None:
    st.info(
        "👋 يرجى رفع ملف البيانات (`PlayersData_2215.csv`) من القائمة الجانبية لبدء عرض خريطة الأحداث."
    )
    st.stop()

df = load_data(uploaded_file)

# ---------------------------------------------------------
# 2. القائمة الجانبية وتحديد الأحداث المطلوب عرضها
# ---------------------------------------------------------
selected_team = st.sidebar.selectbox(
    "اختر الفريق:", sorted(df["Team"].dropna().unique())
)
team_players = df[df["Team"] == selected_team]

selected_player = st.sidebar.selectbox(
    "اختر اللاعب:", sorted(team_players["Full Name"].dropna().unique())
)
p_data = df[df["Full Name"] == selected_player].iloc[0]

st.sidebar.markdown("---")
st.sidebar.header("🎨 تصفية الأكشن والمؤشرات")

# تحديد تفعيل/إلغاء تفعيل أكشن معين على الملعب
show_goals = st.sidebar.checkbox("⚽ الأهداف (Goals)", value=True)
show_assists = st.sidebar.checkbox(
    "🔑 التمريرات المفتاحية/الحاسمة (Assists/Key Passes)", value=True
)
show_dribbles = st.sidebar.checkbox("⚡ المراوغات (Dribbles)", value=True)
show_ball_won = st.sidebar.checkbox(
    "🛡️ استعادة الكرة/الافتطاع (Tackles/Ball Won)", value=True
)
show_crosses = st.sidebar.checkbox("↗️ العرضيات (Crosses)", value=True)

# ---------------------------------------------------------
# 3. توزيـع الأحداث والأكشن بـرموز وألـوان علـى الملـعب
# ---------------------------------------------------------
# إحداثيات تمركز المجهود حسب المراكز
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

# توليد إحداثيات موزعة منطقياً داخل زون اللاعب بناءً على إحصائياته
np.random.seed(int(p_data["ID"]))


def generate_coords(count, x_range, y_range):
    if count <= 0 or pd.isna(count):
        return [], []
    # تحجيم الحد الأقصى للأكشن المعروض لتفادي ازدحام الخريطة
    display_count = min(int(count), 25)
    xs = np.random.uniform(x_range[0], x_range[1], display_count)
    ys = np.random.uniform(y_range[0], y_range[1], display_count)
    return xs, ys


# رسم الملعب التكتيكي
pitch = Pitch(
    pitch_type="statsbomb",
    pitch_color="#1e1e1e",
    line_color="#ffffff",
    stripe=True,
    stripe_color="#252525",
)
fig, ax = pitch.draw(figsize=(12, 8))

# 1. رسم الأهداف (Goals)
if show_goals:
    goals_cnt = p_data.get("GoalsScored Total", 0)
    # الأهداف تكون قريبة من منطقة الجزاء والمرمى
    gx, gy = generate_coords(
        goals_cnt, (max(zone["x"][0], 88), 116), (25, 55)
    )
    if len(gx) > 0:
        pitch.scatter(
            gx,
            gy,
            s=250,
            color="#e74c3c",
            marker="*",
            edgecolors="yellow",
            linewidth=1.5,
            ax=ax,
            label=f"هدف ({int(goals_cnt)})",
            zorder=5,
        )

# 2. رسم التمريرات الحاسمة / المفتاحية (Assists & Key Passes)
if show_assists:
    key_passes = p_data.get("Chances KeyPasses", 0) + p_data.get(
        "Chances Assists", 0
    )
    ax_x, ax_y = generate_coords(
        key_passes, (zone["x"][0], min(zone["x"][1] + 10, 110)), zone["y"]
    )
    if len(ax_x) > 0:
        pitch.scatter(
            ax_x,
            ax_y,
            s=180,
            color="#2ecc71",
            marker="P",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"تمريرة حاسمة/مفتاحية ({int(key_passes)})",
            zorder=4,
        )

# 3. رسم المراوغات (Successful Dribbles)
if show_dribbles:
    dribbles_cnt = p_data.get("Dribble Success", 0)
    dx, dy = generate_coords(dribbles_cnt, zone["x"], zone["y"])
    if len(dx) > 0:
        pitch.scatter(
            dx,
            dy,
            s=150,
            color="#f1c40f",
            marker="o",
            edgecolors="black",
            linewidth=1,
            ax=ax,
            label=f"مراوغة ناجحة ({int(dribbles_cnt)})",
            zorder=3,
        )

# 4. رسم افتطاع الكرة واستعادتها (Ball Won / Tackles)
if show_ball_won:
    tackles_cnt = p_data.get("BallWon Total", 0)
    bx, by = generate_coords(
        tackles_cnt, (max(zone["x"][0] - 15, 5), zone["x"][1]), zone["y"]
    )
    if len(bx) > 0:
        pitch.scatter(
            bx,
            by,
            s=160,
            color="#3498db",
            marker="s",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"استعادة كرة/افتطاع ({int(tackles_cnt)})",
            zorder=3,
        )

# 5. رسم العرضيات (Crosses)
if show_crosses:
    cross_cnt = p_data.get("Cross Success", 0)
    # العرضيات تكون غالبًا على أطراف الملعب
    side_y = (5, 25) if random.random() > 0.5 else (55, 75)
    cx, cy = generate_coords(
        cross_cnt, (max(zone["x"][0], 50), 105), side_y
    )
    if len(cx) > 0:
        pitch.scatter(
            cx,
            cy,
            s=170,
            color="#9b59b6",
            marker="^",
            edgecolors="white",
            linewidth=1,
            ax=ax,
            label=f"عرضية ناجحة ({int(cross_cnt)})",
            zorder=4,
        )

# إضافة دليل الألوان والرموز (Legend)
ax.legend(
    facecolor="#2b2b2b",
    edgecolor="white",
    fontsize=11,
    labelcolor="white",
    loc="upper left",
)

st.pyplot(fig)

# ---------------------------------------------------------
# 4. جدول ملخص الإحصائيات مع الألوان
# ---------------------------------------------------------
st.markdown("---")
st.subheader("📋 تفاصيل إحصائيات الأكشن للاعب")

col1, col2, col3, col4, col5 = st.columns(5)
col1.metric(
    "⚽ الأهداف",
    int(p_data.get("GoalsScored Total", 0)),
    help="رمز نجمة حمراء",
)
col2.metric(
    "🔑 التمريرات الحاسمة",
    int(p_data.get("Chances Assists", 0)),
    help="رمز + أخضر",
)
col3.metric(
    "⚡ المراوغات الناجحة",
    int(p_data.get("Dribble Success", 0)),
    help="دائرة صفراء",
)
col4.metric(
    "🛡️ استعادة الكرة",
    int(p_data.get("BallWon Total", 0)),
    help="مربع أزرق",
)
col5.metric(
    "↗️ العرضيات الناجحة",
    int(p_data.get("Cross Success", 0)),
    help="مثلث بنفسجي",
)
