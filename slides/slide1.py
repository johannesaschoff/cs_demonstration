import streamlit as st
import pandas as pd
import requests
import ast
from st_aggrid import AgGrid, GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

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

    # Load and edit the dataset
    try:
        df = pd.read_csv(csv_url)
        df = df[df["Craftsmanship and production"] == True]

        # Allow users to edit the dataframe
        st.subheader("Edit and Select Rows in the Corporate Dataset")
        st.info("💡 Tip: Click on cells to edit. Use checkboxes to select rows.")

        # Configure ag-grid options
        gd = GridOptionsBuilder.from_dataframe(df)
        gd.configure_pagination(enabled=True)  # Enable pagination
        gd.configure_default_column(editable=True, groupable=True)  # Enable cell editing
        gd.configure_selection(selection_mode="multiple", use_checkbox=True)  # Enable row selection
        grid_options = gd.build()

        # Render the editable table
        grid_table = AgGrid(
            df,
            gridOptions=grid_options,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            theme="material",
        )
        selected_rows = grid_table["selected_rows"]
        edited_df = pd.DataFrame(selected_rows)

        # Show selected rows if any
        st.subheader("Selected and Edited Rows")
        if not edited_df.empty:
            st.dataframe(edited_df)
            
            # Add a download button for the selected rows
            csv = edited_df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Edited Data as CSV",
                data=csv,
                file_name="edited_corporate_dataset.csv",
                mime="text/csv",
            )
        else:
            st.info("No rows selected. Edit cells or select rows to proceed.")

    except Exception as e:
        st.error(f"Failed to load or edit the dataset: {e}")

    # Add a download button for the Excel file
    try:
        response = requests.get(excel_url)
        if response.status_code == 200:
            excel_data = response.content  # Get the file content as binary
    
            st.download_button(
                label="Download data as Excel",
                data=excel_data,
                file_name="Craftsmanship_and_Production.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        else:
            st.error(f"Failed to fetch the Excel file. Status code: {response.status_code}")
    except Exception as e:
        st.error(f"Failed to fetch the Excel file: {e}")

# Run the app
render()
