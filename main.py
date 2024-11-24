import streamlit as st
from slides import slide1, slide2, slide3, slide4, slide5

# Add a logo to the top of the sidebar
logo_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/logo_white.png" 
st.sidebar.image(logo_url, use_column_width=True)

# Sidebar for slide selection
st.sidebar.title("Navigation")
slides = [
    "Craftsmanship and production",
    "Educational Development",
    "Community Development and Employment",
    "Emergency Relief and Basic Needs",
    "Food Security and Sustainable Agriculture",
]
selected_slide = st.sidebar.radio("Choose a slide", slides)

# Render the selected slide
if selected_slide == slides[0]:
    slide1.render()
elif selected_slide == slides[1]:
    slide2.render()
elif selected_slide == slides[2]:
    slide3.render()
elif selected_slide == slides[3]:
    slide4.render()
elif selected_slide == slides[4]:
    slide5.render()
