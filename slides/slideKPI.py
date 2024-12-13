import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests
import ast

# Fetch data directly from Google Sheets
def fetch_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(worksheet="Names")

# Fetch PPTX file from a URL
def fetch_pptx(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch the PPTX. Status code: {response.status_code}")

def render():
    st.title("KPI")
    
    # Section: Data from Google Sheets
    st.markdown("**Matching Corporates**")
    try:
        df = fetch_data()
        
        # Apply transformations if required
        if "Craftsmanship and production" in df.columns:
            df = df[df["Craftsmanship and production"] == True]
        
        if "Industries" in df.columns:
            df["Industries"] = df["Industries"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
        
        st.dataframe(df)
    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

    # Section: Download PPTX
    st.markdown("**Pitchdeck Preview**")
    pptx_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/PitchDeck production.pptx"
    try:
        pptx_data = fetch_pptx(pptx_url)
        st.download_button(
            label="Download PPTX File",
            data=pptx_data,
            file_name="PitchDeck.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
    except Exception as e:
        st.error(f"Could not fetch the PPTX file: {e}")

    # Section: Additional Dataset
    st.markdown("**Matching Charities**")
    csv_education_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/gesourcte_charities.csv"
    try:
        df_charities = pd.read_csv(csv_education_url)
        st.dataframe(df_charities)
    except Exception as e:
        st.error(f"Failed to load the charity dataset: {e}")

render()
