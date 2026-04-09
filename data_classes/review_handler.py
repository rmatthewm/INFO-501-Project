# Handle data from the Yelp dataset

import pygeohash as pgh
from itertools import islice

class ReviewHandler:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__business_length = self.get_file_length(file_path)

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
        # Return a window of results centered around this point.
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

        return results

# testing
if __name__ == '__main__':
    rh = ReviewHandler('data/yelp_businesses.csv')
    # Insert whatever place for testing
    print(rh.location_search())