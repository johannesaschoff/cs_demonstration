import streamlit as st
import pandas as pd
import requests
import ast  


@st.cache_data
def fetch_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content  # Return the binary content of the PDF
    else:
        raise Exception(f"Failed to fetch the PDF. Status code: {response.status_code}")

def render():
    st.title("Community Development and Employment")
    st.markdown("**Project types**")
    st.write("- Bungalows and suites")
    st.write("- Farmhouse Restaurant")
    st.write("- Restaurant «Un»")
    st.write("- Sanctuary Spa")
    st.write("- Pool Bar and Lounge")
    st.write("- Local Attractions")

    # Section: Slideshow
    st.markdown("**Pitchdeck Preview**")
    columns = st.columns(3)

    with columns[0]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image4.png",
            use_column_width=True
        )

    with columns[1]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image5.png",
            use_column_width=True
        )

    with columns[2]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image6.png",
            use_column_width=True
        )
    # Section: PDF Download
    pdf_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/PitchDeck.pdf"
    try:
        pdf_data = fetch_pdf(pdf_url)
        st.download_button(
            label="Download PDF File",
            data=pdf_data,
            file_name="PitchDeck.pdf",
            mime="application/pdf",
        )
    except Exception as e:
        st.error(f"Could not fetch the PDF file: {e}")


    # Section: Corporate Dataset
    st.markdown("**Matching Corporates**")
    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates_with_logos.csv"

    try:
        # Load the dataset
        df = pd.read_csv(csv_url)
        df = df[df["Community Development and Employment"] == True]
        
        df["Industries"] = df["Industries"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)


        # Use Streamlit's column_config.ImageColumn for the Logo column
        st.dataframe(
            df,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    width="small",
                    help="Logos of companies"
                ),
                "Industries": st.column_config.ListColumn(
                    label="Industries",
                    help="List of industries represented as tags"
                )
            },
            hide_index=True,  # Optionally hide the index column
        )

        # Add a download button for the original dataset
        csv_data = pd.read_csv(csv_url).to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download data as CSV",
            data=csv_data,
            file_name="corporate_dataset_with_logos.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

#    dataframe charities
#    st.markdown("**Matching Charities**")
#    try:
#        Load the dataset
#        df = pd.read_csv(csv_education_url)

#         Use Streamlit's column_config.ImageColumn for the Logo column
#        st.dataframe(
#            df,
#            hide_index=True,  
#        )

        # Add a download button for the original dataset
#        csv_data = pd.read_csv(csv_education_url).to_csv(index=False).encode("utf-8")
#        st.download_button(
#            label="Download data as CSV",
#            data=csv_data,
#            file_name="charities_education.csv",
#            mime="text/csv",
#        )

#    except Exception as e:
#        st.error(f"Failed to load the dataset: {e}")
# Run the app

# Run the app
render()
