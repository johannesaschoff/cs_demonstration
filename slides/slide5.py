import streamlit as st
import pandas as pd
import requests
from slides.utils import display_slideshow

# Function to fetch a company's logo using the Clearbit Logo API
@st.cache_data
def fetch_logo(company_name):
    # Replace spaces with dashes for URL compatibility
    company_name = company_name.replace(" ", "-")
    logo_url = f"https://logo.clearbit.com/{company_name}.com"
    response = requests.get(logo_url)
    if response.status_code == 200:
        return logo_url  # Return the logo URL if the logo is found
    else:
        return None  # Return None if the logo is not available

# Function to fetch and add logos to the dataframe
@st.cache_data
def add_logos_to_dataframe(df):
    logo_urls = []
    for company in df["company name"]:
        logo_url = fetch_logo(company)
        if logo_url:
            logo_urls.append(logo_url)
        else:
            logo_urls.append("")  # Add an empty string if no logo is available
    df.insert(0, "Logo", logo_urls)  # Add the logo URLs as the first column
    return df

def render():
    st.title("Food Security and Sustainable Agriculture")
    st.markdown("**Project types**")
    st.write("- Fruit and Vegetable Growing")
    st.write("- Cattle")
    st.write("- Chicken Farming")
    st.write("- Fish Farming")
    st.write("- Experimental Agriculture")

    # Display slideshow
    display_slideshow(
        images=[
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
    )

    # Load CSV from GitHub
    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates.csv"
    try:
        df = pd.read_csv(csv_url)  # Load the CSV file

        # Add logos to the dataframe
        df_with_logos = add_logos_to_dataframe(df)

        # Display dataframe with logos
        st.write("### Corporate Dataset with Logos")
        for index, row in df_with_logos.iterrows():
            logo = row["Logo"]
            company_name = row["company name"]
            # Display logo with company name
            st.markdown(
                f"""
                <div style="display: flex; align-items: center;">
                    <img src="{logo}" style="height: 50px; margin-right: 10px;" alt="{company_name} Logo">
                    <span>{company_name}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Add a download button for the original dataframe
        csv_data = df.to_csv().encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=csv_data,
            file_name="corporate_dataset.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

# Run the function
render()
