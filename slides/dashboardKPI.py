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
    except HttpError as error:
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
    col1.metric(label="Engagement Rate", value=cer, border=True)
    col2.metric(label= "Conversion Rate", value=cr, border=True)
    col3.metric(label="Average Gift Size", value=f"£ {ags}", border=True)
    col4.metric(label="Return on Invest (ROI)", value=roi, border=True)
    
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
    col1.metric(label="Engagement Rate", value=ccer,  border=True)
    col2.metric(label= "Conversion Rate", value=ccr, border=True)
    col3.metric(label="Average Gift Size", value=f"£ {cags}", border=True)
    col4.metric(label="Return on Invest (ROI)", value=croi,border=True)
    
    st.markdown("**Expenditure Inputs**")
    
    sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"
    range_name = "F&s"
    
    
    df = fetch_google_sheets_data(sheet_id, range_name)
    
    try:
        cfh = round(float(df.loc[0, "Corporate Fundraising Hours"]))
        ccfh = round(float(df.loc[0, "Charity Fundraising Hours"]))
        w = round(float(df.loc[0, "Wage"]))
    except KeyError as e:
        st.error(f"Column not found: {e}")
        cer, cr, ags, roi = None, None, None, None
    except ValueError as e:
        st.error(f"Invalid value for conversion: {e}")
        cer, cr, ags, roi = None, None, None, None
    
    col1, col2, col3, col4  = st.columns(4)
    col1.metric(label="Corporate Fundraising Hours", value=f"{cfh} h",border=True)
    col2.metric(label="Charity Fundraising Hours", value=f"{ccfh} h",border=True)
    col3.metric(label="Wage", value=f"{w} £/h", border=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    # Input fields for the three values
    with col1:
        cfh_input = st.text_input("Edit", value=str(cfh), key="cfh_input")
    
    with col2:
        ccfh_input = st.text_input("Edit", value=str(ccfh), key="ccfh_input")
    
    with col3:
        w_input = st.text_input("Edit", value=str(w), key="w_input")
    
    # Combined save button
    if st.button("Save All Changes"):
        try:
            # Update the DataFrame with the new values
            df.loc[0, "Corporate Fundraising Hours"] = int(cfh_input)
            df.loc[0, "Charity Fundraising Hours"] = int(ccfh_input)
            df.loc[0, "Wage"] = int(w_input)
    
            # Construct updated values for Google Sheets
            updated_values = [df.columns.tolist()] + df.fillna("").values.tolist()
    
            # Update the Google Sheet
            result = update_google_sheets_data(sheet_id, range_name, updated_values)
    
            if result:
                st.success("All changes saved successfully! Reloading data...")
                st.rerun()
            else:
                st.error("Failed to save changes.")
        except ValueError as e:
            st.error(f"Invalid input: {e}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
render()
