import pandas as pd
import streamlit as st
import plotly.express as px

st.title("CFB Spread Viewer")

df = pd.read_csv("CFB_Spread_Database.csv")

teams = df['homeTeam'].unique().tolist()

week = st.selectbox([i for i in range(1,17)],df['week'][0])

df = df[df['week'] == week]

df
