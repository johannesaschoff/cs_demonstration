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
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920"
        ],
        captions=["Insight 1", "Insight 2", "Insight 3"]
    )
