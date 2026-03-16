# app.py -- the main file for the Streamlit app

import streamlit as st
import os
from dotenv import load_dotenv
from data_classes.data_handler import DataHandler
from data_classes.api_handler import APIHandler

# Load in our development environment variables
load_dotenv

# Initialize our data handler
dh = DataHandler('data/rental_data.csv', 'data/rental_data_columns.csv')

# Initialize our API handler
API_URL = os.getenv('RENTCAST_API_URL')
API_KEY = os.getenv('RENTCASE_API_KEY')
api = APIHandler(API_URL, API_KEY)

# Add the handlers to our session state so that we can access them 
# across pages
st.session_state['DataHandler'] = dh
st.session_state['APIHandler'] = api

# The name of the app 
app_name = 'Rental Finder'

# Add the pages
page_nav = st.navigation([
    st.Page('views/main_page.py', title=app_name, default=True),
    st.Page('views/cheapest_county.py', title='Cheapest County'),
    st.Page('views/eda_plot.py', title='EDA Visualizer'),
    st.Page('views/example.py', title='Example', url_path='example')
])

page_nav.run()
