# Mimic the output from the RentCast API using a Flask server so we don't need
# to make so many requests while testing.

from flask import Flask

current_state = 'good' 

app = Flask(__name__)

@app.route('/')
def controls():
    return current_state

# Change the state when we access this route 
@app.route('/state/<state>')
def change_state(state):
    global current_state
    # The possible options for state are 'good', 'error', and 'noresult'
    # Anything else will be treated as 'error' 
    current_state = state

    return f'State is now {current_state}.' 



if __name__ == '__main__':
    app.run()
