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
    st.title("Community Development and Employment")
    st.markdown("**Project types**")
    st.write(''':blue-background[Bungalows and suites] :blue-background[Farmhouse Restaurant] :blue-background[Restaurant «Un»] :blue-background[Sanctuary Spa] :blue-background[Pool Bar and Lounge] :blue-background[Local Attractions]''')

    # Section: Slideshow
    st.markdown("**Pitchdeck Preview**")
    columns = st.columns(5)

    image_urls = [
        ["image_1.2.png", "image_6.png"],
        ["image_2.png", "image_7.png"],
        ["image_3.png", "image_8.png"],
        ["image_4.png", "image_9.png"],
        ["image_5.2.png", "image_10.png"]
    ]

    for col, urls in zip(columns, image_urls):
        for url in urls:
            col.image(
                f"https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/{url}",
                use_container_width=True
            )

    pptx_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/PitchDeck community development.pptx"
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
    
        # Define editable and non-editable columns
        editable_columns = ["Total Donations", "Status"]
        disabled_columns = [col for col in df.columns if col not in editable_columns]
        status_options = ["", "Contacted", "Positive Response", "Negative Response", "Partnership"]
        
        df = df[df["Community Development and Employment"] == "TRUE"]
        # Pass the full DataFrame to the editor
        st.write("Editing data:")
        edited_df = st.data_editor(
            df,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    pinned = True,
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
                "Craftsmanship and production": st.column_config.CheckboxColumn(
                    default=False,
                ),
                "Educational Development": st.column_config.CheckboxColumn(
                    default=False,
                ),
                "Community Development and Employment": st.column_config.CheckboxColumn(
                    default=False,
                ),
                "Emergency Relief and Basic Needs": st.column_config.CheckboxColumn(
                    default=False,
                ),
                "Food Security and Sustainable Agriculture": st.column_config.CheckboxColumn(
                    default=False,
                ),
                "EBIT": st.column_config.NumberColumn(
                    "EBIT (in mio.)",
                    help="Source: Pitchbook",
                    format="£ %d",
                ),
      
            },
            hide_index=True,
            disabled=disabled_columns,
            use_container_width=True
        )
    
        if st.button("Save Changes"):
            # Flatten lists to strings for saving to Google Sheets
            for col in edited_df.columns:
                if edited_df[col].apply(lambda x: isinstance(x, list)).any():
                    edited_df[col] = edited_df[col].apply(lambda x: "[" + ", ".join(map(lambda y: f"'{y}'", x)) + "]" if isinstance(x, list) else x)
    
            # Ensure numeric columns are stored as integers and handle NaN values
            numeric_columns = ["Total Donations"]
            for col in numeric_columns:
                if col in edited_df.columns:
                    edited_df[col] = pd.to_numeric(edited_df[col], errors='coerce').fillna(0).astype(int)

            # Ensure string columns are stored as strings and handle NaN values
            str_columns = ["Status"]
            for col in str_columns:
                if col in edited_df.columns:
                    # Convert to string type and replace NaN values with an empty string
                    edited_df[col] = edited_df[col].fillna("").astype(str)
            
            
            # Replace NaN and invalid values in other columns with empty strings
            edited_df = edited_df.fillna("")
    
            # Convert DataFrame to list of lists
            updated_values = [edited_df.columns.tolist()] + edited_df.values.tolist()
    
            try:
                result = update_google_sheets_data(sheet_id, range_name, updated_values)
                if result:
                    st.success("Changes saved successfully! Reloading data...")
                    st.rerun()
                else:
                    st.error("Failed to save changes.")
            except Exception as e:
                st.error(f"An error occurred while saving: {e}")

        st.link_button("Open Google Sheets", "https://docs.google.com/spreadsheets/d/1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY/edit?gid=0#gid=0")
    
    except Exception as e:
        st.error(f"An error occurred: {e}")

    st.markdown("**Matching Charities**")

    charity_sheet_id = "1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY"
    charity_range_name = "Charities"

    try:
        charity_df = fetch_google_sheets_data(charity_sheet_id, charity_range_name)

        charity_df = charity_df[charity_df["Focus"] == "Community Development and Employment"]   
        charity_df = charity_df.rename(columns={"charity_name": "Charity Name", "registered_charity_number": "Registered Charity Number", "latest_income": "Latest Income", "latest_expenditure": "Latest Expenditure", "charity_contact_email": "Charity Contact Email", "charity_activities": "Charity Activities"})

        editable_columns = ["Total Donations", "Status"]
        disabled_columns = [col for col in charity_df.columns if col not in editable_columns]
                
        edited_charity_df = st.data_editor(
            charity_df,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    pinned = True,
                    width="small",
                    help="Logos of companies"
                ),
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
                "Focus": st.column_config.ListColumn(
                    label="Focus",
                    help="List of SG focus area as tags"
                ),
                "Latest Income": st.column_config.NumberColumn(
                    "Latest Income (in thausand)",
                    format="£ %d"
                ),
                "Latest Expenditure": st.column_config.NumberColumn(
                    "Latest Expenditure (in thausand)",
                    format="£ %d"
                )
      
      
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
    
            numeric_columns = ["Total Donations"]
            for col in numeric_columns:
                if col in edited_charity_df.columns:
                    edited_charity_df[col] = pd.to_numeric(edited_charity_df[col], errors='coerce').fillna(0).astype(int)

            # Ensure string columns are stored as strings and handle NaN values
            str_columns = ["Status"]
            for col in str_columns:
                if col in edited_df.columns:
                    # Convert to string type and replace NaN values with an empty string
                    edited_df[col] = edited_df[col].fillna("").astype(str)

            
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
            
        st.link_button("Open Google Sheets", "https://docs.google.com/spreadsheets/d/1TPZ-lKKTrLK3TcG2r7ybl24Hy2SWLC2rhinpNRmjewY/edit?gid=217792113#gid=217792113")

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

render()
