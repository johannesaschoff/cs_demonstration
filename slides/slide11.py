import streamlit as st
import pandas as pd
import requests
import ast
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
    st.title("Craftsmanship and Production")
    st.markdown("**Project types**")
    st.write("- Butchery")
    st.write("- Bakery")
    st.write("- Kitchen")
    st.write("- Woodwork")
    st.write("- Sewing")
    st.write("- Metal Construction Workshop")

    # Section: Slideshow
    st.markdown("**Pitchdeck Preview**")
    columns = st.columns(5)

    image_urls = [
        ["image_1.png", "image_6.png"],
        ["image_2.png", "image_7.png"],
        ["image_3.png", "image_8.png"],
        ["image_4.png", "image_9.png"],
        ["image_5.png", "image_10.png"]
    ]

    for col, urls in zip(columns, image_urls):
        for url in urls:
            col.image(
                f"https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/{url}",
                use_container_width=True
            )

    pptx_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/PitchDeck production.pptx"
    try:
        pptx_data = fetch_pptx(pptx_url)
        st.download_button(
            label="Download PPTX File",
            data=pptx_data,
            file_name="PitchDeck.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
    except Exception as e:
        st.error(f"Could not fetch the PPTX file: {e}")     

    # Google Sheets details
    sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"  # Replace with your Google Sheet ID
    range_name = "Names"  # Replace with your sheet's range (e.g., 'Sheet1!A1:D10')

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

