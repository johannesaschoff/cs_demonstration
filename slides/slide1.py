import streamlit as st
import pandas as pd

# Create a connection to Google Sheets
conn = st.experimental_connection("gsheets", type="gspread")

# Specify the worksheet name
worksheet_name = "Orders"

# Placeholder DataFrame for demonstration purposes
data = pd.DataFrame({
    "Item": ["Apple", "Banana", "Cherry"],
    "Price": [1.2, 0.8, 2.5],
    "Quantity": [10, 20, 15],
})

# Streamlit UI
st.title("Google Sheets Integration with Streamlit")
st.write("CRUD Operations on Google Sheets")

# Create a new worksheet with data
if st.button("New Worksheet"):
    conn.create(worksheet=worksheet_name, data=data)
    st.success(f"Worksheet '{worksheet_name}' Created 🎉")

# Read data from the worksheet
if st.button("Read Worksheet"):
    fetched_data = conn.read(worksheet=worksheet_name)
    st.write("Fetched Data:")
    st.dataframe(fetched_data)

# Update data in the worksheet
if st.button("Update Worksheet"):
    # Example of modified data
    updated_data = pd.DataFrame({
        "Item": ["Orange", "Grape"],
        "Price": [1.5, 2.8],
        "Quantity": [25, 30],
    })
    conn.update(worksheet=worksheet_name, data=updated_data)
    st.success(f"Worksheet '{worksheet_name}' Updated ✅")

# Clear the worksheet
if st.button("Clear Worksheet"):
    conn.clear(worksheet=worksheet_name)
    st.success(f"Worksheet '{worksheet_name}' Cleared 🧹")
