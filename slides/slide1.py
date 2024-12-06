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

    # Section: Corporate Dataset
    st.markdown("**Matching Corporates**")
    csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates_with_logos.csv"
    excel_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/craftmanship_production.xlsx"

    try:
        # Load the dataset
        df = pd.read_csv(csv_url)
        df = df[df["Craftsmanship and production"] == True]

        df["Industries"] = df["Industries"].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)

        # Add an editable column for "Preferred Status" with default values
        df["Preferred Status"] = ["Undecided"] * len(df)

        # Editable DataFrame
        edited_df = st.experimental_data_editor(df)

        # Extract dictionary with selected values
        selected_values = {
            row["Company Name"]: row["Preferred Status"] for _, row in edited_df.iterrows()
        }

        st.markdown("### Selected Preferences")
        st.json(selected_values)  # Display the dictionary of selections

        # Download button for updated DataFrame
        st.download_button(
            label="Download Updated Data",
            data=edited_df.to_csv(index=False).encode("utf-8"),
            file_name="Updated_Corporate_Data.csv",
            mime="text/csv",
        )

    except Exception as e:
        st.error(f"Failed to load the dataset: {e}")

# Run the app
render()
