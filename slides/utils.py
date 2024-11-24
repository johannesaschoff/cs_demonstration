import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import time

# List of GitHub raw image URLs
image_urls = [
    "https://github.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
    "https://github.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
    "https://github.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
]

st.title("Image Slideshow from GitHub")

# Option for slideshow speed
slideshow_speed = st.slider("Select slideshow speed (seconds):", 1, 10, 3)

# Function to load an image from a URL
def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# Show slideshow
if st.button("Start Slideshow"):
    for url in image_urls:
        img = load_image(url)
        st.image(img, use_column_width=True)
        time.sleep(slideshow_speed)
