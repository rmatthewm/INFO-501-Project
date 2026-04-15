# Handle data from the Yelp dataset

import pygeohash as pgh
import pandas as pd
from haversine import haversine, Unit
from itertools import islice
from io import StringIO

class ReviewHandler:
    def __init__(self, file_path):
        """Constructor"""
        self.__file_path = file_path
        self.__business_length = self.get_file_length(file_path)

        # The column names for the data
        self.__header = ['latitude', 'longitude', 'business_id', 'name', 'address', 
                         'city', 'state', 'postal_code', 'stars', 'review_count', 'is_open']

    def get_file_length(self, file_path):

        length = 0
        with open(file_path, 'r') as file:
            # Count all of the items
            item = next(file, None)
            while item is not None:
                length += 1
                item = next(file, None)

        return length

    def get_business(self, i):
        """ Return a business at index i, None if not found

        Args:
            i (int): the index

        Returns:
            str: the entry in the business csv
        """
        with open(self.__file_path, 'r') as file:
            slice_result = list(islice(file, i, i+1))
        
        if len(slice_result) > 0:
            return slice_result[0]
        
        return None

    def location_search(self, lat, long, results=10):
        """ Returns a given number of businesses near the coords given

        Args:
            lat (float): latitude
            long (float): longitude
            results (int, optional): the number of results to return. Defaults to 10.

        Returns:
            pd.DataFrame: a dataframe containing the business data from the results
        """
        # Get the geohash from the lat and long
        search_hash = pgh.encode(float(lat), float(long))

        # Get the search range which we will repeatedly half
        start = 0
        end = self.__business_length
        current_hash = '' 
        while current_hash != search_hash and end - start > 1:
            # Get the middle business in the search range
            mid = ((end - start) // 2) + start
            business = self.get_business(mid).split(',')
            current_hash = pgh.encode(float(business[0]), float(business[1]))

            # Check which side to keep searching
            if search_hash < current_hash:
                end = mid
            else:
                start = mid

        # The result will be at the current mid index. This may not be
        # an exact match but will represent the closest business in the database.
        # Return a window of results centered around this point. We also
        # need to make sure the window doesn't go out of bounds.
        if mid - (results // 2) >= 0:
            start = mid - (results // 2)
        else:
            start = 0

        if mid + (results // 2) <= self.__business_length:
            end = mid + (results // 2)
        else:
            end = self.__business_length

        with open(self.__file_path, 'r') as file:
            results = list(islice(file, start, end))

        # Wrap the string in an IO object so pandas can read it like a file
        results_filelike = StringIO('\n'.join(results))
        df = pd.read_csv(results_filelike, names=self.__header)

        # Add the distance from the given coords
        df['distance'] = df.apply(lambda row: haversine((lat, long), (row['latitude'], row['longitude']), Unit.MILES), axis=1)
        return df

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


# testing
if __name__ == '__main__':
    rh = ReviewHandler('data/yelp_businesses.csv')

    locations = [(39.774, -86.175), (39.597, -86.102), (33.439, -112.069)]

    # Find how many results are needed to find all businesses within a 5 miles radius
    # from three locations
    for loc in locations:
        print(rh.min_results_for_all_businesses(loc[0], loc[1]))