import streamlit.components.v1 as components

def display_slideshow(images, captions):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    .mySlides {{display: none;}}
    .slideshow-container {{max-width: 1000px; margin: auto;}}
    .text {{color: #f2f2f2; font-size: 15px; position: absolute; bottom: 8px; width: 100%; text-align: center;}}
    .dot {{height: 15px; width: 15px; margin: 0 2px; background-color: #bbb; border-radius: 50%; display: inline-block; transition: background-color 0.6s ease;}}
    .active {{background-color: #717171;}}
    .fade {{animation-name: fade; animation-duration: 1.5s;}}
    @keyframes fade {{from {{opacity: .4}} to {{opacity: 1}}}}
    </style>
    </head>
    <body>
    <div class="slideshow-container">
    """
    for i, (image, caption) in enumerate(zip(images, captions), 1):
        html_code += f"""
        <div class="mySlides fade">
          <img src="{image}" style="width:100%">
          <div class="text">{caption}</div>
        </div>
        """
    html_code += """
    </div>
    <br><div style="text-align:center">
    """
    for _ in images:
        html_code += '<span class="dot"></span> '
    html_code += """
    </div>
    <script>
    let slideIndex = 0;
    showSlides();
    function showSlides() {{
      let slides = document.getElementsByClassName("mySlides");
      let dots = document.getElementsByClassName("dot");
      for (let i = 0; i < slides.length; i++) {{
        slides[i].style.display = "none";  
      }}
      slideIndex++;
      if (slideIndex > slides.length) {{slideIndex = 1}}    
      for (let i = 0; i < dots.length; i++) {{
        dots[i].className = dots[i].className.replace(" active", "");
      }}
      slides[slideIndex-1].style.display = "block";  
      dots[slideIndex-1].className += " active";
      setTimeout(showSlides, 2000);
    }}
    </script>
    </body>
    </html>
    """
    components.html(html_code, height=600)
