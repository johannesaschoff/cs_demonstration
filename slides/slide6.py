import streamlit as st

def render():
    st.title("Educational Development")
    st.markdown("**Project types**")
    st.write("- Teaching")
    st.write("- School Meals")
    st.write("- Hygiene")
    st.write("- Medical Care")
    st.write("- Musical Education")

    st.markdown("### Additional Images")
    columns = st.columns(3)

    with columns[0]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            use_column_width=True
        )

    with columns[1]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg",
            use_column_width=True
        )

    with columns[2]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
            use_column_width=True
        )
