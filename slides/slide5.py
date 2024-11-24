import streamlit as st
import pandas as pd
import requests
from slides.utils import display_slideshow

# Function to render the HTML code for displaying an image
def show_image_from_url(image_url):
    return f'<img src="{image_url}" style="height:50px;">'

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

    # Section: Project Types
    st.markdown("**Project Types**")
    st.write("- Fruit and Vegetable Growing")
    st.write("- Cattle")
    st.write("- Chicken Farming")
    st.write("- Fish Farming")
    st.write("- Experimental Agriculture")

    # Section: Slideshow
    st.write("### Slideshow")
    display_slideshow(
        images=[
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
    )

    # Section: PDF Download
    st.write("### Downloadable Resources")
    pdf_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/PitchDeck.pdf"
    try:
        pdf_data = fetch_pdf(pdf_url)
        st.download_button(
            label="Download PDF File",
            data=pdf_data,
            file_name="PitchDeck.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Could not fetch the PDF file: {e}")

    # Section: Corporate Dataset
    st.write("### Corporate Dataset with Logos")
    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates_with_logos.csv"

    try:
        # Load the dataset
        df = pd.read_csv(csv_url)

        # Add a new column with HTML-rendered images
        df["Logo"] = df["Logo"].apply(show_image_from_url)

        # Convert the dataframe to an HTML table with the rendered logos
        html_table = df.to_html(escape=False, index=False)

        # Display the dataframe as an HTML table
        st.markdown(html_table, unsafe_allow_html=True)

        # Add a download button for the original dataset
        csv_data = pd.read_csv(csv_url).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=csv_data,
            file_name="corporate_dataset_with_logos.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

# Run the app
render()
