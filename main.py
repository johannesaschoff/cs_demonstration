import streamlit as st
from slides import slide1, slide2, slide3, slide4, slide5

# Add a logo to the top of the sidebar
logo_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/logo_grey.png"
st.sidebar.image(logo_url, width=100)

# Define icons for each slide
icons = [
    "🎨",  # Icon for "Craftsmanship and production"
    "📘",  # Icon for "Educational Development"
    "🏢",  # Icon for "Community Development and Employment"
    "🚑",  # Icon for "Emergency Relief and Basic Needs"
    "🌱"   # Icon for "Food Security and Sustainable Agriculture"
]

# Sidebar for slide selection
st.sidebar.title("Navigation")
slides = [
    "Craftsmanship and production",
    "Educational Development",
    "Community Development and Employment",
    "Emergency Relief and Basic Needs",
    "Food Security and Sustainable Agriculture"
]

# Create sidebar items with icons
styled_slides = [f"{icons[i]} {slides[i]}" for i in range(len(slides))]
selected_slide = st.sidebar.radio("Choose a slide", styled_slides)

# Determine which slide was selected (remove icon before comparison)
selected_index = styled_slides.index(selected_slide)

# Render the selected slide
if selected_index == 0:
    slide1.render()
elif selected_index == 1:
    slide2.render()
elif selected_index == 2:
    slide3.render()
elif selected_index == 3:
    slide4.render()
elif selected_index == 4:
    slide5.render()
