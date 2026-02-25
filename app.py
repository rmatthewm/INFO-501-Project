# app.py -- the main file for the Streamlit app

import streamlit as st
from __init__ import *

# What should we call the app?
app_name = 'Rental Finder'

# Add the pages
page_nav = st.navigation([
    st.Page('views/main_page.py', title=app_name, default=True)
])

page_nav.run()