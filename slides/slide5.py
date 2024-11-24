import streamlit as st
import pandas as pd
import requests

# Function to fetch a company's logo using the Clearbit Logo API
@st.cache_data
def fetch_logo(company_name):
    # Replace spaces and special characters for URL compatibility
    company_name = company_name.split(" ")[0].replace(",", "").replace(".", "").replace("'", "").lower()
    logo_url = f"https://logo.clearbit.com/{company_name}.com"
    response = requests.get(logo_url)
    if response.status_code == 200:
        return logo_url  # Return the logo URL if the logo is found
    else:
        return None  # Return None if the logo is not available

# Function to add logos to the dataframe
@st.cache_data
def add_logos_to_dataframe(df):
    logo_urls = []
    for company in df["Company Name"]:
        logo_url = fetch_logo(company)
        if logo_url:
            logo_urls.append(logo_url)
        else:
            logo_urls.append("")  # Add an empty string if no logo is available
    df.insert(0, "Logo", logo_urls)  # Add the logo URLs as the first column
    return df

# Streamlit app
def render():
    st.title("Corporate Dataset with Logos")

    # Load CSV dataset
    csv_path = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates.csv"
    try:
        df = pd.read_csv(csv_path)

        # Add logos to the dataframe
        df_with_logos = add_logos_to_dataframe(df)

        # Display the dataframe with logos
        st.write("### Dataset with Company Logos")
        for index, row in df_with_logos.iterrows():
            logo = row["Logo"]
            company_name = row["Company Name"]
            industry = row["Industries"]
            ebit = row["EBIT"]
            st.markdown(
                f"""
                <div style="display: flex; align-items: center; margin-bottom: 10px;">
                    <img src="{logo}" style="height: 50px; margin-right: 10px;" alt="{company_name} Logo">
                    <div>
                        <strong>{company_name}</strong> <br>
                        Industry: {industry} <br>
                        EBIT: {ebit}
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Add a download button for the dataset
        csv_data = df.to_csv().encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=csv_data,
            file_name="corporate_dataset_with_logos.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Failed to load or process the dataset: {e}")

# Run the app
render()
