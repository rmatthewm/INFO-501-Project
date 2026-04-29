# Return data pulled from the RentCast API so we do not need to make so many requests

import os
import json
from flask import Flask, request as req
from random import randint
from dotenv import load_dotenv
from get_listings import get_listings

load_dotenv()

api_key = os.getenv('LISTINGS_API_KEY')

app = Flask(__name__)


@app.route('/')
def controls():
    return 'hello there' 

@app.route('/v1/listings/rental/long-term')
def api():
    # First, check for authentication
    header1 = req.headers.get('Accept')
    header2 = req.headers.get('X-Api-Key')

    # If they do not have the proper headers, deny them access
    if header1 is None or header1 != 'application/json':
        return 'Access denied', 405

    if header2 is None or header2 != api_key:
        return 'Access denied', 405

    # Next, we need to get the query options
    city = req.args.get('city')
    state = req.args.get('state')
    latitude = req.args.get('latitude')
    longitude = req.args.get('longitude')
    radius = req.args.get('radius')
    limit = req.args.get('limit', '200')
    bedrooms = req.args.get('bedrooms')

    # Return the relevant listings from the cache
    listings = get_listings(latitude, longitude, radius, city, state, limit, bedrooms)
    return json.dumps(listings)


if __name__ == '__main__':
    app.run(port=8080)
