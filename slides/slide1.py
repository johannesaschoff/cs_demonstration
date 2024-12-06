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
    credentials_dict = json.loads(st.secrets["GOOGLE_CREDENTIALS"])
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)
    
    # Use AuthorizedSession for compatibility
    gc = gspread.Client(auth=credentials)
    gc.session = gspread.auth.AuthorizedSession(credentials)

    # Open and fetch the Google Sheet
    sheet = gc.open_by_url(sheet_url).sheet1  # Access the first sheet
    data = sheet.get_all_records()  # Fetch all rows as a list of dictionaries
    df = pd.DataFrame(data)
    return df, sheet


def update_sheet(sheet, dataframe):
    """
    Update the Google Sheet with new data from the DataFrame.
    """
    try:
        # Clear existing data in the sheet
        sheet.clear()

        # Convert the DataFrame to a list of lists (compatible with gspread)
        data = [dataframe.columns.values.tolist()] + dataframe.values.tolist()

        # Update the sheet with new data
        sheet.update("A1", data)  # Start updating from cell A1

    except Exception as e:
        st.error(f"Failed to update the Google Sheet: {e}")
        raise


def render():
    st.title("Craftsmanship and Production")

    # Authenticate and fetch Google Sheets data
    try:
        df, sheet = authenticate_and_fetch(SHEET_URL)

        # Ensure the category column exists in the data
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
