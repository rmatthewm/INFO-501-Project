import streamlit as st
import pandas as pd

# Get the data handler
dh = st.session_state['DataHandler']
api = st.session_state['APIHandler']

# Empty container to display results
results_box = None

# The list of state options for selecting a state
STATE_OPTIONS = ['any'] + dh.get_state_codes()


#--------------------------------Event Listeners-------------------------------
def get_results():
    """Generate the results from the user's input on button click"""
    # Get the search criteria
    city = st.session_state['city-input']
    state = st.session_state['state-input']

    # Get the results from the api, for now just 5. Although we should get more and sort them later
    listings = api.get_listings_by_city(city, state, 5) 

    # Display the results
    for listing in listings:
        # Give more information about this listing when expanded
        with results_box.expander(f'${listing["price"]}: {listing["formattedAddress"]}'):
            st.dataframe({
                'Beds': [listing['bedrooms']],
                'Bathrooms': [listing['bathrooms']],
                'Sq Feet': [listing['squareFootage']],
                'Built': [listing['yearBuilt']],
                'Type': [listing['propertyType']],
                'Lat': [listing['latitude']],
                'Long': [listing['longitude']]
            })



#----------------------------------Page Layout---------------------------------
st.title('Find a Rental Property')

# Gather input from the user
col1, col2, col3 = st.columns(3, vertical_alignment='bottom')
with col1:
    st.text_input('City', key='city-input')
with col2:
    st.selectbox('State', STATE_OPTIONS, key='state-input')
with col3:
    st.button('Find my place!', icon=':material/search:', on_click=get_results)

st.divider()

# Create a place to display the results 
results_box = st.container()