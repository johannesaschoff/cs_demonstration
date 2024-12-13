
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

def render():
    st.title("Edit Vendor Areas in Google Sheets")
        
        # Fetch data directly without caching
    def fetch_data():
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn.read(worksheet="Names")
        
    
    
    df= fetch_data()
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
render()
