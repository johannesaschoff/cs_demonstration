import streamlit as st
import pandas as pd

# Title of the application
st.title("NGO Search App")

# Path to the default CSV file in the repository
default_csv_path = 'ngo_data.csv'

# Option to upload a CSV file or use the default one
uploaded_file = st.file_uploader("Upload your NGO CSV file (or use the default one)", type="csv")

# Load the default CSV file if no upload is provided
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.write("Preview of the uploaded file:")
else:
    df = pd.read_csv(default_csv_path)
    st.write("Preview of the default file:")

# Display the first few rows of the DataFrame
st.dataframe(df.head())

# Search box for filtering organizations by keywords
search_query = st.text_input("Enter keywords to search for NGOs")

# Multi-selection for filtering based on specific columns (you can adjust the default columns)
options = st.multiselect(
    "Select columns to filter by:",
    df.columns.tolist(),  # Assuming all columns are searchable
    default=None
)

# Filter the DataFrame based on the search input
if search_query:
    filtered_df = df[df.apply(lambda row: search_query.lower() in row.to_string().lower(), axis=1)]
else:
    filtered_df = df

# Further filter based on selected columns (if any)
if options:
    filtered_df = filtered_df[filtered_df[options].notnull().all(axis=1)]

# Display the filtered DataFrame
st.write("Filtered results:")
st.dataframe(filtered_df)
