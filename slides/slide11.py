import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import pandas as pd

# Function to fetch data from Google Sheets
def fetch_google_sheets_data(sheet_id, range_name):
    # Load credentials from Streamlit secrets
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])

    # Convert data to a pandas DataFrame
    if values:
        df = pd.DataFrame(values[1:], columns=values[0])  # Assuming first row contains headers
        return df
    else:
        return pd.DataFrame()  # Return empty DataFrame if no data

# Function to update data in Google Sheets
def update_google_sheets_data(sheet_id, range_name, values):
    # Load credentials from Streamlit secrets
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    service = build('sheets', 'v4', credentials=creds)

    # Call the Sheets API to update values
    body = {
        'values': values
    }
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        return result
    except HttpError as error:
        st.error(f"An error occurred: {error}")
        return None

def render():
    st.title("KPI Dashboard")

    # Google Sheets details
    sheet_id = "your_google_sheet_id"  # Replace with your Google Sheet ID
    range_name = "KPIdashboard"  # Replace with your sheet's range (e.g., 'Sheet1!A1:D10')

    # Fetch data
    try:
        df = fetch_google_sheets_data(sheet_id, range_name)
        if not df.empty:
            edited_df = st.data_editor(
                df,
                column_config={
                    "Total Donations": st.column_config.NumberColumn(
                        label="Total Donations",
                        help="Edit the total donations for each entry",
                        format="%d",
                    )
                },
                use_container_width=True,
                num_rows="fixed"
            )

            if st.button("Save Changes"):
                update_result = update_google_sheets_data(
                    sheet_id, range_name,
                    [edited_df.columns.tolist()] + edited_df.values.tolist()
                )
                if update_result:
                    st.success("Google Sheets updated successfully!")
                    st.experimental_rerun()
                else:
                    st.error("Failed to update Google Sheets.")
        else:
            st.error("No data found in the specified Google Sheets range.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

render()
