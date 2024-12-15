import streamlit as st
from slides import slide11, slide12, slide13, slide14, slide15, dashboardKPI

st.set_page_config(layout="wide") 

# Add a logo to the top of the sidebar
logo_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/logo_grey.png" 
st.sidebar.image(logo_url, width=100)

# Sidebar for slide selection
st.sidebar.title("Navigation")
slides = [
    '''Educational Development''',
    '''Craftsmanship and production''',
    '''Community Development and Employment''',
    '''Emergency Relief and Basic Needs''',
    '''Food Security and Sustainable Agriculture''',
    '''KPI Dashboard'''
]
selected_slide = st.sidebar.radio("Choose a slide", slides)

# Render the selected slide
if selected_slide == slides[0]:
    slide12.render()
elif selected_slide == slides[1]:
    slide11.render()
elif selected_slide == slides[2]:
    slide13.render()
elif selected_slide == slides[3]:
    slide14.render()
elif selected_slide == slides[4]:
    slide15.render()
elif selected_slide == slides[5]:
    dashboardKPI.render()
