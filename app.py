import streamlit as st
import pandas as pd
import os

st.title("Nayanam Dashboard")

# Check file
file_path = "orders.csv"

st.write("Checking file...")

if not os.path.exists(file_path):
    st.error("orders.csv NOT found")
    st.stop()

st.success("File found")

# Load data safely
try:
    df = pd.read_csv(file_path)
    st.success("Data loaded successfully")
except Exception as e:
    st.error(f"Error loading CSV: {e}")
    st.stop()

# Show basic info
st.write("Columns:", df.columns.tolist())
st.write("Total rows:", len(df))

# Show first few rows
st.dataframe(df.head())