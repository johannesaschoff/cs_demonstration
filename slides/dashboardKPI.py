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

def update_google_sheets_data(sheet_id, range_name, values):
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    service = build('sheets', 'v4', credentials=creds)

    body = {'values': values}
    try:
        result = service.spreadsheets().values().update(
            spreadsheetId=sheet_id, range=range_name,
            valueInputOption="RAW", body=body).execute()
        return result
    except Exception as error:
        st.error(f"An error occurred: {error}")
        return None

def render():
    st.title("KPI Dashboard")

    # Google Sheets details
    sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"  # Replace with your Google Sheet ID
    range_name = "KPIdashboard"  # Replace with your sheet's range (e.g., 'Sheet1!A1:D10')

    # Fetch data
    df = fetch_google_sheets_data(sheet_id, range_name)
    df.columns = df.columns.str.strip().str.replace("\n", "")

    # Replace commas with dots and handle invalid data
    df = df.replace({',': '.', '#DIV/0!': None, '': None}, regex=True).apply(pd.to_numeric, errors='coerce')

    # Access and round specific values
    try:
        cer = round(df.get("Corporate Engagement Rate", pd.Series([None])).iloc[0], 2)
        cr = round(df.get("Corporate Conversion Rate", pd.Series([None])).iloc[0], 2)
        ags = round(df.get("Corporate Average Gift Size", pd.Series([None])).iloc[0], 2)
        roi = round(df.get("Corporate Return on Invest (ROI)", pd.Series([None])).iloc[0], 2)
    except Exception as e:
        st.error(f"Error accessing metrics: {e}")
        cer, cr, ags, roi = None, None, None, None

    # Changes of values
    range_name = "History"
    history = fetch_google_sheets_data(sheet_id, range_name)
    history = history.replace({',': '.', '#DIV/0!': None, '': None}, regex=True)

    try:
        for column in ["Corporate Engagement Rate", "Corporate Conversion Rate", 
                       "Corporate Average Gift Size", "Corporate Return on Invest (ROI)"]:
            if column in history.columns:
                history[column] = pd.to_numeric(history[column], errors='coerce')

        last_value = history["Corporate Engagement Rate"].dropna().iloc[-1]
        second_last_value = history["Corporate Engagement Rate"].dropna().iloc[-2]
        cer_ratio = round((last_value / second_last_value - 1), 2) if second_last_value != 0 else None
    except Exception as e:
        st.error(f"Error processing historical data: {e}")
        cer_ratio = None

    st.markdown("**Corporate KPIs**")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Engagement Rate", value=cer, delta=cer_ratio)
    col2.metric(label="Conversion Rate", value=cr)
    col3.metric(label="Average Gift Size", value=f"£ {ags}")
    col4.metric(label="Return on Invest (ROI)", value=roi)

    st.markdown("**Expenditure Inputs**")
    range_name = "F&s"
    df = fetch_google_sheets_data(sheet_id, range_name)

    try:
        cfh = round(pd.to_numeric(df.get("Corporate Fundraising Hours", pd.Series([None])).iloc[0], errors='coerce'))
        ccfh = round(pd.to_numeric(df.get("Charity Fundraising Hours", pd.Series([None])).iloc[0], errors='coerce'))
        w = round(pd.to_numeric(df.get("Wage", pd.Series([None])).iloc[0], errors='coerce'))
    except Exception as e:
        st.error(f"Error accessing expenditure inputs: {e}")
        cfh, ccfh, w = None, None, None

    col1, col2, col3 = st.columns(3)
    col1.metric(label="Corporate Fundraising Hours", value=f"{cfh} h")
    col2.metric(label="Charity Fundraising Hours", value=f"{ccfh} h")
    col3.metric(label="Wage", value=f"{w} £/h")

    with col1:
        cfh_input = st.text_input("Edit Corporate Fundraising Hours", value=str(cfh))
    with col2:
        ccfh_input = st.text_input("Edit Charity Fundraising Hours", value=str(ccfh))
    with col3:
        w_input = st.text_input("Edit Wage", value=str(w))

    if st.button("Save All Changes"):
        try:
            df.loc[0, "Corporate Fundraising Hours"] = int(cfh_input)
            df.loc[0, "Charity Fundraising Hours"] = int(ccfh_input)
            df.loc[0, "Wage"] = int(w_input)

            updated_values = [df.columns.tolist()] + df.fillna("", downcast='infer').values.tolist()
            result = update_google_sheets_data(sheet_id, range_name, updated_values)

            if result:
                st.success("Changes saved successfully! Reloading data...")
                st.rerun()
            else:
                st.error("Failed to save changes.")
        except Exception as e:
            st.error(f"Error saving changes: {e}")

render()
