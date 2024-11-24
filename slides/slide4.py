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
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
        captions=["Analysis 1", "Analysis 2", "Analysis 3"]
    )

