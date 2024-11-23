import streamlit as st

# Sidebar for slide selection
st.sidebar.title("Navigation")
slides = ["Slide 1: Overview", 
          "Slide 2: Data Insights", 
          "Slide 3: Visualization", 
          "Slide 4: Analysis", 
          "Slide 5: Conclusion"]
selected_slide = st.sidebar.radio("Choose a slide", slides)

# Content for each slide
if selected_slide == slides[0]:
    st.title("Slide 1: Overview")
    st.markdown("**Category: Introduction**")
    st.write("- Welcome to the Overview slide.")
    st.write("- This slide introduces the topic.")
    st.write("- Provides a general summary.")
    st.write("- Prepares the user for the content ahead.")
    st.write("- Sets the stage for deeper dives into data.")
elif selected_slide == slides[1]:
    st.title("Slide 2: Data Insights")
    st.markdown("**Category: Key Data Points**")
    st.write("- Discuss significant data findings.")
    st.write("- Highlight trends in the dataset.")
    st.write("- Present supporting evidence.")
    st.write("- Describe the source of the data.")
    st.write("- Explain why these insights matter.")
elif selected_slide == slides[2]:
    st.title("Slide 3: Visualization")
    st.markdown("**Category: Visual Data Representation**")
    st.write("- Show relationships between variables.")
    st.write("- Provide clear visual aids.")
    st.write("- Simplify complex data into visuals.")
    st.write("- Highlight critical patterns.")
    st.write("- Engage the audience with interactive visuals.")
elif selected_slide == slides[3]:
    st.title("Slide 4: Analysis")
    st.markdown("**Category: Detailed Examination**")
    st.write("- Explore key questions about the data.")
    st.write("- Compare different outcomes.")
    st.write("- Explain the methods used in analysis.")
    st.write("- Present observations and conclusions.")
    st.write("- Discuss any limitations.")
elif selected_slide == slides[4]:
    st.title("Slide 5: Conclusion")
    st.markdown("**Category: Summary and Next Steps**")
    st.write("- Recap the main findings.")
    st.write("- Emphasize key takeaways.")
    st.write("- Suggest potential actions.")
    st.write("- Identify areas for further research.")
    st.write("- End with a strong closing statement.")
