import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('RENTCAST_API_KEY')
base_url = os.getenv('RENTCAST_API_URL')

# Search params
latitude = 39.774235
longitude = -86.175278
radius = 50

def main():
    # Get the url to find rental listings
    url = f'{base_url}/v1/listings/rental/long-term'

    # Pass in the coords as search params
    params = {'latitude': latitude, 'longitude': longitude, 'radius': radius}

    # Create the headers for authentication
    headers = {'Accept': 'application/json', 'X-Api-Key': api_key}

    # Make the request
    try:
        response = requests.get(url, params=params, headers=headers)

    except Exception as e:
        # Print to the console for debugging
        print(e)

    # Save the listings
    with open('data/rent_cast/listings.json', 'a') as file:
        file.write(json.dumps(response.json()))
        print('file written')

if __name__ == '__main__':
    main()