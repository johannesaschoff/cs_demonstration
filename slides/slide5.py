import streamlit as st
import pandas as pd
import requests
import ast  

@st.cache_data
def fetch_pptx(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content 
    else:
        raise Exception(f"Failed to fetch the PPTX. Status code: {response.status_code}")

def render():
    st.title("Food Security and Sustainable Agriculture")

    # Section: Project Types
    st.markdown("**Project Types**")
    st.write("- Fruit and Vegetable Growing")
    st.write("- Cattle")
    st.write("- Chicken Farming")
    st.write("- Fish Farming")
    st.write("- Experimental Agriculture")

    # Section: Slideshow
    st.markdown("**Pitchdeck Preview**")
    columns = st.columns(5)

    image_urls = [
        ["image_1.4.png", "image_6.png"],
        ["image_2.png", "image_7.png"],
        ["image_3.png", "image_8.png"],
        ["image_4.png", "image_9.png"],
        ["image_5.4.png", "image_10.png"]
    ]

    for col, urls in zip(columns, image_urls):
        for url in urls:
            col.image(
                f"https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/{url}",
                use_container_width=True
            )


    # Section: PDF Download
    pptx_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/Pitch_2.pptx"
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
    excel_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/food_security_agriculture.xlsx"


    try:
        # Load the dataset
        df = pd.read_csv(csv_url)
        df = df[df["Food Security and Sustainable Agriculture"] == True]
        df = df.rename(columns={"Contact Mail": "Contact Mail/Phone Nr./LinkedIn"})

        df["Industries"] = df["Industries"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # Use Streamlit's column_config.ImageColumn for the Logo column
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
                    validate=r"^https?://.+", 
                    display_text="View Report" 
                )
            },
            hide_index=True,  # Optionally hide the index column
        )
        response = requests.get(excel_url)
        if response.status_code == 200:
            excel_data = response.content  # Get the file content as binary
    
            # Add a download button for the Excel file
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="Food_Security_and_Sustainable_Agriculture.xlsx",
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
        df = df[df["area_id"] == 5]   
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
