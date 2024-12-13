import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import ast
import requests
import logging

st.set_page_config(layout="wide")


@st.cache_data
def fetch_pptx(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch the PPTX. Status code: {response.status_code}")

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

    # Section: Corporate Dataset
    st.markdown("**Matching Corporates**")

        # Fetch data directly without caching
    def fetch_data(x):
        conn = st.connection("gsheets", type=GSheetsConnection)
        return conn.read(worksheet = x)


    df= fetch_data("Names")
    df = pd.DataFrame(data = df)
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
            if value.strip().upper() == "WAHR":  # Check if the value is "WAHR"
                return True
            elif value.strip().upper() == "FALSCH":  # Check if the value is "FALSCH"
                return False
        return None  # Return None for other cases

    # Apply the function to all specified columns
    for col in columns_to_process:
        if col in df.columns:  # Check if the column exists in the DataFrame
            df[col] = df[col].apply(convert_to_boolean)

    df = df[df["Craftsmanship and production"] == True]


    st.dataframe(
        df,
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
            )
        },
        hide_index=True,
        use_container_width=True
    )


    df_char= fetch_data("Charities")
    df_char = pd.DataFrame(data = df_char)

    df_char = df_char[df_char["area_id"] == 1]   
    df_char = df_char.drop(columns=["fitting area (1 / 0)", "area_id"])
    df_char = df_char.rename(columns={"charity_name": "Charity Name", "registered_charity_number": "Registered Charity Number", "latest_income": "Latest Income", "latest_expenditure": "Latest Expenditure", "charity_contact_email": "Charity Contact Email", "charity_activities": "Charity Activities"})

    st.dataframe(
        df_char,
        column_config={
            "Logo": st.column_config.ImageColumn(
                label="Company Logo",
                width="small",
                help="Logos of companies"
            )
        },
        hide_index=True  
    )


render()
