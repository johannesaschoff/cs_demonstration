import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Slide 2: Data Insights")
    st.markdown("**Category: Key Data Points**")
    st.write("- Discuss significant data findings.")
    st.write("- Highlight trends in the dataset.")
    st.write("- Present supporting evidence.")
    st.write("- Describe the source of the data.")
    st.write("- Explain why these insights matter.")
    display_slideshow(
        images=[
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920"
        ],
        captions=["Insight 1", "Insight 2", "Insight 3"]
    )
