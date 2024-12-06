import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import json

# Streamlit app configuration
st.set_page_config(layout="wide")

# Google Sheets configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1pqJjuQCt28LayLeRne8eZu8e356I1q6NWUzBABsNqeU/edit?usp=sharing"  # Replace with your Google Sheet URL
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_data
def authenticate_and_fetch(sheet_url):
    """
    Authenticate with Google Sheets API and fetch the sheet data.
    """
    # Load credentials from Streamlit secrets
    credentials_dict = st.secrets["GOOGLE_CREDENTIALS"]
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
    
    # Authenticate with gspread
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(sheet_url).sheet1  # Access the first sheet
    data = sheet.get_all_records()  # Fetch all rows as a list of dictionaries
    df = pd.DataFrame(data)
    return df, sheet

def update_sheet(sheet, dataframe):
    """
    Update the Google Sheet with new data from the DataFrame.
    """
    sheet.clear()  # Clear existing data in the sheet
    sheet.update([dataframe.columns.values.tolist()] + dataframe.values.tolist())  # Update with new data

def render():
    st.title("Craftsmanship and Production")

    # Authenticate and fetch Google Sheets data
    try:
        df, sheet = authenticate_and_fetch(SHEET_URL)

        # Display the data as a table
        st.markdown("### Matching Corporates")
        st.write("Current Data from Google Sheets:")
        st.dataframe(df)

        # Add manual input fields for updates
        st.markdown("### Update Data")
        rows = []
        for i in range(len(df)):
            row = {}
            for column in df.columns:
                row[column] = st.text_input(f"Row {i + 1} - {column}", df.at[i, column])
            rows.append(row)

        # Create a new DataFrame from input
        new_df = pd.DataFrame(rows)

        # Save changes back to Google Sheets
        if st.button("Save Changes"):
            update_sheet(sheet, new_df)
            st.success("Google Sheet updated successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

render()
