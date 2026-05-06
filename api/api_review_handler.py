# Handle data from the Yelp dataset

import pygeohash as pgh
from haversine import haversine, Unit
from itertools import islice

class APIReviewHandler:
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

    def location_search(self, locations, results=None, max_dist=None):
        """ Returns a given number of businesses near the coords given

        Args:
            locations (dict): a dictionary of lat, long coords with listing id as the key
            results (int, optional): the number of results to return. Defaults to 2500
            based on testing to get most businesses within a 5 mile radius.
            max_dist (int, optional): the max distance in miles from the coords. Defaults to 5

        Returns:
            list (json): a "json" object containing the mean stars for the business near each location 
        """
        # Set default values
        if results is None:
            results = 2000

        if max_dist is None:
            max_dist = 5

        # Get the index bounds for each location first. Then we can get all
        # the reviews at once without repeats
        review_bounds = {}
        min_bound = self.__business_length
        max_bound = 0

        # Find the bounds for each location
        for key in list(locations.keys()):

            # Get the geohash from the lat and long
            search_hash = pgh.encode(float(locations[key][0]), float(locations[key][1]))

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
            # We want a window of results centered around this point. We also
            # need to make sure the window doesn't go out of bounds.
            if mid - (results // 2) >= 0:
                start = mid - (results // 2)
            else:
                start = 0

            if mid + (results // 2) <= self.__business_length:
                end = mid + (results // 2)
            else:
                end = self.__business_length - 1

            # Save the bounds for the window for this listing
            review_bounds[key] = [start, end]

            if start < min_bound:
                min_bound = start

            if end > max_bound:
                max_bound = end

        # Read the data containing all the windows into memory
        with open(self.__file_path, 'r') as file:
            data = list(islice(file, min_bound, max_bound))

        # Add up the stars for the relevant reviews
        reviews = {}
        for key in list(review_bounds.keys()):
            reviews[key] = {'open': 0, 'open_total': 0, 'closed': 0, 'closed_total': 0}

        for i in range(len(data)):
            # Find the original index
            i_offset = i + min_bound

            # Split apart the csv to json-like
            items = data[i].split(',')
            review_obj = {}
            for i in range(len(items)):
                review_obj[self.__header[i]] = items[i]

            # Find which listings need this business
            for key in list(review_bounds.keys()):
                if i_offset >= review_bounds[key][0] and i_offset <= review_bounds[key][1]:
                    # Only include if it is within the max distance 
                    dist = haversine((locations[key][0], locations[key][1]), (float(review_obj['latitude']), float(review_obj['longitude'])), Unit.MILES)
                    if dist < max_dist:
                        # Add this review to the listing
                        if review_obj['is_open'] == '1\n':
                            reviews[key]['open'] += float(review_obj['stars'])
                            reviews[key]['open_total'] += 1
                        else:
                            reviews[key]['closed'] += float(review_obj['stars'])
                            reviews[key]['closed_total'] += 1

        # Calculate the means
        for key in list(reviews.keys()):
            if reviews[key]['open_total'] > 0:
                reviews[key]['open'] = reviews[key]['open'] / reviews[key]['open_total']

            if reviews[key]['closed_total'] > 0:
                reviews[key]['closed'] = reviews[key]['closed'] / reviews[key]['closed_total']
                
        return reviews
