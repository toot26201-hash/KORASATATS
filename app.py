import matplotlib.pyplot as plt
import numpy as np
from mplsoccer import Pitch

# 1. إعداد الملعب بالخلفية السوداء
pitch = Pitch(half=False, pitch_color='#000000', line_color='#ffffff')
fig, ax = pitch.draw(figsize=(14, 9.5))
fig.patch.set_facecolor('#000000')

# ---------------------------------------------------------
# 2. بيانات التمريرات والعرضيات واستعادة الكرة
# ---------------------------------------------------------

# التمريرات الناجحة (Completed Pass - 11)
pass_completed_x1 = [65, 70, 72, 75, 78, 80, 82, 85, 88, 92, 98]
pass_completed_y1 = [20, 25, 38, 15, 30, 42, 28, 35, 18, 48, 45]
pass_completed_x2 = [82, 95, 92, 98, 96, 102, 100, 105, 112, 108, 114]
pass_completed_y2 = [18, 22, 28, 12, 26, 36, 16, 28, 14, 42, 43]

pitch.arrows(
    pass_completed_x1,
    pass_completed_y1,
    pass_completed_x2,
    pass_completed_y2,
    color='#00ff66',
    width=2,
    headwidth=3.5,
    headlength=3.5,
    ax=ax,
    label='Completed Pass (11)',
)

# التمريرات الخاطئة (Incomplete Pass - 4)
pass_incomp_x1 = [70, 78, 95, 96]
pass_incomp_y1 = [28, 26, 32, 50]
pass_incomp_x2 = [92, 102, 108, 105]
pass_incomp_y2 = [20, 24, 28, 70]

pitch.arrows(
    pass_incomp_x1,
    pass_incomp_y1,
    pass_incomp_x2,
    pass_incomp_y2,
    color='#ff3333',
    width=2,
    headwidth=3.5,
    headlength=3.5,
    ax=ax,
    label='Incomplete Pass (4)',
)

# عرضية ناجحة (Completed Cross - 1)
pitch.scatter(
    [95],
    [30],
    s=180,
    color='#e040fb',
    marker='^',
    edgecolors='white',
    linewidth=1.5,
    ax=ax,
    label='Completed Cross (1)',
    zorder=5,
)

# تمريرة مفتاحية / حاسمة (Key Pass / Assist - 1)
pitch.scatter(
    [80],
    [52],
    s=220,
    color='#ff9100',
    marker='P',
    edgecolors='black',
    linewidth=1,
    ax=ax,
    label='Key Pass / Assist (1)',
    zorder=5,
)

# مراوغة ناجحة (Successful Dribble - 1)
pitch.scatter(
    [100],
    [40],
    s=160,
    color='#ffea00',
    marker='o',
    edgecolors='black',
    ax=ax,
    label='Successful Dribble (1)',
    zorder=5,
)

# استعادة الكرة (Ball Recovery - 6)
recovery_x = [58, 68, 79, 82, 92, 102]
recovery_y = [42, 22, 35, 56, 22, 22]

pitch.scatter(
    recovery_x,
    recovery_y,
    s=130,
    color='#00e5ff',
    marker='s',
    edgecolors='white',
    linewidth=1,
    ax=ax,
    label='Ball Recovery (6)',
    zorder=5,
)

# خطأ مرتكب (Foul Committed - 1)
pitch.scatter(
    [90],
    [18],
    s=180,
    color='#ff6d00',
    marker='h',
    edgecolors='white',
    linewidth=1,
    ax=ax,
    label='Foul Committed (1)',
    zorder=5,
)

# ---------------------------------------------------------
# 3. الالتحامات الأرضية والهوائية (Ground & Aerial Duels)
# ---------------------------------------------------------

# التحام أرضي ناجح (Ground Duel Won - 3)
pitch.scatter(
    [72, 86, 94],
    [32, 45, 25],
    s=160,
    color='#00e676',
    marker='D',
    edgecolors='white',
    linewidth=1,
    ax=ax,
    label='Ground Duel Won (3)',
    zorder=5,
)

# التحام أرضي مخفق (Ground Duel Lost - 2)
pitch.scatter(
    [76, 88],
    [50, 38],
    s=140,
    color='#ff1744',
    marker='D',
    edgecolors='black',
    linewidth=1,
    ax=ax,
    label='Ground Duel Lost (2)',
    zorder=5,
)

# التحام هوائي ناجح (Aerial Duel Won - 2)
pitch.scatter(
    [85, 104],
    [30, 48],
    s=180,
    color='#00b0ff',
    marker='*',
    edgecolors='white',
    linewidth=1,
    ax=ax,
    label='Aerial Duel Won (2)',
    zorder=5,
)

# ---------------------------------------------------------
# 4. التسديدات الهجومية وقيم الأهداف المتوقعة (Shots & xG)
# ---------------------------------------------------------

# تسديدة مسجلة هدف (Goal - 1) [xG: 0.32]
goal_x, goal_y, goal_xg = 104, 38, 0.32
pitch.scatter(
    [goal_x],
    [goal_y],
    s=380,
    color='#ffd700',
    marker='*',
    edgecolors='white',
    linewidth=1.5,
    ax=ax,
    label=f'Goal (xG: {goal_xg})',
    zorder=7,
)
ax.text(
    goal_x,
    goal_y - 4,
    f'Goal ({goal_xg} xG)',
    color='#ffd700',
    fontsize=9,
    ha='center',
    fontweight='bold',
    zorder=8,
)

# تسديدة بين القائمين والعارضة (Shot On Target - 1) [xG: 0.14]
shot_on_x, shot_on_y, shot_on_xg = 96, 26, 0.14
pitch.scatter(
    [shot_on_x],
    [shot_on_y],
    s=180,
    color='#00ff66',
    marker='o',
    edgecolors='black',
    linewidth=1,
    ax=ax,
    label=f'Shot On Target (xG: {shot_on_xg})',
    zorder=6,
)

# تسديدة خارج المرمى (Shot Off Target - 1) [xG: 0.06]
shot_off_x, shot_off_y, shot_off_xg = 88, 52, 0.06
pitch.scatter(
    [shot_off_x],
    [shot_off_y],
    s=150,
    color='#ff1744',
    marker='x',
    linewidth=2,
    ax=ax,
    label=f'Shot Off Target (xG: {shot_off_xg})',
    zorder=6,
)

# ---------------------------------------------------------
# 5. الشارات والـ Legend
# ---------------------------------------------------------

# شارة التلخيص والبطاقة بأسفل الملعب
ax.text(
    60,
    92,
    'YOUSSEF OSAMA NABIH (Al Mosul SC) - LW\nTotal xG: 0.52 | Goals: 1 | Key Passes: 1 | Duels Won: 5/8',
    color='#ffffff',
    fontsize=13,
    ha='center',
    va='center',
    fontweight='bold',
    bbox=dict(
        boxstyle='round,pad=0.6', facecolor='#111111', edgecolor='#00ff66', alpha=0.95
    ),
)

# قائمة الرموز Legend في أعلى اليسار
ax.legend(
    facecolor='#000000',
    edgecolor='#ffffff',
    fontsize=9,
    labelcolor='white',
    loc='upper left',
    framealpha=0.85,
)

plt.tight_layout()
plt.show()
