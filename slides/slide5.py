import streamlit as st
import pandas as pd

# Load the preprocessed CSV with logo links
csv_url = "https://raw.githubusercontent.com/johannesaschoff/cs_demonstration/main/dataframe_corporates_with_logos.csv"
df = pd.read_csv(csv_url)

# Add an HTML-rendered table for logos
def render_logo_dataframe(df):
    # Create an HTML table
    html_table = """
    <table style="width: 100%; border-collapse: collapse;">
        <tr>
            <th style="border: 1px solid black; padding: 8px;">Logo</th>
            <th style="border: 1px solid black; padding: 8px;">Company Name</th>
            <th style="border: 1px solid black; padding: 8px;">Industry</th>
            <th style="border: 1px solid black; padding: 8px;">EBIT</th>
        </tr>
    """
    for _, row in df.iterrows():
        logo_url = row["Logo"]
        company_name = row["Company Name"]
        industry = row["Industries"]
        ebit = row["EBIT"]

        html_table += f"""
        <tr>
            <td style="border: 1px solid black; padding: 8px;">
                <img src="{logo_url}" style="height: 50px;">
            </td>
            <td style="border: 1px solid black; padding: 8px;">{company_name}</td>
            <td style="border: 1px solid black; padding: 8px;">{industry}</td>
            <td style="border: 1px solid black; padding: 8px;">{ebit}</td>
        </tr>
        """
    html_table += "</table>"
    return html_table

# Streamlit app
def render():
    st.title("Corporate Dataset with Logos in Table")
    
    # Render the dataframe with logos as an HTML table
    html_table = render_logo_dataframe(df)
    st.markdown(html_table, unsafe_allow_html=True)

    # Add a download button for the original dataset
    csv_data = df.to_csv().encode("utf-8")
    st.download_button(
        label="Download data as CSV",
        data=csv_data,
        file_name="corporate_dataset_with_logos.csv",
        mime="text/csv",
    )

# Run the app
render()
