
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import ast
import logging

def render():
    st.title("Edit Vendor Areas in Google Sheets")
        
        # Fetch data directly without caching
    def fetch_data():
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn.read(worksheet="Names")
        
    
    
    df= fetch_data()
    df = pd.DataFrame(data = df)
    df = df.rename(columns={"Contact Mail": "Contact Mail/Phone Nr./LinkedIn"})
    
    def safe_literal_eval(x):
        try:
            # Attempt to evaluate the string as a Python literal
            return ast.literal_eval(x) if isinstance(x, str) else x
        except (ValueError, SyntaxError) as e:
            logging.warning(f"Skipping invalid value: {x} ({e})")
            return []  # Return an empty list for invalid values
    
    # Apply the function and ensure all entries are lists
    df["Industries"] = df["Industries"].apply(safe_literal_eval)
    df["Industries"] = df["Industries"].apply(lambda x: x if isinstance(x, list) else [])
    
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
