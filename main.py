import streamlit as st

# GitHub image URL
image_url = "https://github.com/johannesaschoff/cs_demonstration/main/images/image1.jpg"

# Streamlit app
st.title("Display Image from GitHub")
st.image(image_url, caption="Image from GitHub", use_column_width=True)

st.write("This image is hosted on GitHub. Make sure the URL points to the raw version of the image.")
