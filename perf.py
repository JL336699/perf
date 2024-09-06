# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 12:34:11 2024

@author: Joseph.Lapsley
"""

import streamlit as st
import pandas as pd
import zipfile
import os

# Title and description for the Streamlit app
st.title("Municipal Bond Performance Analysis")
st.write("Upload a ZIP file containing your data to analyze the top 10 outliers for both positive and negative performance.")

# Function to process the uploaded ZIP file
def process_uploaded_zip(uploaded_file):
    # Unzipping the file
    with zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        zip_ref.extractall("extracted_data")

    # Assuming there's a specific CSV or Excel file in the ZIP after extraction
    for file in os.listdir("extracted_data"):
        if file.endswith('.xlsx'):
            # Load the Excel file
            file_path = os.path.join("extracted_data", file)
            data = pd.read_excel(file_path)

            # Process the Excel file (e.g., sorting, filtering top outliers)
            # Replace these columns with actual calculations as needed
            top_10_positive = data.nlargest(10, 'NAV Per Share Impact')
            top_10_negative = data.nsmallest(10, 'NAV Per Share Impact')

            # Display the results in Streamlit
            st.subheader("Top 10 Positive Outliers")
            st.write(top_10_positive)

            st.subheader("Top 10 Negative Outliers")
            st.write(top_10_negative)

# Upload ZIP file using Streamlit's native file uploader
uploaded_file = st.file_uploader("Choose a ZIP file", type="zip")

if uploaded_file:
    st.write("Processing the uploaded file...")
    process_uploaded_zip(uploaded_file)
else:
    st.write("Please upload a ZIP file to proceed.")

