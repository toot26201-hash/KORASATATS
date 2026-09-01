import os
import pandas as pd
import plotly.express as px
import streamlit as st

# ضبط إعدادات الصفحة
st.set_page_config(page_title="Players Data Maps", layout="wide")

st.title("⚽ لوحة تحليل وتوزيع اللاعبين (Data Maps)")

# ---------------------------------------------------------
# 1. مكان رفع الملفات في القائمة الجانبية (File Uploader)
# ---------------------------------------------------------
st.sidebar.header("📁 رفع بيانات جديد")
uploaded_file = st.sidebar.file_uploader(
    "قم برفع ملف البيانات (CSV):", type=["csv"]
)


@st.cache_data
def load_data_from_file(file):
    return pd.read_csv(file)


# تحديد مصدر البيانات (إما المرفوع الآن أو الملف المرفوع سابقاً على الخادم)
df = None

if uploaded_file is not None:
    # استخدام الملف المرفوع من قبل المستخدم
    df = load_data_from_file(uploaded_file)
    st.sidebar.success("✅ تم تحميل الملف المرفوع بنجاح!")
else:
    # المحاولة الثانية: قراءة الملف الافتراضي من مجلد التطبيق
    base_dir = os.path.dirname(os.path.abspath(__file__))
    default_file_path = os.path.join(base_dir, "PlayersData_2215.csv")

    if os.path.exists(default_file_path):
        df = pd.read_csv(default_file_path)
    else:
        st.info(
            "👋 مرحباً بك! يرجى رفع ملف البيانات (`PlayersData_2215.csv`) من القائمة الجانبية لبدء التحليل لعرض الخرائط."
        )
        st.stop()

# ---------------------------------------------------------
# 2. الفلاتر والتحليلات (تعمل تلقائياً عند وجود بيانات)
# ---------------------------------------------------------
st.sidebar.markdown("---")
st.sidebar.header("🔍 فلترة البيانات")

# اختيار الفرق
available_teams = sorted(df["Team"].dropna().unique())
teams = st.sidebar.multiselect(
    "اختر الفريق:", options=available_teams, default=available_teams[:5]
)

# اختيار المراكز
available_positions = sorted(df["Primary Position"].dropna().unique())
positions = st.sidebar.multiselect(
    "اختر المركز الرئيسي:",
    options=available_positions,
    default=available_positions,
)

# تطبيق الفلترة
filtered_df = df[
    (df["Team"].isin(teams)) & (df["Primary Position"].isin(positions))
]

if filtered_df.empty:
    st.warning("⚠️ لا توجد بيانات تتطابق مع الخيارات المحددة في الفلتر.")
else:
    # ---------------------------------------------------------
    # Map 1: خريطة توزيع اللاعبين جغرافياً حسب الجنسية (Choropleth Map)
    # ---------------------------------------------------------
    st.subheader("🌍 خريطة التوزيع الجغرافي للاعبين (حسب الجنسية)")

    # تجميع البيانات حسب الدولة
    geo_df = (
        filtered_df.groupby("Nationality")
        .agg(
            Total_Players=("ID", "count"),
            Total_Goals=("GoalsScored Total", "sum"),
            Total_Assists=("Chances Assists", "sum"),
        )
        .reset_index()
    )

    metric_choice = st.radio(
        "اختر المؤشر للعرض على الخريطة:",
        ["Total_Players", "Total_Goals", "Total_Assists"],
        horizontal=True,
    )

    fig_map = px.choropleth(
        geo_df,
        locations="Nationality",
        locationmode="country names",
        color=metric_choice,
        hover_name="Nationality",
        color_continuous_scale=px.colors.sequential.Plasma,
        title=f"توزيع {metric_choice} حسب الجنسية",
    )

    fig_map.update_layout(margin={"r": 0, "t": 40, "l": 0, "b": 0})
    st.plotly_chart(fig_map, use_container_width=True)

    # ---------------------------------------------------------
    # Map 2: خريطة حرارية (Heatmap) لأداء المراكز
    # ---------------------------------------------------------
    st.subheader("🔥 الخريطة الحرارية لأداء المراكز (Position Heatmap)")

    metrics_list = [
        "GoalsScored Total",
        "Chances Assists",
        "Pass Accuracy",
        "BallWon Total",
        "Defensive Clear",
    ]
    heatmap_data = filtered_df.groupby("Primary Position")[metrics_list].mean()

    fig_heat = px.imshow(
        heatmap_data.T,
        labels=dict(x="المركز", y="المؤشر", color="المتوسط"),
        x=heatmap_data.index,
        y=heatmap_data.columns,
        aspect="auto",
        color_continuous_scale="Viridis",
        text_auto=".1f",
    )

    st.plotly_chart(fig_heat, use_container_width=True)

    # عرض جدول البيانات المفلترة
    with st.expander("📄 عرض جدول البيانات"):
        cols_to_show = [
            "Full Name",
            "Team",
            "Primary Position",
            "Nationality",
            "GoalsScored Total",
            "Chances Assists",
        ]
        st.dataframe(filtered_df[cols_to_show])
