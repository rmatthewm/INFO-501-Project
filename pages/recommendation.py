import streamlit as st
from data_handler import DataHandler

# Initialize data
data = DataHandler("data/your_data.csv", "data/headers.csv")

st.title("🏠 Housing Recommendation System")

st.write("Find the best counties for you based on your income and housing needs.")

# USER INPUTS
income = st.number_input("Enter your annual income ($)", min_value=10000, step=1000)
bedrooms = st.selectbox("Select number of bedrooms", [0, 1, 2, 3, 4])

states = ['any'] + data.get_state_codes()
state = st.selectbox("Select a state (optional)", states)

# BUTTON
if st.button("Get Recommendations"):

    results = data.get_recommendations(income, bedrooms, state)

    st.subheader("Top 5 Recommended Locations")

    st.dataframe(
        results[[
            "County_Name",
            "HUD_Area_Name",
            f"fmr_{bedrooms}",
            "affordability_score",
            "affordability_label"
        ]]
    )

    st.write("💡 We use the 30% income rule to estimate affordability.")