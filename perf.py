import streamlit as st
import pandas as pd
import zipfile
import os
from io import BytesIO

# Define the path to the directory
directory_path = r'\\aberdeen.aberdeen-asset.com\groupdfs\Philadelphia Group\Fixed Income\Municipals\JL\perf'

def load_data_from_zip(zip_path):
    data_frames = {}
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith(".xlsx"):
                    with zip_ref.open(file) as extracted_xlsx:
                        df = pd.read_excel(extracted_xlsx)
                        data_frames[file] = df
    except zipfile.BadZipFile:
        st.error("The ZIP file is corrupted or invalid.")
    return data_frames

def load_data_from_xlsx(xlsx_path):
    try:
        df = pd.read_excel(xlsx_path)
        return df
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")

def perform_analysis(df):
    # Example of analysis: Find top 10 outliers for positive and negative performance
    df['Performance'] = df['Base Price Percent Change']  # Assuming this is the performance metric
    top_positives = df.nlargest(10, 'Performance')
    top_negatives = df.nsmallest(10, 'Performance')
    return top_positives, top_negatives

st.title("Process Files from Directory")

# List files in the directory
files = os.listdir(directory_path)

# Dropdown menu to select a file
selected_file = st.selectbox("Select a file", files)

if selected_file:
    file_path = os.path.join(directory_path, selected_file)
    
    if selected_file.endswith(".zip"):
        st.write("Processing ZIP file...")
        data_frames = load_data_from_zip(file_path)
        if data_frames:
            for file_name, df in data_frames.items():
                st.write(f"Data from {file_name}:")
                st.write(df)
                
                top_positives, top_negatives = perform_analysis(df)
                st.write("Top 10 Positive Performance:")
                st.write(top_positives)
                st.write("Top 10 Negative Performance:")
                st.write(top_negatives)
        else:
            st.warning("No Excel files found in the ZIP.")
    
    elif selected_file.endswith(".xlsx"):
        st.write("Processing Excel file...")
        df = load_data_from_xlsx(file_path)
        if df is not None:
            st.write("Here's a preview of your Excel file:")
            st.write(df)
            
            top_positives, top_negatives = perform_analysis(df)
            st.write("Top 10 Positive Performance:")
            st.write(top_positives)
            st.write("Top 10 Negative Performance:")
            st.write(top_negatives)
    
    else:
        st.error("Unsupported file type. Please select a .xlsx or .zip file.")
