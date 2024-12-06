import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Set page configuration
st.set_page_config(layout="wide")

# Google Sheets configuration
SHEET_URL = "https://docs.google.com/spreadsheets/d/1pqJjuQCt28LayLeRne8eZu8e356I1q6NWUzBABsNqeU/edit?usp=sharing"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

@st.cache_data
def authenticate_and_fetch(sheet_url):
    """
    Authenticate with Google Sheets API and fetch the sheet data.
    """
    credentials_dict = st.secrets["GOOGLE_CREDENTIALS"]
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=SCOPES)

    gc = gspread.authorize(credentials)
    sheet = gc.open_by_url(sheet_url).sheet1
    
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
    return df, sheet

def update_sheet(sheet, dataframe):
    """
    Update the Google Sheet with new data from the DataFrame.
    """
    data = [dataframe.columns.values.tolist()] + dataframe.values.tolist()
    sheet.clear()
    sheet.insert_rows(data, row=1)

def render():
    try:
        st.title("Craftsmanship and Production")

        df, sheet = authenticate_and_fetch(SHEET_URL)

        if "category" not in df.columns:
            df["category"] = ""

        # Manage real-time updates
        def on_change_callback():
            st.session_state["dataframe"] = st.session_state["edited_df"]
            update_sheet(sheet, st.session_state["dataframe"])
            st.success("Google Sheet updated automatically!")

        if "dataframe" not in st.session_state:
            st.session_state["dataframe"] = df

        st.session_state["edited_df"] = st.data_editor(
            st.session_state["dataframe"],
            column_config={
                "category": st.column_config.SelectboxColumn(
                    "App Category",
                    help="The category of the app",
                    width="medium",
                    options=["📊 Data Exploration", "📈 Data Visualization", "🤖 LLM"],
                    required=True,
                )
            },
            hide_index=True,
            on_change=on_change_callback,
            use_container_width=True,
        )

    except Exception as e:
        st.error(f"An error occurred: {e}")

render()
