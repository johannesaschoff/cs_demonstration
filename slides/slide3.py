import streamlit as st
import pandas as pd
import requests

@st.cache_data
def fetch_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content  # Return the binary content of the PDF
    else:
        raise Exception(f"Failed to fetch the PDF. Status code: {response.status_code}")

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
