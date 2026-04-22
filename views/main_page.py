import streamlit as st

st.title('Welcome!')
st.divider()

st.header('Find the best listing near you!')
st.page_link('views/find_listing.py', label='Find Now', icon=':material/home:')

st.header('Want to find the most affordable county for your income?')
st.page_link('views/recommendation.py', label='Affordable County', icon=':material/map_search:')
st.divider()

st.header('Or explore the data through visualization?')
st.page_link('views/eda_plot.py', label='Visualize', icon=':material/bar_chart_4_bars:')