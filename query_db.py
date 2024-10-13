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

# State to hold active filters (used in multiselect)
if 'filters' not in st.session_state:
    st.session_state['filters'] = []

# User can enter multiple search keywords as custom categories using multiselect
filters = st.multiselect(
    "Enter keywords to search within 'charity activities'",
    options=[],  # We don't provide preset options, it's fully user-defined
    default=st.session_state['filters'],
    help="Add search terms as categories to filter results in 'charity activities'."
)

# Save the selected filters to session state for persistence
st.session_state['filters'] = filters

# Filter the DataFrame based on the entered keywords (categories) in 'charity activities'
filtered_df = df
for filter_word in filters:
    filtered_df = filtered_df[filtered_df['charity_activities'].str.contains(filter_word, case=False, na=False)]

# Display the filtered DataFrame
st.write(f"Filtered results based on 'charity activities' for filters: {', '.join(filters)}")
st.dataframe(filtered_df)
