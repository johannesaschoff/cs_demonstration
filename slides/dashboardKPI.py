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
    df = fetch_google_sheets_data(sheet_id, range_name)
    df.columns = df.columns.str.strip().str.replace("\n", "")  
    
    # Replace commas with dots and convert to float
    df = df.replace(',', '.', regex=True).apply(pd.to_numeric, errors='coerce')
    
    # Access and round specific values
    try:
        cer = round(float(df.loc[0, "Corporate Engagement Rate"]), 2)
        cr = round(float(df.loc[0, "Corporate Conversion Rate"]), 2)
        ags = round(float(df.loc[0, "Corporate Average Gift Size"]), 2)
        roi = round(float(df.loc[0, "Corporate Return on Invest (ROI)"]), 2)
    except KeyError as e:
        st.error(f"Column not found: {e}")
        cer, cr, ags, roi = None, None, None, None
    except ValueError as e:
        st.error(f"Invalid value for conversion: {e}")
        cer, cr, ags, roi = None, None, None, None
    
    st.markdown("**Corporate KPIs**")
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Engagement Rate", value=cer, delta=0.3, border=True)
    col2.metric(label= "Conversion Rate", value=cr,delta=-0.5, border=True)
    col3.metric(label="Average Gift Size", value=f"£ {ags}",delta=1.2, border=True)
    col4.metric(label="Return on Invest (ROI)", value=roi,delta=0.1, border=True)
    
    try:
        ccer = round(float(df.loc[0, "Charity Engagement Rate"]), 2)
        ccr = round(float(df.loc[0, "Charity Conversion Rate"]), 2)
        cags = round(float(df.loc[0, "Charity Average Gift Size"]), 2)
        croi = round(float(df.loc[0, "Charity Return on Invest (ROI)"]), 2)
    except KeyError as e:
        st.error(f"Column not found: {e}")
        cer, cr, ags, roi = None, None, None, None
    except ValueError as e:
        st.error(f"Invalid value for conversion: {e}")
        cer, cr, ags, roi = None, None, None, None
    
    st.markdown("**Charity KPIs**")
    # Display metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(label="Engagement Rate", value=ccer, delta=0.3, border=True)
    col2.metric(label= "Conversion Rate", value=ccr,delta=-0.5, border=True)
    col3.metric(label="Average Gift Size", value=f"£ {cags}",delta=1.2, border=True)
    col4.metric(label="Return on Invest (ROI)", value=croi,delta=0.1, border=True)

render()
