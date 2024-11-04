import streamlit as st
import pandas as pd
rtest
# Set the page to full width
st.set_page_config(layout="wide")

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

# Input box for users to enter multiple keywords separated by commas
search_query = st.text_input("Enter keywords to search within 'charity activities' (separate keywords with commas)")

# Convert the search query to a list of keywords
keywords = [word.strip() for word in search_query.split(",")] if search_query else []

# Filter the DataFrame based on the entered keywords (categories) in 'charity activities'
filtered_df = df
for keyword in keywords:
    if keyword:
        filtered_df = filtered_df[filtered_df['charity_activities'].str.contains(keyword, case=False, na=False)]

# Display the number of search results
num_results = len(filtered_df)
st.write(f"Number of results: {num_results}")

# Display the filtered DataFrame
st.write(f"Filtered results based on 'charity activities' for filters: {', '.join(keywords)}")
st.dataframe(filtered_df)
