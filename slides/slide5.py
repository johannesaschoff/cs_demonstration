import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Food Security and Sustainable Agriculture")
    st.markdown("**Project types**")
    st.write("- Fruit and Vegetable Growing")
    st.write("- Cattle")
    st.write("- Chicken Farming")
    st.write("- Fish Farming")
    st.write("- Experimental Agriculture")

    # Display slideshow
    display_slideshow(
        images=[
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
    )

    # Raw URL for the PowerPoint file
    ppt_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/PitchDeck.pdf"

    # Add spacing control to reduce the margin
    st.markdown("<style>div.stButton {margin-top: -30px;}</style>", unsafe_allow_html=True)

    # Single button for downloading the file
    st.markdown(
        f"""
        <a href="{ppt_url}" download>
            <button style="padding:10px 20px; font-size:16px;">Download PowerPoint File</button>
        </a>
        """,
        unsafe_allow_html=True,
    )

# Run the function
render()
