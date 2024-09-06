import streamlit as st
import pandas as pd
import os
import zipfile
from datetime import datetime

# Define the path to the network directory
directory_path = r'\\aberdeen.aberdeen-asset.com\groupdfs\Philadelphia Group\Fixed Income\Municipals\JL\perf'

def get_latest_file(directory):
    files = os.listdir(directory)
    # Filter for .xlsx and .zip files
    files = [f for f in files if f.endswith(('.xlsx', '.zip'))]
    
    if not files:
        st.error("No .xlsx or .zip files found in the directory.")
        return None
    
    # Get the full file paths and sort them by modification time
    files = [os.path.join(directory, f) for f in files]
    latest_file = max(files, key=os.path.getmtime)
    
    return latest_file

def load_data_from_zip(zip_file):
    data_frames = {}
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            for file in zip_ref.namelist():
                if file.endswith(".xlsx"):
                    with zip_ref.open(file) as extracted_xlsx:
                        df = pd.read_excel(extracted_xlsx)
                        data_frames[file] = df
    except zipfile.BadZipFile:
        st.error("The ZIP file is corrupted or invalid.")
    return data_frames

def load_data_from_xlsx(xlsx_file):
    try:
        df = pd.read_excel(xlsx_file)
        return df
    except Exception as e:
        st.error(f"Error reading the Excel file: {e}")

def perform_analysis(df):
    # Example of analysis: Find top 10 outliers for positive and negative performance
    df['Performance'] = df['Base Price Percent Change']  # Assuming this is the performance metric
    top_positives = df.nlargest(10, 'Performance')
    top_negatives = df.nsmallest(10, 'Performance')
    return top_positives, top_negatives

st.title("Automatically Process Latest File")

# Get the latest file from the directory
latest_file = get_latest_file(directory_path)

if latest_file:
    st.write(f"Processing file: {latest_file}")
    
    if latest_file.endswith(".zip"):
        data_frames = load_data_from_zip(latest_file)
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
    
    elif latest_file.endswith(".xlsx"):
        df = load_data_from_xlsx(latest_file)
        if df is not None:
            st.write("Here's a preview of your Excel file:")
            st.write(df)
            
            top_positives, top_negatives = perform_analysis(df)
            st.write("Top 10 Positive Performance:")
            st.write(top_positives)
            st.write("Top 10 Negative Performance:")
            st.write(top_negatives)
    
    else:
        st.error("Unsupported file type.")
else:
    st.error("No files found in the directory.")
