import streamlit as st

st.title('Welcome')
st.header('Want to find the cheapest county in your state?')
st.page_link('views/cheapest_county.py', label='Get Started', icon=':material/map_search:')