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

# State to hold active filters
if 'filters' not in st.session_state:
    st.session_state['filters'] = []

# Search box for filtering by keywords in the "charity activities" column
search_query = st.text_input("Enter keywords to search within 'charity activities'")

# Add the filter to the session state if it's not already there
if search_query:
    if search_query not in st.session_state['filters']:
        st.session_state['filters'].append(search_query)

# Display active filters as clickable categories
st.write("Active Filters:")
for filter_word in st.session_state['filters']:
    if st.button(f"Remove {filter_word}", key=filter_word):
        st.session_state['filters'].remove(filter_word)

# Filter the DataFrame based on active filters
filtered_df = df
for filter_word in st.session_state['filters']:
    filtered_df = filtered_df[filtered_df['charity_activities'].str.contains(filter_word, case=False, na=False)]

# Display the filtered DataFrame
st.write(f"Filtered results based on 'charity activities' for filters: {', '.join(st.session_state['filters'])}")
st.dataframe(filtered_df)
