import streamlit as st
import streamlit.components.v1 as components

# Function to declare and integrate the custom carousel component
def image_carousel():
    # Declare the custom component
    imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

    # List of images to display in the carousel
    imageUrls = [
        "https://images.unsplash.com/photo-1522093007474-d86e9bf7ba6f?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=764&q=80",
        "https://images.unsplash.com/photo-1610016302534-6f67f1c968d8?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=1075&q=80",
        "https://images.unsplash.com/photo-1516550893923-42d28e5677af?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=872&q=80",
        "https://images.unsplash.com/photo-1541343672885-9be56236302a?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8MHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=687&q=80",
    ]

    # Integrate the custom component
    selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=200)

    # Display the selected image
    if selectedImageUrl is not None:
        st.image(selectedImageUrl)

# Main function for the Streamlit app
def main():
    st.title("Image Carousel Example")

    st.write("Below is an example of an image carousel implemented as a custom Streamlit component.")

    # Display the carousel
    image_carousel()

# Run the app
if __name__ == "__main__":
    main()
