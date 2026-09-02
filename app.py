import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
from mplsoccer import Pitch

# 1. إعدادات الصفحة
st.set_page_config(page_title="Cedric Ngah Analytics", layout="wide")

st.title("⚽ CEDRIC NGAH (Al Mosul SC) - Passing Map")

np.random.seed(88)

# 2. إعداد الملعب المظلم
pitch = Pitch(half=False, pitch_color="#000000", line_color="#ffffff")
fig, ax = pitch.draw(figsize=(13, 8.5))
fig.patch.set_facecolor("#000000")

# ---------------------------------------------------------
# 3. إحداثيات التمريرات (88 ناجحة + 24 خاطئة)
# ---------------------------------------------------------
num_completed = 88
num_incomp = 24

# التمريرات الناجحة (من منطقة قلب الدفاع CB)
pass_comp_x1 = np.clip(np.random.normal(30, 8, num_completed), 10, 50)
pass_comp_y1 = np.clip(np.random.normal(40, 14, num_completed), 10, 70)
pass_comp_x2 = np.clip(
    pass_comp_x1 + np.random.uniform(10, 35, num_completed), 15, 85
)
pass_comp_y2 = np.clip(
    pass_comp_y1 + np.random.uniform(-22, 22, num_completed), 5, 75
)

# رسم الـ 88 سهمًا بسمك نحيف (width=0.8) وشفافية (alpha=0.35) لإظهار التداخل والكثافة
pitch.arrows(
    pass_comp_x1,
    pass_comp_y1,
    pass_comp_x2,
    pass_comp_y2,
    color="#00ff66",
    width=0.8,
    headwidth=2.2,
    headlength=2.2,
    alpha=0.35,
    ax=ax,
    label=f"Completed Pass ({num_completed})",
    zorder=3,
)

# التمريرات الخاطئة (24 تمريرة)
pass_inc_x1 = np.clip(np.random.normal(28, 8, num_incomp), 10, 48)
pass_inc_y1 = np.clip(np.random.normal(40, 12, num_incomp), 10, 70)
pass_inc_x2 = np.clip(
    pass_inc_x1 + np.random.uniform(12, 40, num_incomp), 15, 95
)
pass_inc_y2 = np.clip(
    pass_inc_y1 + np.random.uniform(-28, 28, num_incomp), 5, 75
)

pitch.arrows(
    pass_inc_x1,
    pass_inc_y1,
    pass_inc_x2,
    pass_inc_y2,
    color="#ff3333",
    width=0.9,
    headwidth=2.4,
    headlength=2.4,
    alpha=0.6,
    ax=ax,
    label=f"Incomplete Pass ({num_incomp})",
    zorder=4,
)

# ---------------------------------------------------------
# 4. الأفعال الدفاعية (استعادة الكرة، التشتيت، الأخطاء)
# ---------------------------------------------------------

# Ball Recovery (42)
rec_x = np.clip(np.random.normal(25, 12, 42), 8, 55)
rec_y = np.clip(np.random.normal(40, 18, 42), 5, 75)
pitch.scatter(
    rec_x,
    rec_y,
    s=70,
    color="#00e5ff",
    marker="s",
    edgecolors="white",
    linewidth=0.6,
    alpha=0.85,
    ax=ax,
    label="Ball Recovery (42)",
    zorder=5,
)

# Clearance / Block (12)
clear_x = np.clip(np.random.normal(20, 8, 12), 6, 40)
clear_y = np.clip(np.random.normal(40, 16, 12), 8, 72)
pitch.scatter(
    clear_x,
    clear_y,
    s=90,
    color="#90a4ae",
    marker="D",
    edgecolors="white",
    linewidth=0.8,
    ax=ax,
    label="Clearance / Block (12)",
    zorder=5,
)

# Foul Committed (6)
pitch.scatter(
    np.random.uniform(20, 45, 6),
    np.random.uniform(15, 65, 6),
    s=120,
    color="#ff6d00",
    marker="h",
    edgecolors="white",
    ax=ax,
    label="Foul Committed (6)",
    zorder=5,
)

# Successful Dribble (1)
pitch.scatter(
    [38],
    [42],
    s=140,
    color="#ffea00",
    marker="o",
    edgecolors="black",
    ax=ax,
    label="Successful Dribble (1)",
    zorder=6,
)

# ---------------------------------------------------------
# 5. الشارات والـ Legend والعرض في Streamlit
# ---------------------------------------------------------
ax.text(
    60,
    92,
    "CEDRIC NGAH (Al Mosul SC) - CB",
    color="#ffffff",
    fontsize=13,
    ha="center",
    va="center",
    fontweight="bold",
    bbox=dict(
        boxstyle="round,pad=0.5", facecolor="#111111", edgecolor="#00ff66"
    ),
)

ax.legend(
    facecolor="#000000",
    edgecolor="#ffffff",
    fontsize=9.5,
    labelcolor="white",
    loc="upper left",
    framealpha=0.85,
)

# التغيير الجوهري لمنع الشاشة السوداء: استخدام st.pyplot بدلاً من plt.show
st.pyplot(fig)
