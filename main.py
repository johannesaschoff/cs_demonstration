import streamlit as st
from slides import slide1, slide2, slide3, slide4, slide5

# Add a logo to the top of the sidebar
logo_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/logo_grey.png"
st.sidebar.image(logo_url, width=100)

# Define icons and slides
icons = [
    "🎨",  # Icon for "Craftsmanship and production"
    "📘",  # Icon for "Educational Development"
    "🏢",  # Icon for "Community Development and Employment"
    "🚑",  # Icon for "Emergency Relief and Basic Needs"
    "🌱"   # Icon for "Food Security and Sustainable Agriculture"
]

slides = [
    "Craftsmanship and production",
    "Educational Development",
    "Community Development and Employment",
    "Emergency Relief and Basic Needs",
    "Food Security and Sustainable Agriculture"
]

# Sidebar for slide selection
st.sidebar.title("Navigation")

# Generate styled options with icons above the text
styled_slides = [
    f"""
    <div style="text-align: center; line-height: 1.5;">
        <span style="font-size: 2rem;">{icons[i]}</span><br>
        <span>{slides[i]}</span>
    </div>
    """
    for i in range(len(slides))
]

# Use `st.sidebar.radio` with HTML
selected_slide = st.sidebar.radio(
    "Choose a slide",
    slides,
    format_func=lambda x: slides[slides.index(x)]  # Keeps internal selection clean
)

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
