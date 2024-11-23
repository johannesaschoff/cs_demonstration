import streamlit as st
import streamlit.components.v1 as components

# Sidebar for slide selection
st.sidebar.title("Navigation")
slides = ["Slide 1: Overview", 
          "Slide 2: Data Insights", 
          "Slide 3: Visualization", 
          "Slide 4: Analysis", 
          "Slide 5: Conclusion"]
selected_slide = st.sidebar.radio("Choose a slide", slides)

# Slideshow HTML template
def display_slideshow(images, captions):
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
    * {{box-sizing: border-box;}}
    body {{font-family: Verdana, sans-serif;}}
    .mySlides {{display: none;}}
    img {{vertical-align: middle;}}

    .slideshow-container {{
      max-width: 1000px;
      position: relative;
      margin: auto;
    }}

    .text {{
      color: #f2f2f2;
      font-size: 15px;
      padding: 8px 12px;
      position: absolute;
      bottom: 8px;
      width: 100%;
      text-align: center;
    }}

    .numbertext {{
      color: #f2f2f2;
      font-size: 12px;
      padding: 8px 12px;
      position: absolute;
      top: 0;
    }}

    .dot {{
      height: 15px;
      width: 15px;
      margin: 0 2px;
      background-color: #bbb;
      border-radius: 50%;
      display: inline-block;
      transition: background-color 0.6s ease;
    }}

    .active {{
      background-color: #717171;
    }}

    .fade {{
      animation-name: fade;
      animation-duration: 1.5s;
    }}

    @keyframes fade {{
      from {{opacity: .4}} 
      to {{opacity: 1}}
    }}

    @media only screen and (max-width: 300px) {{
      .text {{font-size: 11px}}
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
          <img src="{image}" style="width:100%">
          <div class="text">{caption}</div>
        </div>
        """
    html_code += """
    </div>
    <br>
    <div style="text-align:center">
    """
    for _ in images:
        html_code += '<span class="dot"></span> '
    html_code += """
    </div>

    <script>
    let slideIndex = 0;
    showSlides();

    function showSlides() {{
      let i;
      let slides = document.getElementsByClassName("mySlides");
      let dots = document.getElementsByClassName("dot");
      for (i = 0; i < slides.length; i++) {{
        slides[i].style.display = "none";  
      }}
      slideIndex++;
      if (slideIndex > slides.length) {{slideIndex = 1}}    
      for (i = 0; i < dots.length; i++) {{
        dots[i].className = dots[i].className.replace(" active", "");
      }}
      slides[slideIndex-1].style.display = "block";  
      dots[slideIndex-1].className += " active";
      setTimeout(showSlides, 2000); // Change image every 2 seconds
    }}
    </script>

    </body>
    </html>
    """
    components.html(html_code, height=600)

# Content for each slide
if selected_slide == slides[0]:
    st.title("Slide 1: Overview")
    st.markdown("**Category: Introduction**")
    st.write("- Welcome to the Overview slide.")
    st.write("- This slide introduces the topic.")
    st.write("- Provides a general summary.")
    st.write("- Prepares the user for the content ahead.")
    st.write("- Sets the stage for deeper dives into data.")
    display_slideshow(
        images=[
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920"
        ],
        captions=["Caption 1", "Caption 2", "Caption 3"]
    )
elif selected_slide == slides[1]:
    st.title("Slide 2: Data Insights")
    st.markdown("**Category: Key Data Points**")
    st.write("- Discuss significant data findings.")
    st.write("- Highlight trends in the dataset.")
    st.write("- Present supporting evidence.")
    st.write("- Describe the source of the data.")
    st.write("- Explain why these insights matter.")
    display_slideshow(
        images=[
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920"
        ],
        captions=["Insight 1", "Insight 2", "Insight 3"]
    )
elif selected_slide == slides[2]:
    st.title("Slide 3: Visualization")
    st.markdown("**Category: Visual Data Representation**")
    st.write("- Show relationships between variables.")
    st.write("- Provide clear visual aids.")
    st.write("- Simplify complex data into visuals.")
    st.write("- Highlight critical patterns.")
    st.write("- Engage the audience with interactive visuals.")
    display_slideshow(
        images=[
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920",
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920"
        ],
        captions=["Visual 1", "Visual 2", "Visual 3"]
    )
elif selected_slide == slides[3]:
    st.title("Slide 4: Analysis")
    st.markdown("**Category: Detailed Examination**")
    st.write("- Explore key questions about the data.")
    st.write("- Compare different outcomes.")
    st.write("- Explain the methods used in analysis.")
    st.write("- Present observations and conclusions.")
    st.write("- Discuss any limitations.")
    display_slideshow(
        images=[
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920",
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920"
        ],
        captions=["Analysis 1", "Analysis 2", "Analysis 3"]
    )
elif selected_slide == slides[4]:
    st.title("Slide 5: Conclusion")
    st.markdown("**Category: Summary and Next Steps**")
    st.write("- Recap the main findings.")
    st.write("- Emphasize key takeaways.")
    st.write("- Suggest potential actions.")
    st.write("- Identify areas for further research.")
    st.write("- End with a strong closing statement.")
    display_slideshow(
        images=[
            "https://unsplash.com/photos/GJ8ZQV7eGmU/download?force=true&w=1920",
            "https://unsplash.com/photos/eHlVZcSrjfg/download?force=true&w=1920",
            "https://unsplash.com/photos/zVhYcSjd7-Q/download?force=true&w=1920"
        ],
        captions=["Conclusion 1", "Conclusion 2", "Conclusion 3"]
    )
