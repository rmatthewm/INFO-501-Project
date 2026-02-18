# Raul created this as an example of some of the streamlit
# capabilities we might use.

import streamlit as st

class Why(Exception):
    pass

"""
General Notes:

It seems to auto update when you make changes to the file without having 
to rerun streamlit, which is nice.

"""

#===================================text=======================================
# There are methods for 'title', 'header', and 'subheader'
st.title('Test stuff')

# For other text styles, you can use markdown
st.markdown('*Look at this text*')

# Just a horizontal line for looks
st.divider()

#===================================input======================================
# Button, with action
def on_go_clicked():
    st.success('Went!')
    st.toast('Button clicked', icon='🔥')
st.button('Go', on_click=on_go_clicked)

# There are several result status boxes like 'success' above or this.
# A new status box will replace any existing ones
def on_dont_clicked():
    try:
        raise Why("Why would you do that?")
    except Exception as e:
        st.exception(e)
st.button("DON'T CLICK THIS", on_click=on_dont_clicked)

st.divider()

# There are also built in elements for basically every common input
# including sliders and calendars
number = st.number_input('Input a number')
toggled = st.toggle('Toggle')
# Only takes numerical data
slider_result = st.slider('Slider', min_value=0, max_value=100)
# Takes anything iterable
slider2_result = st.select_slider('Slider2', options=range(50))
date = st.date_input('Date')

st.divider()