# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 14:55:52 2024

@author: Joseph.Lapsley
"""

import pandas as pd
import os

# Define the directory containing the files
directory_path = 'G:/Fixed Income/Municipals/JL/perf'

# List all files in the directory
files = os.listdir(directory_path)
print(f"Files in directory: {files}")

# Filter for Excel files
xlsx_files = [f for f in files if f.lower().endswith('.xlsx')]
print(f".xlsx files found: {xlsx_files}")

# Check if there are any .xlsx files
if not xlsx_files:
    raise FileNotFoundError("No .xlsx files found in the directory.")

# Find the latest file based on creation/modification time
latest_file = max(xlsx_files, key=lambda f: os.path.getmtime(os.path.join(directory_path, f)))
latest_file_path = os.path.join(directory_path, latest_file)

print(f"Processing latest file: {latest_file_path}")

# Load the data from the latest Excel file
try:
    data = pd.read_excel(latest_file_path)
except Exception as e:
    print(f"Error loading file: {e}")
    exit()

# Display the first few rows to understand the structure of the data
print("Sample data:")
print(data.head())

# Display the columns to verify data loading
print("\nColumns in the data:", data.columns.tolist())

# Ensure the necessary columns are present
required_columns = [
    'Price Date', 'Fund', 'CUSIP Number', 'Security Description',
    'Base Price Percent Change', 'Base Market Value Change'
]

# Check if the required columns are present
missing_columns = [col for col in required_columns if col not in data.columns]
if missing_columns:
    raise ValueError(f"Missing columns in the data: {', '.join(missing_columns)}")

# Convert columns to numeric if necessary
data['Base Price Percent Change'] = pd.to_numeric(data['Base Price Percent Change'], errors='coerce')
data['Base Market Value Change'] = pd.to_numeric(data['Base Market Value Change'], errors='coerce')

# Drop rows with NaN values in the relevant columns
data.dropna(subset=['Base Price Percent Change', 'Base Market Value Change'], inplace=True)

# Display some statistics for debugging
print("\nData statistics:")
print(data.describe())

# Find the top 10 biggest positive and negative price changes
top_10_positive_changes = data.sort_values(by='Base Price Percent Change', ascending=False).head(10)
top_10_negative_changes = data.sort_values(by='Base Price Percent Change', ascending=True).head(10)

# Find the top 10 biggest positive and negative market value changes
top_10_positive_market_value_changes = data.sort_values(by='Base Market Value Change', ascending=False).head(10)
top_10_negative_market_value_changes = data.sort_values(by='Base Market Value Change', ascending=True).head(10)

# Print the results
print("\nTop 10 Biggest Positive Price Changes:")
print(top_10_positive_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Price Percent Change']].to_string(index=False))

print("\nTop 10 Biggest Negative Price Changes:")
print(top_10_negative_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Price Percent Change']].to_string(index=False))

print("\nTop 10 Biggest Positive Market Value Changes:")
print(top_10_positive_market_value_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Market Value Change']].to_string(index=False))

print("\nTop 10 Biggest Negative Market Value Changes:")
print(top_10_negative_market_value_changes[['Fund', 'CUSIP Number', 'Security Description', 'Base Market Value Change']].to_string(index=False))
