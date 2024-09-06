# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 12:34:11 2024

@author: Joseph.Lapsley
"""

import streamlit as st
import pandas as pd
import zipfile
import os

# Helper function to process .xlsx files
def process_xlsx(file):
    df = pd.read_excel(file)
    return df

# Helper function to process .zip files
def process_zip(file):
    with zipfile.ZipFile(file, 'r') as zip_ref:
        # Extract all files to a temporary directory
        zip_ref.extractall("temp_data")
        for extracted_file in zip_ref.namelist():
            if extracted_file.endswith('.xlsx'):
                # Process the extracted Excel file
                return pd.read_excel(os.path.join("temp_data", extracted_file))
    return None

# Streamlit UI
st.title("Upload a Zip or Excel File")

uploaded_file = st.file_uploader("Upload a .zip or .xlsx file", type=["zip", "xlsx"])

if uploaded_file:
    file_details = {"filename": uploaded_file.name, "filetype": uploaded_file.type}
    
    if uploaded_file.name.endswith('.xlsx'):
        st.write("Processing Excel file...")
        try:
            df = process_xlsx(uploaded_file)
            st.write("File processed successfully!")
            st.dataframe(df.head())  # Display the first few rows of the DataFrame
        except Exception as e:
            st.error(f"Error processing Excel file: {e}")
    
    elif uploaded_file.name.endswith('.zip'):
        st.write("Processing Zip file...")
        try:
            df = process_zip(uploaded_file)
            if df is not None:
                st.write("File processed successfully!")
                st.dataframe(df.head())  # Display the first few rows of the DataFrame
            else:
                st.error("No valid Excel file found in the ZIP archive.")
        except Exception as e:
            st.error(f"Error processing Zip file: {e}")
    
    else:
        st.error("Unsupported file type. Please upload a .zip or .xlsx file.")
