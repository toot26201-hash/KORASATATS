import plotly.express as px
import pandas as pd
import streamlit as st

# قراءة ملف الفريق
team_df = pd.read_csv("Data_2215.csv")
team_data = team_df.iloc[0]

st.header(f"🛡️ Team Performance Overview: {team_data['Team Name']}")

# 1. عرض بطاقات الـ KPIs الرئيسية
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)
kpi1.metric("Matches Played", team_data["Admin MatchesPlayed"])
kpi2.metric(
    "Record (W-D-L)",
    f"{team_data['Admin Win']}-{team_data['Admin Draw']}-{team_data['Admin Lost']}",
)
kpi3.metric(
    "Goals (Scored/Conceded)",
    f"{team_data['GoalsScored Total']} / {team_data['GoalsConceded Total']}",
)
kpi4.metric("Expected Goals (xG)", team_data["GoalsScored XG"])
kpi5.metric(
    "Avg Possession",
    f"{team_data['Possession_TimePercent Average']*100:.1f}%",
)

st.markdown("---")

# 2. رسم بياني لتغير الاستحواذ عبر فترات اللقاء (15-min Intervals)
st.subheader("⏱️ Possession & Dominance Timeline")

pos_intervals = {
    "0-15m": team_data["Possession_TimePercent T_0_15"] * 100,
    "15-30m": team_data["Possession_TimePercent T_15_30"] * 100,
    "30-45m": team_data["Possession_TimePercent T_30_45"] * 100,
    "45-60m": team_data["Possession_TimePercent T_45_60"] * 100,
    "60-75m": team_data["Possession_TimePercent T_60_75"] * 100,
    "75-90m": team_data["Possession_TimePercent T_75_90"] * 100,
}

pos_df = pd.DataFrame(
    list(pos_intervals.items()), columns=["Interval", "Possession %"]
)
fig_pos = px.line(
    pos_df,
    x="Interval",
    y="Possession %",
    markers=True,
    title="Possession Percentage Across Match Intervals",
)
fig_pos.update_traces(line_color="#00e676", line_width=3)
st.plotly_chart(fig_pos, use_container_width=True)

# 3. توزيع أساليب استعادة الكرة (Defensive Recoveries)
st.subheader("🛡️ Ball Recovery & Defensive Actions")
rec_data = {
    "Ball Recoveries": team_data["BallWon BallRecover"],
    "Interceptions": team_data["BallWon InterceptionWon"],
    "Tackles Won": team_data["BallWon TackleWon"],
    "Aerial Duels Won": team_data["BallWon Aerial"],
}
rec_df = pd.DataFrame(
    list(rec_data.items()), columns=["Action Type", "Count"]
)
fig_rec = px.bar(
    rec_df,
    x="Action Type",
    y="Count",
    color="Action Type",
    title="Team Ball Recovery Breakdown",
)
st.plotly_chart(fig_rec, use_container_width=True)
