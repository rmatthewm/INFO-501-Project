import streamlit as st
import pandas as pd

# Get the data handler
dh = st.session_state['DataHandler']

# Empty container to display results
box = None

STATE_OPTIONS = ['any'] + dh.get_state_codes()

#--------------------------------Event Listeners-------------------------------
def get_results():
    # Get the search criteria
    state = st.session_state['state-input']
    bed_count = st.session_state['bedrooms-input']

    # Get the data results
    data = dh.get_cheapest_counties(state, bed_count)

    # Display the results
    for index, row in data.iterrows():
        # Give more information about this county when expanded
        price = row[f'fmr_{bed_count}']
        with box.expander(f'{row["countyname"]}, {row["stusps"]}     {price}'):
            st.dataframe({
                'County': [row['countyname']],
                'State*': [row['stusps']],
                '0 Bed Rate': [row['fmr_0']],
                '1 Bed Rate': [row['fmr_1']],
                '2 Bed Rate': [row['fmr_2']],
                '3 Bed Rate': [row['fmr_3']],
                '4 Bed Rate': [row['fmr_4']],
                'Population': [row['pop2023']]
            })

            # Compare to national and state averages
            nat_avg = dh.get_average_rate(bed_count=bed_count)
            state_avg = dh.get_average_rate(row['stusps'], bed_count)

            # Display the comparisons with delta colors inverted because
            # lower is better
            col1, col2 = st.columns(2)
            col1.metric('Compared to National Average:', f'${int(price-nat_avg)}', 
                    f'{int((price-nat_avg)*100/nat_avg)}%', delta_color='inverse')
            col2.metric('Compared to State Average:', f'${int(price-state_avg)}', 
                    f'{int((price-state_avg)*100/state_avg)}%', delta_color='inverse')

            st.markdown('**state or territory*')


#----------------------------------Page Layout---------------------------------
st.title('Rental Finder')

# Gather input from the user
col1, col2, col3 = st.columns(3, vertical_alignment='bottom')
with col1:
    st.selectbox('Desired State', STATE_OPTIONS, key='state-input')
with col2:
    st.selectbox('Desired Bedroom Count', (0,1,2,3,4), key='bedrooms-input')
with col3:
    st.button('Find my place!', on_click=get_results)

st.divider()

# Right now, we can just find the cheapest 
box = st.container()