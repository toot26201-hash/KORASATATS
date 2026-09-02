import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch

# 1. إعداد الملعب بالخلفية السوداء
pitch = Pitch(half=False, pitch_color='#000000', line_color='#ffffff')
fig, ax = pitch.draw(figsize=(14, 9.5))
fig.patch.set_facecolor('#000000')

# تثبيت العشوائية لضمان اتساق الإحداثيات عند إعادة التشغيل
np.random.seed(42)

# ---------------------------------------------------------
# 2. توليد وتجهيز إحداثيات كافة التمريرات (109 ناجحة + 16 خاطئة)
# ---------------------------------------------------------

# أ) التمريرات الناجحة بالكامل (Completed Passes = 109)
num_completed = 109
pass_comp_x1 = np.clip(np.random.normal(58, 12, num_completed), 20, 105)
pass_comp_y1 = np.clip(np.random.normal(40, 15, num_completed), 10, 70)
pass_comp_x2 = np.clip(
    pass_comp_x1 + np.random.uniform(-5, 25, num_completed), 10, 115
)
pass_comp_y2 = np.clip(
    pass_comp_y1 + np.random.uniform(-18, 18, num_completed), 5, 75
)

# رسم الـ 109 سهم للتمريرات الناجحة بسمك رفيع (width=1.1) وشفافية متوازنة (alpha=0.45)
pitch.arrows(
    pass_comp_x1,
    pass_comp_y1,
    pass_comp_x2,
    pass_comp_y2,
    color='#00ff66',
    width=1.1,
    headwidth=2.8,
    headlength=2.8,
    alpha=0.45,
    ax=ax,
    label=f'Completed Pass ({num_completed})',
    zorder=3,
)

# ب) التمريرات الخاطئة بالكامل (Incomplete Passes = 16)
num_incomp = 16
pass_inc_x1 = np.clip(np.random.normal(55, 10, num_incomp), 25, 95)
pass_inc_y1 = np.clip(np.random.normal(42, 14, num_incomp), 10, 70)
pass_inc_x2 = np.clip(
    pass_inc_x1 + np.random.uniform(5, 30, num_incomp), 15, 115
)
pass_inc_y2 = np.clip(
    pass_inc_y1 + np.random.uniform(-25, 25, num_incomp), 5, 75
)

# رسم الـ 16 سهم للتمريرات الخاطئة
pitch.arrows(
    pass_inc_x1,
    pass_inc_y1,
    pass_inc_x2,
    pass_inc_y2,
    color='#ff3333',
    width=1.2,
    headwidth=3.0,
    headlength=3.0,
    alpha=0.75,
    ax=ax,
    label=f'Incomplete Pass ({num_incomp})',
    zorder=4,
)

# ---------------------------------------------------------
# 3. الأفعال التكتيكية الأخرى (العرضيات، التمريرات الحاسمة، الاسترداد)
# ---------------------------------------------------------

# عرضية ناجحة (Completed Cross = 1)
pitch.scatter(
    [88],
    [15],
    s=200,
    color='#e040fb',
    marker='^',
    edgecolors='white',
    linewidth=1.5,
    ax=ax,
    label='Completed Cross (1)',
    zorder=6,
)

# تمريرة مفتاحية / حاسمة (Key Pass / Assist = 3)
kp_x = [82, 85, 86]
kp_y = [32, 56, 64]
pitch.scatter(
    kp_x,
    kp_y,
    s=240,
    color='#ff9100',
    marker='P',
    edgecolors='black',
    linewidth=1,
    ax=ax,
    label='Key Pass / Assist (3)',
    zorder=6,
)

# استعادة الكرة (Ball Recovery = 21)
num_recoveries = 21
rec_x = np.clip(np.random.normal(50, 16, num_recoveries), 15, 90)
rec_y = np.clip(np.random.normal(40, 18, num_recoveries), 8, 72)

pitch.scatter(
    rec_x,
    rec_y,
    s=110,
    color='#00e5ff',
    marker='s',
    edgecolors='white',
    linewidth=1,
    ax=ax,
    label=f'Ball Recovery ({num_recoveries})',
    zorder=5,
)

# ---------------------------------------------------------
# 4. الشارات والـ Legend
# ---------------------------------------------------------

# شارة الاسم والمركز أسفل الملعب
ax.text(
    60,
    92,
    'ALI SHAKHOWAN OMAR (Al Mosul SC) - CM',
    color='#ffffff',
    fontsize=14,
    ha='center',
    va='center',
    fontweight='bold',
    bbox=dict(
        boxstyle='round,pad=0.6', facecolor='#111111', edgecolor='#ffffff', alpha=0.9
    ),
)

# الـ Legend في أعلى اليسار
ax.legend(
    facecolor='#000000',
    edgecolor='#ffffff',
    fontsize=10,
    labelcolor='white',
    loc='upper left',
    framealpha=0.85,
)

plt.tight_layout()
plt.show()
