import streamlit as st
import streamlit.components.v1 as components

# Set the page configuration
st.set_page_config(layout="wide")

# Define the HTML content that uses the custom font
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <style>
    @font-face {
        font-family: 'UnitSlabOT-Bold';
        src: url('/static/UnitSlabOT-Bold.otf') format('opentype');
    }
    body {
        font-family: 'UnitSlabOT-Bold', sans-serif;
    }
    </style>
</head>
<body>
    <h1>This is a test of the custom font</h1>
    <p>This text should be rendered in 'UnitSlabOT-Bold' font.</p>
</body>
</html>
"""

# Render the HTML in Streamlit
components.html(html_content, height=200)

st.write("If the above text is displayed with the custom font, the test is successful.")
