import streamlit as st

# Initialize data
data = st.session_state['DataHandler']

st.title("🏠 Income-Based Recommendation System")
st.write("Find the best counties for you based on your income and housing needs.")

# User inputs
income = st.number_input("Enter your annual income ($)", min_value=10000, step=1000)
bedrooms = st.selectbox("Select number of bedrooms", [0, 1, 2, 3, 4])

states = ['any'] + sorted(data.get_state_codes())
state = st.selectbox("Select a state (optional)", states)

# Button
if st.button("Get Recommendations"):
    results = data.get_recommendations(income, bedrooms, state, n_results=5)

    monthly_income = income / 12
    affordable_rent = monthly_income * 0.30

    st.subheader("Top 5 Recommended Locations")
    st.write(f"Estimated affordable monthly rent based on your income: **${affordable_rent:,.2f}**")

    st.dataframe(
        results[[
            "countyname",
            "hud_area_name",
            f"fmr_{bedrooms}",
            "affordability_score",
            "affordability_label"
        ]].rename(columns={
            "countyname": "County",
            "hud_area_name": "HUD Area",
            f"fmr_{bedrooms}": "Monthly Rent",
            "affordability_score": "Score / 100",
            "affordability_label": "Affordability"
        }),
        use_container_width=True
    )

    st.write("💡 A score of 100 means the rent is within the recommended affordable limit based on the 30% income rule.")