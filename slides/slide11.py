import streamlit as st
import pandas as pd
import requests
import ast
import logging
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.oauth2.service_account import Credentials

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
        if "edited_df" not in st.session_state:
            df = fetch_google_sheets_data(sheet_id, range_name)
            df = pd.DataFrame(data=df)
            df = df.rename(columns={"Contact Mail": "Contact Mail/Phone Nr./LinkedIn"})

            def safe_literal_eval(x):
                try:
                    # Attempt to evaluate the string as a Python literal
                    return ast.literal_eval(x) if isinstance(x, str) else x
                except (ValueError, SyntaxError) as e:
                    logging.warning(f"Skipping invalid value: {x} ({e})")
                    return []  # Return an empty list for invalid values

            # Apply the function and ensure all entries are lists
            df["Industries"] = df["Industries"].apply(safe_literal_eval)
            df["Industries"] = df["Industries"].apply(lambda x: x if isinstance(x, list) else [])

            # List of columns to process
            columns_to_process = [
                "Craftsmanship and production",
                "Educational Development",
                "Community Development and Employment",
                "Emergency Relief and Basic Needs",
                "Food Security and Sustainable Agriculture"
            ]

            # Define a function to convert "WAHR" to True and "FALSCH" to False
            def convert_to_boolean(value):
                if isinstance(value, str):
                    if value.strip().upper() == "WAHR":
                        return True
                    elif value.strip().upper() == "FALSCH":
                        return False
                return None

            # Apply the function to all specified columns
            for col in columns_to_process:
                if col in df.columns:
                    df[col] = df[col].apply(convert_to_boolean)

            df = df[df["Craftsmanship and production"] == True]
            st.session_state.edited_df = df

        edited_df = st.session_state.edited_df

        if not edited_df.empty:
            edited_df = st.data_editor(
                edited_df,
                column_config={
                    "Logo": st.column_config.ImageColumn(
                        label="Company Logo",
                        width="small",
                        help="Logos of companies"
                    ),
                    "Industries": st.column_config.ListColumn(
                        label="Industries",
                        help="List of industries represented as tags"
                    ),
                    "Sustainability report": st.column_config.LinkColumn(
                        label="Sustainability Report",
                        help="Link to the company's sustainability report",
                        validate=r"^https?://.+",
                        display_text="View Report"
                    ),
                    "Total Donations": st.column_config.NumberColumn(
                        "Total Donations (in CHF)",
                        help="Total amount of collected donations from Corporate in CHF",
                        min_value=0,
                        max_value=100000000,
                        step=1,
                        format="CHF%d",
                    )
                },
                disabled=[
                    "Logo", "Company Name", "Industries", "EBIT", "Craftsmanship and production",
                    "Educational Development", "Community Development and Employment",
                    "Emergency Relief and Basic Needs", "Food Security and Sustainable Agriculture",
                    "Contact Name", "Contact Mail/Phone Nr./LinkedIn", "Sustainability report", "Focus"
                ],
                hide_index=True,
                use_container_width=True
            )

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
                        st.session_state.pop("edited_df", None)  # Clear session state to refresh data
                        st.success("Changes saved successfully!")
                        st.rerun()  # Rerun the app to fetch updated data
                    else:
                        st.error("Failed to save changes.")
                except Exception as e:
                    st.error(f"An error occurred while saving: {e}")
        else:
            st.error("No data found in the specified Google Sheets range.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

render()
