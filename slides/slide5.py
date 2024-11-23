import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Slide 5: Conclusion")
    st.markdown("**Category: Summary and Next Steps**")
    st.write("- Recap the main findings.")
    st.write("- Emphasize key takeaways.")
    st.write("- Suggest potential actions.")
    st.write("- Identify areas for further research.")
    st.write("- End with a strong closing statement.")
    display_slideshow(
        images=[
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920"
        ],
        captions=["Conclusion 1", "Conclusion 2", "Conclusion 3"]
    )
