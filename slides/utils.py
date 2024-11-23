import streamlit.components.v1 as components

def display_slideshow(images, captions):
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
        border-radius: 15px;
        overflow: hidden;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }}
    .mySlides {{
        display: none;
        border-radius: 15px;
    }}
    .prev, .next {{
        cursor: pointer;
        position: absolute;
        top: 50%;
        width: auto;
        padding: 16px;
        margin-top: -22px;
        color: white;
        font-weight: bold;
        font-size: 18px;
        transition: 0.6s ease;
        user-select: none;
    }}
    .next {{
        right: 0;
        border-radius: 3px 0 0 3px;
    }}
    .prev {{
        left: 0;
        border-radius: 0 3px 3px 0;
    }}
    .text {{
        color: #ffffff;
        font-size: 16px;
        padding: 8px 12px;
        position: absolute;
        bottom: 10px;
        width: 100%;
        text-align: center;
        background: rgba(0, 0, 0, 0.5);
        border-radius: 0 0 15px 15px;
    }}
    .dot {{
        height: 12px;
        width: 12px;
        margin: 0 2px;
        background-color: #bbb;
        border-radius: 50%;
        display: inline-block;
        transition: background-color 0.6s ease;
    }}
    .active {{
        background-color: #717171;
    }}
    </style>
    </head>
    <body>

    <div class="slideshow-container">
    """
    for i, (image, caption) in enumerate(zip(images, captions), 1):
        html_code += f"""
        <div class="mySlides fade">
          <div class="numbertext">{i} / {len(images)}</div>
          <img src="{image}" style="width:100%; border-radius: 15px;">
          <div class="text">{caption}</div>
        </div>
        """
    html_code += """
    <a class="prev" onclick="plusSlides(-1)">&#10094;</a>
    <a class="next" onclick="plusSlides(1)">&#10095;</a>
    </div>
    <br>
    <div style="text-align:center">
    """
    for _ in images:
        html_code += '<span class="dot"></span> '
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
