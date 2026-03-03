import streamlit as st

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
        price = row[f'fmr_{bed_count}']
        with box.expander(f'{row["countyname"]}, {row["stusps"]}     {price}'):
            st.dataframe(row)
    


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