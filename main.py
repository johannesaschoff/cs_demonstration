import streamlit as st

# List of GitHub raw image URLs
image_urls = [
    "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.jpg",
    "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.jpg",
    "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.jpg",
]

# Streamlit app
st.title("Image Gallery")

# Slider for navigation
current_image_index = st.slider(
    "Navigate through the images:",
    min_value=0,
    max_value=len(image_urls) - 1,
    step=1,
    format="Image %d",
)

# Display the current image
st.image(
    image_urls[current_image_index],
    caption=f"Image {current_image_index + 1}",
    use_column_width=True,
)
