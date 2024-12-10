import streamlit as st
import pandas as pd
import requests
import ast  


@st.cache_data
def fetch_pptx(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content  # Return the binary content of the PDF
    else:
        raise Exception(f"Failed to fetch the pptx. Status code: {response.status_code}")

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
    columns = st.columns(5)

    with columns[0]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_1.2.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_6.png",
            use_column_width=True
        )

    with columns[1]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_2.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_7.png",
            use_column_width=True
        )

    with columns[2]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_3.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_8.png",
            use_column_width=True
        )

    with columns[3]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_4.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_9.png",
            use_column_width=True
        )

    with columns[4]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_5.2.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image_10.png",
            use_column_width=True
        )


    # Section: PDF Download
    pptx_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/Pitch_2.pptx"
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
    excel_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/community_employment.xlsx"

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
                ),
                "Sustainability report": st.column_config.LinkColumn(
                    label="Sustainability Report",
                    help="Link to the company's sustainability report",
                    validate=r"^https?://.+",  
                    display_text="View Report" 
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
                file_name="Community_Development_and_Employment.xlsx",
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
