import streamlit as st
import pandas as pd
import requests
import io


@st.cache_data
def fetch_pdf(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content  # Return the binary content of the PDF
    else:
        raise Exception(f"Failed to fetch the PDF. Status code: {response.status_code}")


def render():
    st.title("Craftsmanship and production")
    st.markdown("**Project types**")
    st.write("- Butchery")
    st.write("- Bakery")
    st.write("- Kitchen")
    st.write("- Woodwork")
    st.write("- Sewing")
    st.write("- Metal Construction Workshop")

    # Section: Slideshow
    st.markdown("**Pitchdeck Preview**")
    columns = st.columns(3)

    with columns[0]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.1.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.4.png",
            use_column_width=True
        )

    with columns[1]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.2.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.5.png",
            use_column_width=True
        )

    with columns[2]:
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.3.png",
            use_column_width=True
        )
        st.image(
            "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/images/image1.6.png",
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
        df = df[df["Craftsmanship and production"] == True]

        # Use Streamlit's column_config.ImageColumn for the Logo column
        st.dataframe(
            df,
            column_config={
                "Logo": st.column_config.ImageColumn(
                    label="Company Logo",
                    width="small",
                    help="Logos of companies"
                )
            },
            hide_index=True,  # Optionally hide the index column
        )

        # Add a download button for the original dataset
        excel_buffer = io.BytesIO()
        df.to_excel(excel_buffer, index=False, engine='openpyxl')
        excel_buffer.seek(0)  # Move the buffer's cursor to the beginning
        st.download_button(
            label="Download data as Excel",
            data=excel_buffer,
            file_name="corporate_dataset_with_logos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

# Run the app
render()
