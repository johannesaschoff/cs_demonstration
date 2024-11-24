import streamlit as st
from slides.utils import display_slideshow
import pandas as pd

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

    # Add custom CSS to reduce margins
    st.markdown(
        """
        <style>
        .stMarkdown {
            margin-bottom: -30px; /* Adjust this value to fine-tune spacing */
        }
        div.stButton > button {
            margin-top: -40px; /* Moves button closer to the slideshow */
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Raw URL for the PowerPoint file
    ppt_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/PitchDeck.pdf"

    # Single button for downloading the file
    st.markdown(
        f"""
        <a href="{ppt_url}" download>
            <button style="padding:10px 20px; font-size:16px;">Download PowerPoint File</button>
        </a>
        """,
        unsafe_allow_html=True,
    )

    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates.csv"
    try:
        df = pd.read_csv(csv_url)  # Load the CSV file
        st.write("### Corporate Dataset")
        st.dataframe(df)  # Display the dataframe in Streamlit
    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

# Run the function
render()
