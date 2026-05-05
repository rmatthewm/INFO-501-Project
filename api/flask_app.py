# Return data pulled from the RentCast API so we do not need to make so many requests

import os
import json
from flask import Flask, request as req
from random import randint
from dotenv import load_dotenv
from get_listings import get_listings
from api_review_handler import APIReviewHandler

load_dotenv()

api_key = os.getenv('REVIEWS_API_KEY')
reviews_file = os.getenv('REVIEWS_PATH')

# Create the review handler
rh = APIReviewHandler(reviews_file)

app = Flask(__name__)

@app.route('/')
def controls():
    return 'hello there' 

@app.route('/v1/listings/rental/long-term')
def api():
    """ This route returns rental listings matching the RentCast search params """
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

@app.route('/reviews')
def reviews():
    """ This route returns nearby business Yelp review data """

    # First, check for authentication
    header1 = req.headers.get('Accept')
    header2 = req.headers.get('X-Api-Key')

    # If they do not have the proper headers, deny them access
    if header1 is None or header1 != 'application/json':
        return 'Access denied', 405

    if header2 is None or header2 != api_key:
        return 'Access denied', 405

    # Get the query options
    lat = float(req.args.get('latitude'))
    long = float(req.args.get('longitude'))
    results = req.args.get('results')
    max_dist = req.args.get('maxDist')

    # Correct the data types if optional args are given
    if results is not None:
        results = int(results)

    if max_dist is not None:
        max_dist = int(max_dist)

    return json.dumps(rh.location_search(lat, long, results, max_dist))


if __name__ == '__main__':
    app.run(port=8080)
