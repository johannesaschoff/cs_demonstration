import streamlit.components.v1 as components

def display_slideshow(images):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body {{
        font-family: 'Arial', sans-serif;
    }}
    .slideshow-container {{
        max-width: 1000px;
        margin: auto;
        position: relative;
        overflow: hidden;
        background-color: transparent; /* Transparent background */
        border-radius: 15px; /* Rounded corners for the entire slideshow container */
    }}
    .mySlides {{
        display: none;
    }}
    .mySlides img {{
        width: 100%;
        border-radius: 15px; /* Rounded corners for images */
    }}
    .prev, .next {{
        cursor: pointer;
        position: absolute;
        top: 50%;
        width: 40px; /* Fixed width for circular arrows */
        height: 40px; /* Fixed height for circular arrows */
        padding: 0; /* Remove extra padding */
        margin-top: -20px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        transition: 0.6s ease;
        user-select: none;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 50%; /* Make the arrows circular */
        text-align: center;
        line-height: 40px; /* Center the arrow symbol vertically */
    }}
    .next {{
        right: 10px;
    }}
    .prev {{
        left: 10px;
    }}
    .dot {{
        height: 12px;
        width: 12px;
        margin: 0 4px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
        transition: background-color 0.6s ease;
        cursor: pointer;
    }}
    .active {{
        background-color: #717171;
    }}
    </style>
    </head>
    <body>

    <div class="slideshow-container">
    """
    for i, image in enumerate(images, 1):
        html_code += f"""
        <div class="mySlides">
          <img src="{image}">
        </div>
        """
    html_code += """
    <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
    <a class="next" onclick="plusSlides(1)">&#10095;</a>
    </div>
    <br>
    <div style="text-align:center">
    """
    for idx in range(len(images)):
        html_code += f'<span class="dot" onclick="currentSlide({idx+1})"></span>'
    html_code += """
    </div>

    <script>
    let slideIndex = 1;
    showSlides(slideIndex);

    function plusSlides(n) {{
      showSlides(slideIndex += n);
    }}

    function currentSlide(n) {{
      showSlides(slideIndex = n);
    }}

    function showSlides(n) {{
      let i;
      let slides = document.getElementsByClassName("mySlides");
      let dots = document.getElementsByClassName("dot");
      if (n > slides.length) {{slideIndex = 1}}
      if (n < 1) {{slideIndex = slides.length}}
      for (i = 0; i < slides.length; i++) {{
        slides[i].style.display = "none";
      }}
      for (i = 0; i < dots.length; i++) {{
        dots[i].className = dots[i].className.replace(" active", "");
      }}
      slides[slideIndex-1].style.display = "block";
      dots[slideIndex-1].className += " active";
    }}
    </script>

    </body>
    </html>
    """
    components.html(html_code, height=600)
