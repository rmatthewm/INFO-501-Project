# app.py -- the main file for the Streamlit app

import streamlit as st
import os
from dotenv import load_dotenv
from data_classes.data_handler import DataHandler
from data_classes.api_handler import APIHandler
from data_classes.review_handler import ReviewHandler
from data_classes.recommendation_model import RecommendationModel as RecModel

# Load in our development environment variables
load_dotenv()

# Initialize our data handler
dh = DataHandler('data/rental_data.csv', 'data/rental_data_columns.csv')

# Initialize our API handler
API_URL = os.getenv('LISTINGS_API_URL')
API_KEY = os.getenv('LISTINGS_API_KEY')
api = APIHandler(API_URL, API_KEY)

# Initialize our Yelp review handler
rh = ReviewHandler('data/yelp_businesses.csv')

# Intitialize our recommendation model
rec_model = RecModel(rh, dh)

# Add the handlers to our session state so that we can access them 
# across pages
st.session_state['DataHandler'] = dh
st.session_state['APIHandler'] = api
st.session_state['RecModel'] = rec_model

# The name of the app 
app_name = 'Rental Finder'

# Add the pages
page_nav = st.navigation([
    st.Page('views/main_page.py', title=app_name, default=True),
    st.Page('views/find_listing.py', title='Find Listing'),
    st.Page('views/cheapest_county.py', title='Cheapest County'),
    st.Page('views/eda_plot.py', title='EDA Visualizer'),
    st.Page('views/affordability_app.py', title='Affordability App'),
    st.Page('views/recommendation.py', title='Income-Based Recommendation System')
])

page_nav.run()
