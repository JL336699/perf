# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 12:34:11 2024

@author: Joseph.Lapsley
"""

import streamlit as st
import pandas as pd
import zipfile
import os
from io import BytesIO

st.title("Upload ZIP or Excel File")

uploaded_file = st.file_uploader("Choose an Excel or ZIP file", type=["xlsx", "zip"])

if uploaded_file is not None:
    file_name = uploaded_file.name
    
    # Check if it's a ZIP file
    if file_name.endswith(".zip"):
        with zipfile.ZipFile(BytesIO(uploaded_file.read()), 'r') as zip_ref:
            # Extract all files from the zip archive
            zip_ref.extractall("extracted_data")
            st.success(f"Extracted files: {zip_ref.namelist()}")
        
        # Check if there's an xlsx file in the zip and process it
        for file in zip_ref.namelist():
            if file.endswith(".xlsx"):
                extracted_file_path = os.path.join("extracted_data", file)
                df = pd.read_excel(extracted_file_path)
                st.write(df)
            else:
                st.warning(f"No Excel files found in {file_name}")
    
    # Check if it's an Excel file
    elif file_name.endswith(".xlsx"):
        df = pd.read_excel(uploaded_file)
        st.write("Here's a preview of your uploaded Excel file:")
        st.write(df)
    
    else:
        st.error("Unsupported file type. Please upload a .xlsx or .zip file.")
