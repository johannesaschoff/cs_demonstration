

import streamlit as st 
from streamlit_gsheets import SheetsConnection
import pandas as pd

# Display Title and Description
st.title("Vendor Management Portal")
st.markdown("Enter the details of the new vendor below.")

# Establishing a Google Sheets connection
conn = st. experimental_connection("gsheets", type=GSheetsConnection)

# Fetch existing vendors data
existing_data = conn.read (worksheet="dataframe_corporates_with_logos", usecols = list(range(6)), tt1=5)
existing_data = existing_data.dropna(how="all")

st. dataframe (existing_data)
