import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Streamlit app configuration
st.set_page_config(layout="wide")

# Google Sheets configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1pqJjuQCt28LayLeRne8eZu8e356I1q6NWUzBABsNqeU/edit?usp=sharing"  # Replace with your Google Sheet URL
SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]

# Function to authenticate and fetch data from Google Sheets
@st.cache_data
def authenticate_and_fetch(sheet_url):
    """
    Authenticate with Google Sheets API and fetch the sheet data.
    """
    try:
        # Load credentials from Streamlit secrets
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES,
        )

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

# Function to update Google Sheets with edited data
def update_sheet(sheet, dataframe):
    """
    Update the Google Sheet with new data from the DataFrame.
    """
    try:
        # Convert DataFrame to a list of lists for Google Sheets
        data = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
        
        # Clear the sheet and update with new data
        sheet.clear()  # Clear existing data
        sheet.update(data)  # Write new rows starting at the first row
    except Exception as e:
        st.error(f"Failed to update the Google Sheet: {e}")
        raise

# Main function to render the Streamlit app
def render():
    st.title("Google Sheets as a Database with Streamlit")

    try:
        # Authenticate and fetch Google Sheet data
        df, sheet = authenticate_and_fetch(SHEET_URL)

        # Display editable table in Streamlit
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
