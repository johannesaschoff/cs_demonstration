import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Community Development and Employment")
    st.markdown("**Project types**")
    st.write("- Bungalows and suites")
    st.write("- Farmhouse Restaurant")
    st.write("- Restaurant «Un»")
    st.write("- Sanctuary Spa")
    st.write("- Pool Bar and Lounge")
    st.write("- Local Attractions")

    display_slideshow(
        images=[
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
        captions=["Visual 1", "Visual 2", "Visual 3"]
    )
