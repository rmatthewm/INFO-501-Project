# Handle data from the Yelp dataset

import requests
import pandas as pd

class ReviewHandler:
    def __init__(self, base_url, api_key):
        """Constructor"""
        self.__base_url = base_url 
        self.__api_key = api_key

    def location_search(self, lat, long, results=2000, max_dist=5):
        """ Returns a given number of businesses near the coords given

        Args:
            lat (float): latitude
            long (float): longitude
            results (int, optional): the number of results to return. Defaults to 2500
            based on testing to get most businesses within a 5 mile radius.
            max_dist (int, optional): the max distance in miles from the coords. Defaults to 5

        Returns:
            pd.DataFrame: a dataframe containing the business data from the results
        """
        # Get the url
        url = f'{self.__base_url}/reviews'

        # Add the args as search params
        params = {'latitude': lat, 'longitude': long, 'results': results, 'max_dist': max_dist}

        # Create the headers for authentication
        headers = {'Accept': 'application/json', 'X-Api-Key': self.__api_key}

        # Get the review data from the api
        try:
            response = requests.get(url, params=params, headers=headers)

            # Convert to a dataframe
            reviews = pd.json_normalize(response.json())

            # Convert the stars to a float
            reviews['stars'] = reviews['stars'].astype('float')

        except Exception as e:
            print(e)
            return pd.DataFrame()

        return reviews

    def location_search_dist_stats(self, lat, long, results=10):
        """ Returns the mean, max, and min distance from lat, long returned given
        the number of results requested. This is mostly to understand how sparse the
        dataset is so we can calibrate how many results to return to reasonably 
        capture all the businesses in a given radius 

        Args:
            lat (float): latitude
            long (float): longitude
            results (int, optional): the number of results to pull from the data. Defaults to 10.

        Returns:
            tuple: (mean, max, min) distances from the coords given 
        """
        results = self.location_search(lat, long, results)

        # Calculate the distances
        mean = results['distance'].mean()
        max = results['distance'].max()
        min = results['distance'].min()

        return (mean, max, min)


    def min_results_for_all_businesses(self, lat, long, dist=5):
        """ Find the minimum number of results needed from the data
        in order to find all businesses within a certain distance from
        the given coords

        Args:
            lat (float): latitude
            long (float): longitude
            dist (int, optional): distance in miles from coords. Defaults to 5.

        Returns:
            int: the minimum number of results up to a cap
        """
        # This is the max number of businesses it can request
        max_req_results = 20000

        # The number of businesses found on the last iteration
        previous_num_bus = 0 

        # The number of businesses found on this iteration
        num_bus = 0 

        # In case there are some businesses near the edge, we need
        # 3 repetitions with no change to end
        unchanged_reps = 0

        # The number of results we will request from the data
        req_results = 0

        while unchanged_reps < 3 and req_results < max_req_results:
            # Each try will increase the number of results requested by 100
            req_results += 100

            # Get the results
            results = self.location_search(lat, long, req_results)

            # Find how many are within a certain distance
            num_bus = (results['distance'] <= 5.0).sum()

            # Check if we have gotten more this time
            if num_bus == previous_num_bus:
                unchanged_reps += 1
            else:
                previous_num_bus = num_bus
                unchanged_reps = 0

        # Unless we hit the cap, subtract 300 because we checked 3 more times without a change
        if req_results == max_req_results:
            return req_results
        else:
            return req_results - 300
