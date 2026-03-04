import streamlit as st

st.title('Welcome!')
st.divider()

st.header('Want to find the cheapest county in your state?')
st.page_link('views/cheapest_county.py', label='Get Started', icon=':material/map_search:')
st.divider()

st.header('Or explore the data through visualization?')
st.page_link('views/eda_plot.py', label='Visualize', icon=':material/bar_chart_4_bars:')