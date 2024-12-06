import streamlit as st
import pandas as pd
import requests
import ast

st.set_page_config(layout="wide")

@st.cache_data
def fetch_pptx(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to fetch the PPTX. Status code: {response.status_code}")

def render():
    st.title("Craftsmanship and Production")
    st.markdown("**Project types**")
    st.write("- Butchery")
    st.write("- Bakery")
    st.write("- Kitchen")
    st.write("- Woodwork")
    st.write("- Sewing")
    st.write("- Metal Construction Workshop")

    # Section: Slideshow
    st.markdown("**Pitchdeck Preview**")
    columns = st.columns(6)

    # (Column images code remains unchanged)

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
    excel_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/craftmanship_production.xlsx"

    try:
        # Load the dataset
        df = pd.read_csv(csv_url)
        df = df[df["Craftsmanship and production"] == True]

        df["Industries"] = df["Industries"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # Add an editable column for "Preferred Status" using a Selectbox
        df["Contaced (double-click cell to edit)"] = ["Not yet contacted"] * len(df)  

        edited_df = st.data_editor(
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
                "Preferred Status": st.column_config.SelectboxColumn(
                    "Preferred Status",
                    help="Set the preferred status for each company",
                    options=["Not yet contacted", "Contacted"],  # Options for the selectbox
                    required=True
                )
            },
            hide_index=True,
            use_container_width=True
        )

        # Provide a download button for the updated DataFrame
        st.download_button(
            label="Download Updated Data",
            data=edited_df.to_csv(index=False).encode("utf-8"),
            file_name="Updated_Corporate_Data.csv",
            mime="text/csv",
        )

        response = requests.get(excel_url)
        if response.status_code == 200:
            excel_data = response.content  # Get the file content as binary

            # Add a download button for the Excel file
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="Craftsmanship_and_Production.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(f"Failed to fetch the Excel file. Status code: {response.status_code}")

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

# Run the app
render()
