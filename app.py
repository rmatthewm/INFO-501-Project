# app.py -- the main file for the Streamlit app

import streamlit as st
from data_classes.data_handler import DataHandler

# Initialize our data handler
dh = DataHandler('data/rental_data.csv')

# Add the data handler to our session state so that we can access it
# across pages
st.session_state['DataHandler'] = dh

# What should we call the app?
app_name = 'Rental Finder'

# Add the pages
page_nav = st.navigation([
    st.Page('views/main_page.py', title=app_name, default=True),
    st.Page('views/example.py', title='Example', url_path='example')
])

page_nav.run()