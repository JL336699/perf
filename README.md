# Municipal Bond Analysis App

This is a Streamlit app for analyzing municipal bond data. It processes a ZIP file, extracts the CSV, and identifies the top 10 positive and negative outliers based on the "Base Price Percent Change" column.

## Setup

1. **Create and activate the `perf` conda environment**:
   ```bash
   conda create --name perf python=3.9
   conda activate perf
