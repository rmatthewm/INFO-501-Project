# A model to recommend listings to the user
from review_handler import ReviewHandler
from data_handler import DataHandler
from haversine import haversine, Unit

class RecommendationModel:
    def __init__(self, review_handler, fmr_handler):
        # We will need a review handler and data handler
        self.rh = review_handler
        self.fmrh = fmr_handler

    def score_listing(lat, long, distance, price):
        return 

    def recommend_listings(self, listings, lat, long, top=10):
        # Calculate the distance from the desired coords
        listings['distance'] = listings.apply(lambda row: haversine((lat, long), (row['latitude'], row['longitude']), Unit.MILES), axis=1)

        # Calculate the scores for the listings
        listings['score'] = listings.apply(lambda row: self.score_listing(row['latitude'], row['longitude'], row['distance'], row['price']), axis=1)

        # Sort by the scores
        listings.sort_values(by='score', ascending=False)

        # Return the top items
        return listings.iloc[:top]

