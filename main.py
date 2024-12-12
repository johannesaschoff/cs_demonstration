import streamlit as st
from slides import slide1, slide2, slide3, slide4, slide5, slideKPI

st.set_page_config(layout="wide") 

# Add a logo to the top of the sidebar
logo_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/logo_grey.png" 
st.sidebar.image(logo_url, width=100)

# Sidebar for slide selection
st.sidebar.title("Navigation")
slides = [
    "Craftsmanship and production",
    "Educational Development",
    "Community Development and Employment",
    "Emergency Relief and Basic Needs",
    "Food Security and Sustainable Agriculture",
    "KPI"
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
elif selected_slide == slides[5]:
    slide5.render()
