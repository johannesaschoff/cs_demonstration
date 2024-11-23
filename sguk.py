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
    st.write("Welcome to the Overview slide. Here you can introduce your topic.")
elif selected_slide == slides[1]:
    st.title("Slide 2: Data Insights")
    st.write("This slide contains key data insights.")
    st.write("Add tables, summaries, or descriptions of your data.")
elif selected_slide == slides[2]:
    st.title("Slide 3: Visualization")
    st.write("Visualize your data here.")
    st.line_chart([1, 2, 3, 4, 5])  # Example visualization
elif selected_slide == slides[3]:
    st.title("Slide 4: Analysis")
    st.write("Perform detailed analysis here.")
    st.write("Include charts, explanations, and inferences.")
elif selected_slide == slides[4]:
    st.title("Slide 5: Conclusion")
    st.write("Summarize your findings here.")
    st.write("End with a call to action or final thoughts.")
