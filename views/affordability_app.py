import streamlit as st
import pandas as pd

# Assume your DataHandler loads df
from data_handler import DataHandler
from affordability import calculate_affordability

st.title("🏠 Housing Affordability Calculator")

# Load data
data = DataHandler()
df = data.get_data()

# User Inputs
income = st.number_input("Enter your annual income ($)", min_value=10000, step=1000)
bedrooms = st.selectbox("Select number of bedrooms", [0, 1, 2, 3, 4])

if st.button("Find Affordable Locations"):
    
    results = calculate_affordability(df, income, bedrooms)
    
    st.subheader("Top Affordable Locations")
    
    st.dataframe(
        results[["County_Name", "HUD_Area_Name", f"fmr_{bedrooms}", "affordability_score", "affordability_label"]].head(10)
    )