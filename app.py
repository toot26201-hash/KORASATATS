import streamlit as st
import pandas as pd
import plotly.express as px

# ضبط إعدادات الصفحة
st.set_page_config(page_title="Players Data Maps", layout="wide")

st.title("⚽ لوحة تحليل وتوزيع اللاعبين (Data Maps)")

# 1. تحميل البيانات
@st.cache_data
def load_data():
    df = pd.read_csv("PlayersData_2215.csv")
    return df

df = load_data()

# القائمة الجانبية للتصفية (Sidebar Filters)
st.sidebar.header("فلترة البيانات")
teams = st.sidebar.multiselect("اختر الفريق:", options=df["Team"].dropna().unique(), default=df["Team"].dropna().unique()[:5])
positions = st.sidebar.multiselect("اختر المركز الرئيسي:", options=df["Primary Position"].dropna().unique(), default=df["Primary Position"].dropna().unique())

# تطبيق الفلترة
filtered_df = df[(df["Team"].isin(teams)) & (df["Primary Position"].isin(positions))]

# ---------------------------------------------------------
# Map 1: خريطة توزيع اللاعبين جغرافياً حسب الجنسية
# ---------------------------------------------------------
st.subheader("🌍 خريطة التوزيع الجغرافي للاعبين (حسب الجنسية)")

# تجميع البيانات حسب الدولة
geo_df = filtered_df.groupby("Nationality").agg(
    Total_Players=("ID", "count"),
    Total_Goals=("GoalsScored Total", "sum"),
    Total_Assists=("Chances Assists", "sum")
).reset_index()

metric_choice = st.radio("اختر المؤشر للعرض على الخريطة:", ["Total_Players", "Total_Goals", "Total_Assists"], horizontal=True)

fig_map = px.choropleth(
    geo_df,
    locations="Nationality",
    locationmode="country names",
    color=metric_choice,
    hover_name="Nationality",
    color_continuous_scale=px.colors.sequential.Plasma,
    title=f"توزيع {metric_choice} حسب الجنسية"
)

fig_map.update_layout(margin={"r":0,"t":40,"l":0,"b":0})
st.plotly_chart(fig_map, use_container_width=True)

# ---------------------------------------------------------
# Map 2: خريطة حرارية (Heatmap) للعلاقة بين المراكز والمؤشرات
# ---------------------------------------------------------
st.subheader("🔥 الخريطة الحرارية لأداء المراكز (Position Heatmap)")

heatmap_data = filtered_df.groupby("Primary Position")[
    ["GoalsScored Total", "Chances Assists", "Pass Accuracy", "BallWon Total", "Defensive Clear"]
].mean()

fig_heat = px.imshow(
    heatmap_data.T,
    labels=dict(x="المركز", y="المؤشر", color="المتوسط"),
    x=heatmap_data.index,
    y=heatmap_data.columns,
    aspect="auto",
    color_continuous_scale="Viridis",
    text_auto=".1f"
)

st.plotly_chart(fig_heat, use_container_width=True)

# عرض البيانات المفلترة
with st.expander("📄 عرض جدول البيانات المفلترة"):
    st.dataframe(filtered_df[['Full Name', 'Team', 'Primary Position', 'Nationality', 'GoalsScored Total', 'Chances Assists']])
