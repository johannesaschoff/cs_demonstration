import streamlit as st
import pandas as pd

# Title of the application
st.title("NGO Search App")

# Path to the default CSV files in the repository
default_csv_part1 = 'ngo_data_part1.csv'
default_csv_part2 = 'ngo_data_part2.csv'

# Option to upload CSV files or use the default ones
uploaded_file1 = st.file_uploader("Upload the first part of your NGO CSV file (or use the default)", type="csv", key="part1")
uploaded_file2 = st.file_uploader("Upload the second part of your NGO CSV file (or use the default)", type="csv", key="part2")

# Load the default CSV files if no upload is provided
if uploaded_file1 and uploaded_file2:
    df1 = pd.read_csv(uploaded_file1)
    df2 = pd.read_csv(uploaded_file2)
    st.write("Preview of the uploaded files:")
else:
    df1 = pd.read_csv(default_csv_part1)
    df2 = pd.read_csv(default_csv_part2)
    st.write("Preview of the default files:")

# Merging the two DataFrames
df = pd.concat([df1, df2], ignore_index=True)

# Display the first few rows of the merged DataFrame
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
