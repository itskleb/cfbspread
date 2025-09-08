import pandas as pd
import streamlit as st
import plotly.express as px

st.title("CFB Spread Viewer")

df = pd.read_csv("CFB_Spread_Database.csv")

teams = df['homeTeam'].unique().tolist()
with st.sidebar:
  week = st.selectbox("Week",[i for i in range(1,17)])
  team = st.selectbox("Team",df['homeTeam'].sort_values().unique().tolist())
df = df[df['week'] == week]

money = px.scatter(df.x='spreaddiff',y='spreadchg')

st.plotly_chart(money)

df
