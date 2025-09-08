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

money = px.histogram(df,x='spreadchg',hover_data=['favorite','spreadmean'])

time = px.line(df,x='date',y='spreadchg',color='favorite',hover_data=['spreadmean','spreadOpen','homeTeam'])
t1,t2 = st.tabs(['Histogram','Line'])
with t1:
  st.plotly_chart(money)
with t2:
  st.plotly_chart(time)

df['spreadABV'] = df['spreadchg'].abs()


display_df = df[['homeTeam', 'awayTeam', 'favorite','spreadmean','spreadchg','spreadABV']]

display_df
