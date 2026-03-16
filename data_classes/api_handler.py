# A wrapper for interacting with the RentalCast API

import requests


class APIHandler:
    def __init__(self, base_url, api_key):
        self.__base_url = base_url
        self.__api_key = api_key

    def get_listings_by_city(self, city, state):
        # Get the url to find rental listings
        url = f'{self.__base_url}/v1/listings/rental/long-term'

        # Pass in the city and state as search params
        params = {'city': city, 'state': state}

        # Create the headers for authentication
        headers = {'Accept': 'application/json', 'X-Api-Key': self.__api_key}

        # Make the request
        try:
            response = requests.get(url, params)

        except Exception as e:
            # Print to the console for debugging
            print(e)

            # From the outside perspective, we can just return an empty list
            return []

        # Return the listings
        return response.json() 

    def get_listings_by_coords(self, latitude, longitude, radius):
        # Get the url to find rental listings
        url = f'{self.__base_url}/v1/listings/rental/long-term'

        # Pass in the city and state as search params
        params = {'latitude': latitude, 'longitude': longitude, 'radius': radius}

        # Create the headers for authentication
        headers = {'Accept': 'application/json', 'X-Api-Key': self.__api_key}

        # Make the request
        try:
            response = requests.get(url, params)

        except Exception as e:
            # Print to the console for debugging
            print(e)

            # From the outside perspective, we can just return an empty list
            return []

        # Return the listings
        return response.json()