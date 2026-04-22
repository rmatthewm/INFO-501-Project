import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

# Get the data handlers
dh = st.session_state['DataHandler']
api = st.session_state['APIHandler']
rec_model = st.session_state['RecModel']

school_coords = (0.0, 0.0)

# Empty container to display results
results_box = None

# The list of state options for selecting a state
STATE_OPTIONS = ['any'] + dh.get_state_codes()


#--------------------------------Event Listeners-------------------------------
def get_results():
    """Generate the results from the user's input on button click"""
    # If the user has not yet selected a location, return
    if school_coords == (0.0, 0.0):
        results_box.write('Choose a location first.')
        return

    # Get the desired number of bedrooms
    beds = st.session_state['bed_input']

    # Get the results from the api
    listings = api.get_listings_by_coords(school_coords[0], school_coords[1], 50, beds=beds, limit=50) 

    # Display a message if we get no results
    if len(listings) == 0:
        results_box.write('No listings found.')

    else:
        # Get the most recommended results, using IUPUI as central location for now
        recommended_listings = rec_model.recommend_listings(listings, school_coords[0], school_coords[1])
        print(school_coords)

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

# Get the work or school location from the user that 
# we will try to find listings near
col1, col2, col3 = st.columns(3, vertical_alignment='bottom')
with col1:
    location_text = st.empty()
    location_text.text('Click on your school or workplace to get your nearby listing recommendations.')
with col2:
    st.selectbox('Bedroom count', [0,1,2,3,4], key='bed_input')
with col3:
    st.button('Find my place!', icon=':material/search:', on_click=get_results)

m = folium.Map(location=[39.774235, -86.175278], zoom_start=10)
output = st_folium(m, width=700, height=500)
if output and output.get('last_clicked'):
    school_coords = (float(output['last_clicked']['lat']), float(output['last_clicked']['lng']))
    location_text.write(f'Searching near: {school_coords[0]:.4f}, {school_coords[1]:.4f}')

st.divider()
# Create a place to display the results 
results_box = st.container()