import streamlit as st

# Get the data handler
dh = st.session_state['DataHandler']


#--------------------------------Event Listeners-------------------------------
def get_results():
    # Get the search criteria
    state = st.session_state['state-input']
    bed_count = st.session_state['bedrooms-input']

    # Get the data results
    data = dh.get_cheapest_counties(state, bed_count)

    # Display the results
    st.dataframe(data)
    


#----------------------------------Page Layout---------------------------------
st.title('Rental Finder')

# Gather input from the user
col1, col2, col3 = st.columns(3, vertical_alignment='bottom')
with col1:
    st.text_input('Desired State', key='state-input')
with col2:
    st.number_input('Desired Bedroom Count', key='bedrooms-input', value=0)
with col3:
    st.button('Find my place!', on_click=get_results)

st.divider()

# Right now, we can just find the cheapest 
st.dataframe(key='data-display')

# List the top results here