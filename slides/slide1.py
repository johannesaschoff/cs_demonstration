import streamlit as st
import streamlit.components.v1 as components
from slides.utils import display_slideshow

def render():
    st.title("Slide 1: Overview")
    st.markdown("**Category: Introduction**")
    st.write("- Welcome to the Overview slide.")
    st.write("- This slide introduces the topic.")
    st.write("- Provides a general summary.")
    st.write("- Prepares the user for the content ahead.")
    st.write("- Sets the stage for deeper dives into data.")
    display_slideshow(
        images=[
            "https://github.com/johannesaschoff/cs_demonstration/blob/4010f37ca53b5861a2bd43c853a7c4f596549e77/slides/image1.png",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920"
        ],
        captions=["Caption 1", "Caption 2", "Caption 3"]
    )
