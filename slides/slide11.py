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

# Function to update data in Google Sheets
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
    
    
    st.markdown("**Matching Corporates**")
    corporate_sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"
    corporate_range_name = "Names"

    try:
        corporate_df = fetch_google_sheets_data(corporate_sheet_id, corporate_range_name)
        corporate_df = corporate_df.rename(columns={"Contact Mail": "Contact Mail/Phone Nr./LinkedIn"})

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
            if col in corporate_df.columns:  
                corporate_df[col] = corporate_df[col].apply(convert_to_boolean)

        corporate_df = corporate_df[corporate_df["Craftsmanship and production"] == True]
    
        def safe_literal_eval(x):
            try:
                return ast.literal_eval(x) if isinstance(x, str) else x
            except (ValueError, SyntaxError):
                logging.warning(f"Skipping invalid value: {x}")
                return []
    
        if "Industries" in corporate_df.columns:
            corporate_df["Industries"] = corporate_df["Industries"].apply(safe_literal_eval)
            corporate_df["Industries"] = corporate_df["Industries"].apply(lambda x: x if isinstance(x, list) else [])
    
        editable_columns = ["Total Donations", "Contacted", "Positive Response", "Negative Response", "Partnership"]
        disabled_columns = [col for col in corporate_df.columns if col not in editable_columns]
    
        edited_corporate_df = st.data_editor(
            corporate_df,
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
                    validate=r"^https?://.+",  # Basic validation for URLs
                    display_text="View Report"  # Display text for the links
                ),
                "Total Donations": st.column_config.NumberColumn(
                    "Total Donations (in CHF)",
                    help="Total amount of collected donations from Corporate in CHF",
                    min_value=0,
                    max_value=100000000,
                    step=1,
                    format="CHF%d",
                ),
                "Contacted": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=1,
                    step=1,
                ),
                "Positive Response": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=1,
                    step=1,
                ),
                "Negative Response": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=1,
                    step=1,
                ),
                "Partnership": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=1,
                    step=1,
                ),
            },
            hide_index=True,
            disabled=disabled_columns,
            use_container_width=True,
            key="corporate_data_editor"
        )
    
        if st.button("Save Changes", key="save_corporate_changes"):
            for col in edited_corporate_df.columns:
                if edited_corporate_df[col].apply(lambda x: isinstance(x, list)).any():
                    edited_corporate_df[col] = edited_corporate_df[col].apply(lambda x: "[" + ", ".join(map(lambda y: f"'{y}'", x)) + "]" if isinstance(x, list) else x)
    
            numeric_columns = ["Total Donations", "Contacted", "Positive Response", "Negative Response", "Partnership"]
            for col in numeric_columns:
                if col in edited_corporate_df.columns:
                    edited_corporate_df[col] = pd.to_numeric(edited_corporate_df[col], errors='coerce').fillna(0).astype(int)
            
            edited_corporate_df = edited_corporate_df.fillna("")
    
            updated_values = [edited_corporate_df.columns.tolist()] + edited_corporate_df.values.tolist()
    
            try:
                result = update_google_sheets_data(corporate_sheet_id, corporate_range_name, updated_values)
                if result:
                    st.success("Changes saved successfully! Reloading data...")
                    st.rerun()
                else:
                    st.error("Failed to save changes.")
            except Exception as e:
                st.error(f"An error occurred while saving: {e}")
    except Exception as e:
        st.error(f"An error occurred: {e}")

    st.markdown("**Matching Charities**")

    charity_sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"
    charity_range_name = "Charities"

    try:
        charity_df = fetch_google_sheets_data(charity_sheet_id, charity_range_name)
        charity_df["area_id"] = pd.to_numeric(charity_df["area_id"], errors="coerce")

        charity_df = charity_df[charity_df["area_id"] == 1]   
        charity_df = charity_df.rename(columns={"charity_name": "Charity Name", "registered_charity_number": "Registered Charity Number", "latest_income": "Latest Income", "latest_expenditure": "Latest Expenditure", "charity_contact_email": "Charity Contact Email", "charity_activities": "Charity Activities"})

        editable_columns = ["Total Donations", "Contacted", "Positive Response", "Negative Response", "Partnership"]
        disabled_columns = [col for col in charity_df.columns if col not in editable_columns]

        edited_charity_df = st.data_editor(
            charity_df,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    width="small",
                    help="Logos of companies"
                ),
                "Total Donations": st.column_config.NumberColumn(
                    "Total Donations (in CHF)",
                    help="Total amount of collected donations from Corporate in CHF",
                    min_value=0,
                    max_value=100000000,
                    step=1,
                    format="CHF%d",
                ),
                "Contacted": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=1,
                    step=1,
                ),
                "Positive Response": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=1,
                    step=1,
                ),
                "Negative Response": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=1,
                    step=1,
                ),
                "Partnership": st.column_config.NumberColumn(
                    min_value=0,
                    max_value=1,
                    step=1,
                ),
            },
            hide_index=True,
            disabled=disabled_columns,
            use_container_width=True,
            key="charity_data_editor"
        )

        if st.button("Save Changes", key="save_charity_changes"):
            for col in edited_charity_df.columns:
                if edited_charity_df[col].apply(lambda x: isinstance(x, list)).any():
                    edited_charity_df[col] = edited_charity_df[col].apply(lambda x: "[" + ", ".join(map(lambda y: f"'{y}'", x)) + "]" if isinstance(x, list) else x)
    
            numeric_columns = ["Total Donations", "Contacted", "Positive Response", "Negative Response", "Partnership"]
            for col in numeric_columns:
                if col in edited_charity_df.columns:
                    edited_charity_df[col] = pd.to_numeric(edited_charity_df[col], errors='coerce').fillna(0).astype(int)
            
            edited_charity_df = edited_charity_df.fillna("")
    
            updated_values = [edited_charity_df.columns.tolist()] + edited_charity_df.values.tolist()
    
            try:
                result = update_google_sheets_data(charity_sheet_id, charity_range_name, updated_values)
                if result:
                    st.success("Changes saved successfully! Reloading data...")
                    st.rerun()
                else:
                    st.error("Failed to save changes.")
            except Exception as e:
                st.error(f"An error occurred while saving: {e}")
    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

render()
