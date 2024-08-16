import streamlit as st

# Load HTML content
with open('us_sectors.html', 'r') as file:
    html_content = file.read()

# Display HTML content in Streamlit
st.markdown(html_content, unsafe_allow_html=True)
