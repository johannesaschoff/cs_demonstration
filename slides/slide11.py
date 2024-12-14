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
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    service = build('sheets', 'v4', credentials=creds)

    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
    values = result.get('values', [])

    if values:
        df = pd.DataFrame(values[1:], columns=values[0])
        return df
    else:
        return pd.DataFrame()

# Function to update specific columns in Google Sheets
def update_google_sheets_columns(sheet_id, range_name, columns, df):
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"])
    service = build('sheets', 'v4', credentials=creds)

    updated_df = df[columns].fillna("")  # Only include specific columns
    updated_values = [updated_df.columns.tolist()] + updated_df.values.tolist()

    body = {'values': updated_values}
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
    st.write(''':blue-background[Butchery] :blue-background[Bakery] :blue-background[Kitchen] :blue-background[Woodwork] :blue-background[Sewing] :blue-background[Metal Construction Workshop]''')

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

    sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"
    range_name = "Corporates"

    try:
        # Fetch fresh data from Google Sheets
        df = fetch_google_sheets_data(sheet_id, range_name)
        df = df.rename(columns={"Contact Mail": "Contact Mail/Phone Nr./LinkedIn"})

        def safe_literal_eval(x):
            try:
                return ast.literal_eval(x) if isinstance(x, str) else x
            except (ValueError, SyntaxError):
                logging.warning(f"Skipping invalid value: {x}")
                return []

        # Process columns with list-like data
        if "Industries" in df.columns:
            df["Industries"] = df["Industries"].apply(safe_literal_eval)
            df["Industries"] = df["Industries"].apply(lambda x: x if isinstance(x, list) else [])

        # Ensure unique column names
        df.columns = pd.Series(df.columns).apply(lambda x: f"{x}_dup" if list(df.columns).count(x) > 1 else x)

        # Define editable and non-editable columns
        editable_columns = ["Total Donations", "Status"]
        disabled_columns = [col for col in df.columns if col not in editable_columns]
        status_options = ["", "Contacted", "Positive Response", "Negative Response", "Partnership"]

        df = df[df["Craftsmanship and production"] == "TRUE"]

        st.write("Editing data:")
        edited_df = st.data_editor(
            df,
            column_config={
                "Total Donations": st.column_config.NumberColumn(
                    "Total Donations",
                    help="Total amount of collected donations from Corporate in £",
                    min_value=0,
                    max_value=100000000,
                    step=1,
                    format="£ %d",
                ),
                "Status": st.column_config.SelectboxColumn(
                    label="Status",
                    options=status_options,
                    help="Select the current status of the corporate."
                ),
            },
            hide_index=True,
            disabled=disabled_columns,
            use_container_width=True
        )

        if st.button("Save Changes"):
            try:
                result = update_google_sheets_columns(sheet_id, range_name, editable_columns, edited_df)
                if result:
                    st.success("Changes saved successfully! Reloading data...")
                    st.rerun()
                else:
                    st.error("Failed to save changes.")
            except Exception as e:
                st.error(f"An error occurred while saving: {e}")

    except Exception as e:
        st.error(f"An error occurred: {e}")

render()
