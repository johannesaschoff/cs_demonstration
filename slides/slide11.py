import streamlit as st
import pandas as pd
import requests
import ast
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials
import pandas as pd
import logging


@st.cache_data
def fetch_pptx(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch the PPTX. Status code: {response.status_code}")

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

    # Google Sheets details
    sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"  # Replace with your Google Sheet ID
    range_name = "Names"  # Replace with your sheet's range (e.g., 'Sheet1!A1:D10')

    # Fetch data
    try:
        # Add a session state to persist the data
        if "edited_df" not in st.session_state:
            df = fetch_google_sheets_data(sheet_id, range_name)
            df = pd.DataFrame(data=df)
            df = df.rename(columns={"Contact Mail": "Contact Mail/Phone Nr./LinkedIn"})

            # Data preprocessing
            def safe_literal_eval(x):
                try:
                    return ast.literal_eval(x) if isinstance(x, str) else x
                except (ValueError, SyntaxError):
                    return []

            df["Industries"] = df["Industries"].apply(safe_literal_eval)
            df["Industries"] = df["Industries"].apply(lambda x: x if isinstance(x, list) else [])

            columns_to_process = [
                "Craftsmanship and production",
                "Educational Development",
                "Community Development and Employment",
                "Emergency Relief and Basic Needs",
                "Food Security and Sustainable Agriculture"
            ]

            def convert_to_boolean(value):
                if isinstance(value, str):
                    if value.strip().upper() == "WAHR":
                        return True
                    elif value.strip().upper() == "FALSCH":
                        return False
                return None

            for col in columns_to_process:
                if col in df.columns:
                    df[col] = df[col].apply(convert_to_boolean)

            df = df[df["Craftsmanship and production"] == True]
            st.session_state.edited_df = df  # Save to session state

        edited_df = st.session_state.edited_df

        # Editable DataFrame
        edited_df = st.data_editor(
            edited_df,
            column_config={
                "Logo": st.column_config.ImageColumn(label="Company Logo", width="small"),
                "Industries": st.column_config.ListColumn(label="Industries"),
                "Sustainability report": st.column_config.LinkColumn(
                    label="Sustainability Report", validate=r"^https?://.+"
                ),
                "Total Donations": st.column_config.NumberColumn("Total Donations (in CHF)", min_value=0),
            },
            hide_index=True,
            use_container_width=True,
        )

        # Save changes
        if st.button("Save Changes"):
            # Flatten any list-like columns
            for col in edited_df.columns:
                if edited_df[col].apply(lambda x: isinstance(x, list)).any():
                    edited_df[col] = edited_df[col].apply(lambda x: ", ".join(x) if isinstance(x, list) else x)

            # Convert DataFrame to a list of lists
            updated_values = [edited_df.columns.tolist()] + edited_df.values.tolist()

            # Update Google Sheets
            try:
                result = update_google_sheets_data(sheet_id, range_name, updated_values)
                if result:
                    st.session_state.edited_df = edited_df  # Save the new state
                    st.success("Changes saved successfully!")
                else:
                    st.error("Failed to save changes.")
            except Exception as e:
                st.error(f"An error occurred while saving: {e}")

render()
