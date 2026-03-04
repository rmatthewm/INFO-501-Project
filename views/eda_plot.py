import streamlit as st

# Get the data handler
dh = st.session_state['DataHandler']

# A box to display the plot in
box = None

# Generate the plot
def visualize():
    # Get the data to visualize
    x = st.session_state['x']
    y = st.session_state['y']

print(type(dh.get_columns()))

st.title('Explore the Data')

# Get the columns in the data
data_cols = dh.get_columns()

col1, col2, col3 = st.columns(3, vertical_alignment='bottom')
col1.selectbox('X Axis', data_cols, format_func=dh.get_col_fancy_name, key='x')
col2.selectbox('Y Axis', data_cols, format_func=dh.get_col_fancy_name, key='y')
col3.button('Visualize', on_click=visualize)

box = st.container()