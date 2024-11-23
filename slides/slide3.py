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
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920",
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920"
        ],
        captions=["Visual 1", "Visual 2", "Visual 3"]
    )
