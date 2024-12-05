import streamlit as st
import pandas as pd
import requests
import ast

st.set_page_config(layout="wide")

# Initialize or load the contact tracking dictionary
if "contacted_tracker" not in st.session_state:
    st.session_state["contacted_tracker"] = {}  # This will store row keys and their "Contacted" status

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

        # Generate a unique row key for tracking, e.g., based on company name or ID
        df["row_key"] = df.apply(lambda row: row["Company Name"], axis=1)  # Adjust this as per your dataset

        # Update the Category column based on the tracker dictionary
        df["Category"] = df["row_key"].apply(
            lambda key: st.session_state["contacted_tracker"].get(key, "Not Contacted")
        )

        # Use st.data_editor for an interactive dataframe with a select box column
        edited_df = st.data_editor(
            df,
            column_config={
                "Category": st.column_config.SelectboxColumn(
                    "Category",
                    help="Select a category for each company",
                    options=["Not Contacted", "Contacted"],
                    required=True,
                ),
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
            hide_index=True,
            use_container_width=True
        )

        # Update the tracker dictionary with the new selections
        for _, row in edited_df.iterrows():
            st.session_state["contacted_tracker"][row["row_key"]] = row["Category"]

        # Option to download the updated dataframe as a CSV
        if st.button("Save Updated DataFrame"):
            csv_data = edited_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Updated Data as CSV",
                data=csv_data,
                file_name="Updated_Craftsmanship_and_Production.csv",
                mime="text/csv",
            )

        # Add a download button for the Excel file
        response = requests.get(excel_url)
        if response.status_code == 200:
            excel_data = response.content
            st.download_button(
                label="Download Original Excel File",
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
