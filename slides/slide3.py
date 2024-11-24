import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Slide 3: Visualization")
    st.markdown("**Category: Visual Data Representation**")
    st.write("- Show relationships between variables.")
    st.write("- Provide clear visual aids.")
    st.write("- Simplify complex data into visuals.")
    st.write("- Highlight critical patterns.")
    st.write("- Engage the audience with interactive visuals.")
    display_slideshow(
        images=[
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
        captions=["Visual 1", "Visual 2", "Visual 3"]
    )
