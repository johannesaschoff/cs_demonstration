import streamlit as st
import pandas as pd
import requests
import ast  

@st.cache_data
def fetch_pptx(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content 
    else:
        raise Exception(f"Failed to fetch the PPTX. Status code: {response.status_code}")

def render():
    st.title("Food Security and Sustainable Agriculture")

    # Section: Project Types
    st.markdown("**Project Types**")
    st.write("- Fruit and Vegetable Growing")
    st.write("- Cattle")
    st.write("- Chicken Farming")
    st.write("- Fish Farming")
    st.write("- Experimental Agriculture")

    # Section: Slideshow
    st.markdown("**Pitchdeck Preview**")
    columns = st.columns(6)

    with columns[0]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image7.png",
            use_column_width=True
        )

    with columns[1]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image2.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image8.png",
            use_column_width=True
        )

    with columns[2]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image3.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image9.png",
            use_column_width=True
        )

    with columns[3]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image4.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image10.png",
            use_column_width=True
        )

    with columns[4]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image5.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image11.png",
            use_column_width=True
        )

    with columns[5]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image6.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image12.png",
            use_column_width=True
        )
    # Section: PDF Download
    pptx_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/Pitch.pptx"
    try:
        pptx_data = fetch_pptx(pptx_url)
        st.download_button(
            label="Download PPTX File",
            data=pptx_data,
            file_name="PitchDeck.pptx",
            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
        )
    except Exception as e:
        st.error(f"Could not fetch the PPTX file: {e}")


    # Section: Corporate Dataset
    st.markdown("**Matching Corporates**")
    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates_with_logos.csv"
    excel_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/food_security_agriculture.xlsx"


    try:
        # Load the dataset
        df = pd.read_csv(csv_url)
        df = df[df["Food Security and Sustainable Agriculture"] == True]

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
        response = requests.get(excel_url)
        if response.status_code == 200:
            excel_data = response.content  # Get the file content as binary
    
            # Add a download button for the Excel file
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="Food_Security_and_Sustainable_Agriculture.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(f"Failed to fetch the Excel file. Status code: {response.status_code}")


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
