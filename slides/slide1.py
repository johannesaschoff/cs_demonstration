import streamlit as st
import pandas as pd
import gspread
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
    st.write("Loading credentials from secrets...")

    # Load credentials
    credentials_dict = st.secrets["GOOGLE_CREDENTIALS"]
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)

    try:
        # Authenticate and access the sheet
        gc = gspread.Client(auth=credentials)
        gc.session = gspread.AuthorizedSession(credentials)
        sheet = gc.open_by_url(sheet_url).sheet1
        st.write("Google Sheet accessed successfully!")

        # Fetch data
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
        
        # Prepare data for update
        data = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
        st.write("Prepared data for update:", data)  # Debugging log

        # Clear the sheet by deleting rows and adding empty rows
        sheet.resize(1)  # Resizes the sheet to only one row (the header)
        st.write("Sheet cleared successfully.")

        # Update the sheet with new data
        sheet.insert_rows(data, row=1)  # Inserts the data starting from row 1
        st.write("Sheet updated successfully.")
    except Exception as e:
        st.error(f"Failed to update the Google Sheet: {e}")
        raise

@st.cache_data
def test_connection(sheet_url):
    """
    Test the connection to the Google Sheet by fetching its data.
    """
    st.write("Testing connection to Google Sheet...")

    # Load credentials from Streamlit secrets
    credentials_dict = st.secrets["GOOGLE_CREDENTIALS"]
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)

    try:
        # Authenticate and access the sheet
        gc = gspread.Client(auth=credentials)
        gc.session = gspread.AuthorizedSession(credentials)
        sheet = gc.open_by_url(sheet_url).sheet1
        st.write("Google Sheet accessed successfully!")

        # Fetch some data
        data = sheet.get_all_records()
        st.write("Sample data fetched from Google Sheet:")
        st.write(data[:5])  # Show the first 5 records for testing

        return True
    except Exception as e:
        st.error(f"Failed to connect to the Google Sheet: {e}")
        return False

def render():
    st.title("Google Sheets Connection Test and Update")

    # Test the connection
    is_connected = test_connection(SHEET_URL)

    if is_connected:
        st.success("Connection to Google Sheet is working!")

        try:
            # Fetch data and make it editable
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
    else:
        st.error("Connection to Google Sheet failed.")

# Run the app
render()
