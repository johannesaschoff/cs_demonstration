import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Educational Development")
    st.markdown("**Project types**")
    st.write("- Teaching")
    st.write("- School Meals")
    st.write("- Hygiene")
    st.write("- Medical Care")
    st.write("- Musical Education")

    display_slideshow(
        images=[
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
        captions=["Insight 1", "Insight 2", "Insight 3"]
    )
