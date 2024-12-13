
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import ast
import requests

def render():
    st.title("Edit Vendor Areas in Google Sheets")
        
        # Fetch data directly without caching
    def fetch_data():
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn.read(worksheet="Names")
        
    
    try:
        df= fetch_data()
    
        df = df[df["Craftsmanship and production"] == True]
        df = df.rename(columns={"Contact Mail": "Contact Mail/Phone Nr./LinkedIn"})
    
        st.dataframe(
            df,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    width="small",
                    help="Logos of companies"
                ),
                "Industries": st.column_config.ListColumn(
                    label="Industries",
                    help="List of industries represented as tags"
                ),
                "Sustainability report": st.column_config.LinkColumn(
                    label="Sustainability Report",
                    help="Link to the company's sustainability report",
                    validate=r"^https?://.+",  # Basic validation for URLs
                    display_text="View Report"  # Display text for the links
                )
            },
            hide_index=True,
            use_container_width=True
        )
        response = requests.get(excel_url)
        if response.status_code == 200:
            excel_data = response.content
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="Craftsmanship_and_Production.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(f"Failed to fetch the Excel file. Status code: {response.status_code}")
    except Exception as e:
            st.error(f"Failed to load the dataset: {e}")
render()
