import streamlit as st
from slides import slide1, slide2, slide3, slide4, slide5

# Sidebar for slide selection
st.sidebar.title("Navigation")
slides = ["Slide 1: Overview", 
          "Slide 2: Data Insights", 
          "Slide 3: Visualization", 
          "Slide 4: Analysis", 
          "Slide 5: Conclusion"]
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
