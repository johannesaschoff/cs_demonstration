import streamlit as st
import requests  # To fetch the PDF file from the web
import pandas as pd
from slides.utils import display_slideshow

# Function to download the PDF file as binary data
@st.cache_data
def fetch_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content  # Return the binary content of the PDF
    else:
        raise Exception(f"Failed to fetch the PDF. Status code: {response.status_code}")

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

    # PDF file URL
    pdf_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/PitchDeck.pdf"

    try:
        # Fetch the PDF binary data
        pdf_data = fetch_pdf(pdf_url)

        # Streamlit-native download button for the PDF file
        st.download_button(
            label="Download PDF File",
            data=pdf_data,
            file_name="PitchDeck.pdf",
            mime="application/pdf",
        )

    except Exception as e:
        st.error(f"Could not fetch the PDF file: {e}")

    # Load CSV from GitHub
    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates.csv"
    try:
        df = pd.read_csv(csv_url)  # Load the CSV file
        st.write("### Corporate Dataset")
        st.dataframe(df)  # Display the dataframe in Streamlit

        # Add a download button for the dataframe
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
