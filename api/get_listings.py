# Get listings from those cached by the api call

from haversine import haversine, Unit
import json

def get_listings(lat=None, long=None, radius=None, city=None, state=None, limit=None, bedrooms=None):
    # Add default data
    if limit is None:
        limit = 500

    # Read in the listings from the cached files 
    with open('data/rent_cast/listings.json', 'r') as file:
        text = file.read()
        data = json.loads(text)

    print(len(data))

    # We need to filter the items we have cached by the criteria given.
    # There shouldn't be too many so we can run through them this way.
    listings = []
    for listing in data:
        passed_filters = True

        # Check if it is within the given distance
        if lat is not None and long is not None and radius is not None:
            if haversine((float(lat), float(long)), (float(listing['latitude']), float(listing['longitude'])), Unit.MILES) > float(radius):
                passed_filters = False

        # Check if it is in the given city
        if city is not None and state is not None:
            if listing['city'] != city or listing['state'] != state:
                passed_filters = False

        # Check that it has the correct number of bedrooms
        if bedrooms is not None and int(listing['bedrooms']) != int(bedrooms):
            passed_filters = False

        # Add this listing if it has not been filtered out
        if passed_filters:
            listings.append(listing)

    return listings
