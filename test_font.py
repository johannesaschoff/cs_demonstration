import streamlit as st
import streamlit.components.v1 as components

# Set the page configuration to full width
st.set_page_config(layout="wide")

# Define the HTML content that tests the custom font
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Font Test</title>
    <style>
    @font-face {
        font-family: 'UnitSlabOT-Bold';
        src: url('https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/fonts/UnitSlabOT-Bold.otf') format('opentype');
        font-weight: normal;
        font-style: normal;
    }

    body {
        font-family: 'UnitSlabOT-Bold', sans-serif;
        margin: 40px;
    }

    h1 {
        font-family: 'UnitSlabOT-Bold';
        font-size: 36px;
        color: #333;
    }

    p {
        font-family: 'UnitSlabOT-Bold';
        font-size: 18px;
        color: #666;
    }
    </style>
</head>
<body>
    <h1>Custom Font Test</h1>
    <p>This text is rendered using the 'UnitSlabOT-Bold' font.</p>
</body>
</html>
"""

# Embed the HTML content in Streamlit
components.html(html_content, height=200)

st.write("If the above text is displayed with the custom font, the test is successful.")
