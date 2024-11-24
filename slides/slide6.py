import streamlit as st
from slides.utils import display_slideshow

def render():
    st.title("Educational Development")
    st.markdown("**Project types**")
    st.write("- Teaching")
    st.write("- School Meals")
    st.write("- Hygiene")
    st.write("- Medical Care")
    st.write("- Musical Education")

    with columns[0]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            caption="Caption 1",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            caption="Caption 2",
            use_column_width=True
        )

    with columns[1]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            caption="Caption 3",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg",
            caption="Caption 4",
            use_column_width=True
        )

    with columns[2]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg",
            caption="Caption 5",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            caption="Caption 6",
            use_column_width=True
        )
