import os
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

# These are commented out to avoid accidentally running and spending an API call
#api_key = os.getenv('RENTCAST_API_KEY')
#base_url = os.getenv('RENTCAST_API_URL')

# Search params
latitude = 39.774235
longitude = -86.175278
radius = 20

def main():
    listings = []

    offset = 0
    # Get multiple pages of results to save
    for i in range(1):

        # Get the url to find rental listings
        url = f'{base_url}/v1/listings/rental/long-term'

        # Pass in the coords as search params
        params = {'latitude': latitude, 'longitude': longitude, 'radius': radius, 'includeTotalCount': 'true', 'limit': 500, 'offset': offset}

        # Create the headers for authentication
        headers = {'Accept': 'application/json', 'X-Api-Key': api_key}

        # Make the request
        try:
            response = requests.get(url, params=params, headers=headers)
            print(response.headers)

        except Exception as e:
            # Print to the console for debugging
            print(e)
            # If we encounter any error, stop repeating
            break

        # Add the listing
        listings += response.json()

        offset += 500

        # Save the listings
        with open('data/rent_cast/listings.json', 'w') as file:
            file.write(json.dumps(listings, indent=4))
            print(f'file written ({i})')

        # Since we have such limited number of calls, don't risk hitting any
        # rate limits and wait 5 seconds between each call
        time.sleep(5)

if __name__ == '__main__':
    start = input('Are you sure you want to run a series of API calls? "Yes" or anything else to exit ->')
    if start == 'Yes':
        main()
    
    print('exiting')