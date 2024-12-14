import streamlit as st
import pandas as pd
import requests
import ast

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
    st.write(''':blue-background[Butchery''')
    st.write(''':blue-background[Bakery''')
    st.write(''':blue-background[Kitchen''')
    st.write(''':blue-background[Woodwork''')
    st.write(''':blue-background[Sewing''')
    st.write(''':blue-background[Metal Construction Workshop''')

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
    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates_with_logos.csv"
    excel_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/craftmanship_production.xlsx"

    try:
        df = pd.read_csv(csv_url)
        df = df[df["Craftsmanship and production"] == True]
        df = df.rename(columns={"Contact Mail": "Contact Mail/Phone Nr./LinkedIn"})

        df["Industries"] = df["Industries"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

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
        response = requests.get(excel_url)
        if response.status_code == 200:
            excel_data = response.content
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="Craftsmanship_and_Production.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(f"Failed to fetch the Excel file. Status code: {response.status_code}")

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

    st.markdown("**Matching Charities**")
    csv_education_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/gesourcte_charities.csv"  # Fixed URL

    try:
        df = pd.read_csv(csv_education_url)
        df = df[df["area_id"] == 1]   
        df = df.drop(columns=["fitting area (1 / 0)", "area_id"])
        df = df.rename(columns={"charity_name": "Charity Name", "registered_charity_number": "Registered Charity Number", "latest_income": "Latest Income", "latest_expenditure": "Latest Expenditure", "charity_contact_email": "Charity Contact Email", "charity_activities": "Charity Activities"})
    
        st.dataframe(
            df,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    width="small",
                    help="Logos of companies"
                )
            },
            hide_index=True  
        )

        excel_url_charity = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/gesourcte_charities.xlsx"
        response = requests.get(excel_url_charity)
        if response.status_code == 200:
            excel_data = response.content
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="charities_sourcing.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(f"Failed to fetch the Excel file. Status code: {response.status_code}")

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")


render()
