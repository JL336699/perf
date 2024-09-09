import streamlit as st
import pandas as pd
import os

# Define the path to the directory
directory_path = 'G:/Fixed Income/Municipals/JL/perf'

def load_latest_file(directory):
    # List all files in the directory
    files = os.listdir(directory)
    xlsx_files = [f for f in files if f.endswith('.xlsx')]
    
    if not xlsx_files:
        st.error("No .xlsx files found in the directory.")
        return None
    
    # Sort files by creation time or name
    latest_file = sorted(xlsx_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)[0]
    return os.path.join(directory, latest_file)

def analyze_data(file_path):
    try:
        # Load the data from the Excel file
        data = pd.read_excel(file_path)
        
        # Ensure the necessary columns are present
        required_columns = [
            'Price Date', 'Fund', 'CUSIP Number', 'Security Description',
            'Base Price Percent Change', 'Base Market Value Change'
        ]
        missing_columns = [col for col in required_columns if col not in data.columns]
        if missing_columns:
            st.error(f"Missing columns in the data: {', '.join(missing_columns)}")
            return
        
        # Convert columns to numeric if necessary
        data['Base Price Percent Change'] = pd.to_numeric(data['Base Price Percent Change'], errors='coerce')
        data['Base Market Value Change'] = pd.to_numeric(data['Base Market Value Change'], errors='coerce')

        # Drop rows with NaN values in the relevant columns
        data.dropna(subset=['Base Price Percent Change', 'Base Market Value Change'], inplace=True)

        # Find the top 10 biggest positive and negative price changes
        top_10_positive_changes = data.sort_values(by='Base Price Percent Change', ascending=False).head(10)
        top_10_negative_changes = data.sort_values(by='Base Price Percent Change', ascending=True).head(10)

        # Find the top 10 biggest positive and negative market value changes
        top_10_positive_market_value_changes = data.sort_values(by='Base Market Value Change', ascending=False).head(10)
        top_10_negative_market_value_changes = data.sort_values(by='Base Market Value Change', ascending=True).head(10)

        # Display results in Streamlit
        st.write("### Top 10 Biggest Positive Price Changes")
        st.write(top_10_positive_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Price Percent Change']])

        st.write("### Top 10 Biggest Negative Price Changes")
        st.write(top_10_negative_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Price Percent Change']])

        st.write("### Top 10 Biggest Positive Market Value Changes")
        st.write(top_10_positive_market_value_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Market Value Change']])

        st.write("### Top 10 Biggest Negative Market Value Changes")
        st.write(top_10_negative_market_value_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Market Value Change']])

    except Exception as e:
        st.error(f"Error loading file: {e}")

def main():
    st.title("Muni Performance Analysis")

    file_path = load_latest_file(directory_path)
    if file_path:
        st.write(f"Processing latest file: {file_path}")
        analyze_data(file_path)

if __name__ == "__main__":
    main()
