import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Slide 4: Analysis")
    st.markdown("**Category: Detailed Examination**")
    st.write("- Explore key questions about the data.")
    st.write("- Compare different outcomes.")
    st.write("- Explain the methods used in analysis.")
    st.write("- Present observations and conclusions.")
    st.write("- Discuss any limitations.")
    display_slideshow(
        images=[
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920",
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920"
        ],
        captions=["Analysis 1", "Analysis 2", "Analysis 3"]
    )

