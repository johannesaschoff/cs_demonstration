
import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import requests
import ast

def render():
    st.markdown("**Matching Charities**")
    #csv_education_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/gesourcte_charities.csv" 
    conn = st.connection("gsheets", type=GSheetsConnection)
    existing_data = conn.read(worksheet="Names")

    try:
        #df = pd.read_csv(csv_education_url)
        #df = df[df["area_id"] == 1]   
        #df = df.drop(columns=["fitting area (1 / 0)", "area_id"])
        #df = df.rename(columns={"charity_name": "Charity Name", "registered_charity_number": "Registered Charity Number", "latest_income": "Latest Income", "latest_expenditure": "Latest Expenditure", "charity_contact_email": "Charity Contact Email", "charity_activities": "Charity Activities"})
        
        st.data_editor(
            existing_data,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    width="small",
                    help="Logos of companies"
                ),
                "area": st.column_config.SelectboxColumn(
                    "Select Area",
                    width="medium",
                    options=[
                        "Production",
                        "Education",
                        "Community",
                        "Emergency",
                        "Agriculture",
                    ],
                    required=True,
                )
            },
            hide_index=True  
        )
    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")


render()
