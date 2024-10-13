import streamlit as st
import pandas as pd

# Title of the application
st.title("NGO Search App")

# Path to the default CSV files in the repository
default_csv_part1 = 'charity_filtered_above50.csv'
default_csv_part2 = 'charity_filtered_under50.csv'

# Load the default CSV files automatically
df1 = pd.read_csv(default_csv_part1)
df2 = pd.read_csv(default_csv_part2)

# Merging the two DataFrames
df = pd.concat([df1, df2], ignore_index=True)

# Display the first few rows of the merged DataFrame
st.write("Merged NGO Dataset Preview:")
st.dataframe(df.head())

# Search box for filtering by keywords in the "charity activities" column
search_query = st.text_input("Enter keywords to search within 'charity activities'")

# Always filter based on the "charity activities" column
if search_query:
    filtered_df = df[df['charity_activities'].str.contains(search_query, case=False, na=False)]
else:
    filtered_df = df

# Multi-selection for filtering based on additional specific columns
options = st.multiselect(
    "Select additional columns to filter by:",
    df.columns.tolist(),  # Assuming all columns are searchable
    default=None
)

# Further filter based on selected columns (if any)
if options:
    filtered_df = filtered_df[filtered_df[options].notnull().all(axis=1)]

# Display the filtered DataFrame
st.write(f"Filtered results based on 'charity activities' for '{search_query}':")
st.dataframe(filtered_df)
