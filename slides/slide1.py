import streamlit as st
import pandas as pd
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# Streamlit app configuration
st.set_page_config(layout="wide")

# Google Sheets configuration
SHEET_URL = "YOUR_GOOGLE_SHEET_URL"  # Replace with your Google Sheet URL
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_data
def authenticate_and_fetch(sheet_url):
    """
    Authenticate with Google Sheets API and fetch the sheet data.
    """
    try:
        # Load credentials from Streamlit secrets
        credentials_dict = st.secrets["GOOGLE_CREDENTIALS"]  # Ensure it's in TOML format
        credentials = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
        
        # Authorize with Google Sheets
        client = gspread.authorize(credentials)
        sheet = client.open_by_url(sheet_url).sheet1  # Access the first sheet
        
        # Fetch data and convert to DataFrame
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df, sheet
    except Exception as e:
        st.error(f"Failed to authenticate or fetch the sheet: {e}")
        raise

def update_sheet(sheet, dataframe):
    """
    Update the Google Sheet with new data from the DataFrame.
    """
    try:
        # Prepare data for updating the sheet
        data = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
        
        # Clear the sheet and update with new data
        sheet.clear()  # Clear existing data
        sheet.insert_rows(data, row=1)  # Write new rows starting at the first row
    except Exception as e:
        st.error(f"Failed to update the Google Sheet: {e}")
        raise

def render():
    st.title("Google Sheets as a Database with Streamlit")

    try:
        # Authenticate and fetch the Google Sheet data
        df, sheet = authenticate_and_fetch(SHEET_URL)

        # Display editable table
        st.markdown("### Edit Data")
        edited_df = st.data_editor(df, hide_index=True)

        # Save changes back to Google Sheets
        if st.button("Save Changes"):
            update_sheet(sheet, edited_df)
            st.success("Google Sheet updated successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

# Run the Streamlit app
render()
