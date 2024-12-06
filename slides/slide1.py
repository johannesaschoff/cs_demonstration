import streamlit as st
import pandas as pd
import gspread
from google.auth.transport.requests import Request
from google.oauth2.service_account import Credentials

# Streamlit app configuration
st.set_page_config(layout="wide")

# Google Sheets configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1pqJjuQCt28LayLeRne8eZu8e356I1q6NWUzBABsNqeU/edit?usp=sharing"  # Replace with your Google Sheet URL
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Path to your service account credentials file
SERVICE_ACCOUNT_FILE = "path/to/credentials.json"  # Replace with the path to your JSON file


@st.cache_data
def authenticate_and_fetch(sheet_url):
    """
    Authenticate with Google Sheets API and fetch the sheet data.
    """
    credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
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

        # Display editable data table
        st.markdown("### Matching Corporates")
        edited_df = st.experimental_data_editor(df, num_rows="dynamic")

        # Save changes back to Google Sheets
        if st.button("Save Changes"):
            update_sheet(sheet, edited_df)
            st.success("Google Sheet updated successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")


render()
