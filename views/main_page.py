import streamlit as st

#--------------------------------Event Listeners-------------------------------
def get_results():
    # Get the search criteria
    state = st.session_state['state-input']
    bed_count = st.session_state['bedrooms-input']

#----------------------------------Page Layout---------------------------------
st.title('Rental Finder')

# Gather input from the user
st.text_input('Desired State', key='state-input')
st.number_input('Desired Bedroom Count', key='bedrooms-input')
st.button('Find my place!')
st.divider()

# Right now, we can just find the cheapest 

# List the top results here