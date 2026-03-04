# Raul created this as an example of some of the streamlit
# capabilities we might use.

import streamlit as st
import pandas as pd

# Get our data
data = pd.read_csv('data/rental_data.csv')
data_headers = pd.read_csv('data/rental_data_headers.csv')

class Why(Exception):
    pass


# General Notes:
#
# It seems to auto update when you make changes to the file without having 
# to rerun streamlit, which is nice.
#
# Streamlit also supports multiple pages and simple navigation.
#
# No thousands separator for dataframe display?
#
# Custom components can be made using JavaScript.
#
# IMPORTANT! countyname label is wrong in data_headers

"""
FYI: Any variable or value standing on it's own is written to the page,
so since multiline strings using triple " are not technically comments
in Python, but just multiline strings, they will be written to the page.
(like this one)
"""


#===================================text=======================================
# There are methods for 'title', 'header', and 'subheader'
st.title('Test stuff')

# For other text styles, you can use markdown
st.markdown('*Look at this text*')

# Just a horizontal line for looks
st.divider()


#===================================input======================================
st.header('Input Stuff')

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

# Example of columns
st.markdown('*notice the columns*')
col1, col2 = st.columns(2)

# There are also built in elements for basically every common input
# including sliders and calendars
number = col1.number_input('Input a number')
toggled = col1.toggle('Toggle')
# Only takes numerical data
slider_result = col1.slider('Slider', min_value=0, max_value=100)
# Takes anything iterable
slider2_result = col2.select_slider('Slider2', options=range(50))
date = col2.date_input('Date')

st.divider()


#================================more layout stuff=============================
# Expanders could be nice for showing results potentially and clicking to view
# more information.
with st.expander('Expand to see more stuff'):
    st.text('more stuff')

# Popover is like an expander but the opened box floats
with st.popover('Click to see more stuff'):
    st.text('also more stuff')

st.divider()


#====================================data======================================
st.header('Data Stuff')

# Dataframes display table like data including pandas dataframes
display_data = data[['countyname', 'metro', 'pop2023', 'fmr_1', 'fmr_2', 'fmr_3', 'fmr_4']]
display_data['rates_list'] = display_data[['fmr_1', 'fmr_2', 'fmr_3', 'fmr_4']].agg(list, axis=1)

# Columns can be configured like this
st.dataframe(display_data, 
             column_config={
                'countyname': 'County',
                'metro': st.column_config.CheckboxColumn(
                    'Is Metro Area?',
                    default=False,
                    disabled=True,
                ),
                'pop2023': st.column_config.NumberColumn(
                    '2023 Population',
                    format='%d 👤',
                ),
                'fmr_1': st.column_config.NumberColumn(
                     'Rate (1 bed)',
                     format='$%d',
                 ),
                'fmr_2': st.column_config.NumberColumn(
                     'Rate (2 bed)',
                     format='$%d',
                 ),
                'fmr_3': st.column_config.NumberColumn(
                     'Rate (3 bed)',
                     format='$%d',
                 ),
                'fmr_4': st.column_config.NumberColumn(
                     'Rate (4 bed)',
                     format='$%d',
                 ),
                 'rates_list': st.column_config.BarChartColumn(
                     'Rate by Beds',
                     y_min=400,
                     y_max=6000
                 )
             })
