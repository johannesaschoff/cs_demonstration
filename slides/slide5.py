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
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg"
        ],
        captions=["Conclusion 1", "Conclusion 2", "Conclusion 3"]
    )
