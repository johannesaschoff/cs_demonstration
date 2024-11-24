import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Emergency Relief and Basic Needs")
    st.markdown("**Category: Detailed Examination**")
    st.write("- Food")
    st.write("- Medicine")
    st.write("- Water Pumps")

    display_slideshow(
        images=[
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
        captions=["Analysis 1", "Analysis 2", "Analysis 3"]
    )

