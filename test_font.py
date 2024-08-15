import streamlit as st

# Load the custom CSS from style.css
with open("style.css") as css_file:
    st.markdown(f'<style>{css_file.read()}</style>', unsafe_allow_html=True)

# Your Streamlit app content
st.title("Custom Font Test")
st.write("This text should be rendered in the custom font 'UnitSlabOT-Bold'.")
