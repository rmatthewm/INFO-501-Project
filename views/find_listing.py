import streamlit as st
import pandas as pd

# Get the data handlers
dh = st.session_state['DataHandler']
api = st.session_state['APIHandler']
rec_model = st.session_state['RecModel']

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

    # Get the results from the api
    listings = api.get_listings_by_city(city, state, 50) 

    # Display a message if we get no results
    if len(listings) == 0:
        results_box.write('No listings found.')

    else:
        # Get the most recommended results, using IUPUI as central location for now
        recommended_listings = rec_model.recommend_listings(listings, 39.774235, -86.175278)

        # Display the results
        for i in range(len(recommended_listings)):
            # Give more information about this listing when expanded
            with results_box.expander(f'${recommended_listings.iloc[i]["price"]}: {recommended_listings.iloc[i]["formattedAddress"]}'):
                st.dataframe({
                    'Beds': [recommended_listings.iloc[i]['bedrooms']],
                    'Bathrooms': [recommended_listings.iloc[i]['bathrooms']],
                    'Sq Feet': [recommended_listings.iloc[i]['squareFootage']],
                    'Built': [recommended_listings.iloc[i]['yearBuilt']],
                    'Type': [recommended_listings.iloc[i]['propertyType']],
                    'Distance': [recommended_listings.iloc[i]['distance']],
                    'Score': [recommended_listings.iloc[i]['score']]
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