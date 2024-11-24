import streamlit as st
import pandas as pd
import requests
from slides.utils import display_slideshow

# Function to fetch the PDF file as binary data
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
    st.write("### Pitchdeck Overview")
    st.markdown(
        """
        <style>
        .slideshow-container {
            margin-bottom: -20px; /* Reduces margin below the slideshow */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="slideshow-container">', unsafe_allow_html=True)
    display_slideshow(
        images=[
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg",
        ],
    )
    st.markdown('</div>', unsafe_allow_html=True)

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
        df = df[df["Food Security and Sustainable Agriculture"] == True]

        # Use Streamlit's column_config.ImageColumn for the Logo column
        st.dataframe(
            df,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    width="small",
                    help="Logos of companies"
                )
            },
            hide_index=True,  # Optionally hide the index column
        )

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
