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

@st.cache_data
def authenticate_and_fetch(sheet_url):
    """
    Authenticate with Google Sheets API and fetch the sheet data.
    """
    # Debug: Show the loaded credentials from secrets
    st.write("Loading credentials from secrets...")
    
    credentials_dict = st.secrets["GOOGLE_CREDENTIALS"]  # Ensure it's TOML format in secrets
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
    
    # Debug: Check if credentials are valid
    st.write("Credentials loaded successfully.")
    
    try:
        gc = gspread.authorize(credentials)  # Authorize the client
        sheet = gc.open_by_url(sheet_url).sheet1  # Access the first sheet
        st.write("Google Sheet accessed successfully.")
        
        # Fetch the data and convert to DataFrame
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        st.write("Data fetched successfully.")
        return df, sheet
    except Exception as e:
        st.error(f"Failed to authenticate or fetch the sheet: {e}")
        raise

def update_sheet(sheet, dataframe):
    """
    Update the Google Sheet with new data from the DataFrame.
    """
    try:
        st.write("Clearing sheet and updating data...")
        
        # Clear the sheet and update with the new data
        sheet.clear()
        data = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
        sheet.update("A1", data)
        
        st.write("Data updated successfully.")
    except Exception as e:
        st.error(f"Failed to update the Google Sheet: {e}")
        raise

def render():
    st.title("Craftsmanship and Production")

    try:
        df, sheet = authenticate_and_fetch(SHEET_URL)

        if "category" not in df.columns:
            df["category"] = ""

        # Display editable data with a select box column
        st.markdown("### Update Data with Categories")
        edited_df = st.data_editor(
            df,
            column_config={
                "category": st.column_config.SelectboxColumn(
                    "App Category",
                    help="The category of the app",
                    width="medium",
                    options=[
                        "📊 Data Exploration",
                        "📈 Data Visualization",
                        "🤖 LLM",
                    ],
                    required=True,
                )
            },
            hide_index=True,
        )

        # Save changes back to Google Sheets
        if st.button("Save Changes"):
            update_sheet(sheet, edited_df)
            st.success("Google Sheet updated successfully!")
    except Exception as e:
        st.error(f"An error occurred: {e}")

render()
