# Mimic the output from the RentCast API using a Flask server so we don't need
# to make so many requests while testing.

from flask import Flask, request as req
from random import randint
from fake_listing_generator import gen_fake_listing
import json

current_state = 'good' 
valid_api_key = 'lets-a-gooo--Mario'

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

@app.route('/v1/listings/rental/long-term')
def api():
    # First, check for authentication
    header1 = req.headers.get('Accept')
    header2 = req.headers.get('X-Api-Key')

    # If they do not have the proper headers, deny them access
    if header1 is None or header1 != 'application/json':
        return 'Access denied', 405

    if header2 is None or header2 != valid_api_key:
        return 'Access denied', 405

    # Next, we need to get the query options
    city = req.args.get('city')
    state = req.args.get('state')
    latitude = req.args.get('latitude')
    longitude = req.args.get('longitude')
    radius = req.args.get('radius')
    limit = req.args.get('limit', '200')
    property_type = req.args.get('propertyType')
    bedrooms = req.args.get('bedrooms')

    # Check that either city, state or lat, long, radius has been given
    if ((city is None or state is None) and 
        (latitude is None or longitude is None or radius is None)):
        return 'Must provide a location to search.', 400

    # Per the API docs, the radius must be 100 or less
    if radius is not None:
        radius = int(radius)
        if radius > 100 or radius < 1:
            return f'Radius {radius} is invalid.', 400

    # If the state is noresult, return an empty list
    if current_state == 'noresult':
        return json.dumps([]) 

    # Get the coords, if they were given
    latlong = (float(latitude), float(longitude)) if latitude is not None and longitude is not None else None

    # If the state is good, return some random results
    if current_state == 'good':
        results = []
        limit = int(limit)
        for i in range(randint(0, limit)):
            results.append(gen_fake_listing(city, state, latlong, radius))
            
        return json.dumps(results)


    # If we made it this far, return an error
    return 'The server exploded just before your request was made.', 500


if __name__ == '__main__':
    app.run(port=8080)
