import streamlit as st
from googleapiclient.discovery import build
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

def render():
    st.title("KPI Dashboard")

    # Google Sheets details
    sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"  # Replace with your Google Sheet ID
    range_name = "KPIdashboard"  # Replace with your sheet's range (e.g., 'Sheet1!A1:D10')

    # Fetch data
    try:
        df = fetch_google_sheets_data(sheet_id, range_name)
        if not df.empty:
            st.dataframe(df)
        else:
            st.error("No data found in the specified Google Sheets range.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

render()