# A wrapper for interacting with the RentalCast API

import requests
import pandas as pd

class APIHandler:
    def __init__(self, base_url, api_key):
        self.__base_url = base_url
        self.__api_key = api_key

    def get_listings_by_city(self, city, state, limit=None):
        """ Pulls listings in a given city from the API

        Args:
            city (str): the city
            state (str): the state
            limit (int, optional): max number of items to return. Defaults to None.

        Returns:
            pd.DataFrame: a dataframe containing the listings
        """
        # Get the url to find rental listings
        url = f'{self.__base_url}/v1/listings/rental/long-term'

        # Pass in the city and state as search params
        params = {'city': city, 'state': state}

        # Add the limit if one was given 
        if limit is not None:
            params['limit'] = limit

        # Create the headers for authentication
        headers = {'Accept': 'application/json', 'X-Api-Key': self.__api_key}

        # Make the request
        try:
            response = requests.get(url, params=params, headers=headers)

        except Exception as e:
            # Print to the console for debugging
            print(e)

            # From the outside perspective, we can just return an empty dataframe 
            return pd.DataFrame()

        # Check that we got a good response
        if response.status_code == 200:
            # Return the listings
            return pd.json_normalize(response.json())

        # Otherwise, we can print what happened and return an empty list
        print(f'Response had status code {response.status_code}. Returned {response.content}')
        return pd.DataFrame()

    def get_listings_by_coords(self, latitude, longitude, radius, beds=None, limit=None):
        """ Pulls listings within a certain radius of given coords from the API

        Args:
            latitude (float): latitude
            longitude (float): longitude
            radius (int): the max radius from the coords to get listings
            limit (int, optional): max number of items to return. Defaults to None.

        Returns:
            pd.DataFrame: a dataframe containing the listings
        """
        # Get the url to find rental listings
        url = f'{self.__base_url}/v1/listings/rental/long-term'

        # Pass in the city and state as search params
        params = {'latitude': latitude, 'longitude': longitude, 'radius': radius}

        if beds is not None:
            params['bedrooms'] = beds

        # Add the limit if one was given 
        if limit is not None:
            params['limit'] = limit

        # Create the headers for authentication
        headers = {'Accept': 'application/json', 'X-Api-Key': self.__api_key}

        # Make the request
        try:
            response = requests.get(url, params=params, headers=headers)

        except Exception as e:
            # Print to the console for debugging
            print(e)

            # From the outside perspective, we can just return an empty dataframe 
            return pd.DataFrame() 

        # Return the listings
        return pd.json_normalize(response.json())
