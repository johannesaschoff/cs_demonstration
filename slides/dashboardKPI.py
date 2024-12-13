import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import ast
import logging

def render():
  st.title("KPI Dashboard")

  def fetch_data(x):
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(worksheet = x)

  df= fetch_data("KPIdashboard")
  df = pd.DataFrame(data = df)
  st.dataframe(df)

render()
