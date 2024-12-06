import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Streamlit page configuration
st.set_page_config(layout="wide")

# Load credentials from secrets
def authenticate_with_google():
    credentials_info = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(credentials_info)
    return credentials

@st.cache_data
def fetch_google_sheet(sheet_url):
    credentials = authenticate_with_google()
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(sheet_url).sheet1  # Access first sheet
    data = sheet.get_all_records()  # Fetch existing data
    return pd.DataFrame(data), sheet

def update_google_sheet(sheet, dataframe):
    try:
        # Prepare and write data
        rows = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
        sheet.clear()
        sheet.insert_rows(rows, row=1)
        st.success("Data successfully updated in Google Sheets!")
    except Exception as e:
        st.error(f"Error updating Google Sheet: {e}")

def render_app():
    st.title("Data Management with Google Sheets")

    # Fetch data from Google Sheets
    sheet_url = st.secrets["private_gsheets_url"]
    data, sheet = fetch_google_sheet(sheet_url)

    # Add a category column if it doesn't exist
    if "category" not in data.columns:
        data["category"] = ""

    # Interactive table with update feature
    edited_data = st.data_editor(
        data,
        column_config={
            "category": st.column_config.SelectboxColumn(
                "Category",
                options=["Option 1", "Option 2", "Option 3"],
                required=True,
            )
        },
        hide_index=True,
        use_container_width=True,
    )

    # Button to save changes
    if st.button("Save Changes"):
        update_google_sheet(sheet, edited_data)

# Run the app
if __name__ == "__main__":
    render_app()
