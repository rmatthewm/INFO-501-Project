# A model to recommend listings to the user
from review_handler import ReviewHandler
from data_handler import DataHandler
from haversine import haversine, Unit

class RecommendationModel:
    def __init__(self, review_handler, fmr_handler):
        # We will need a review handler and data handler
        self.rh = review_handler
        self.fmrh = fmr_handler

        self.dist_weight = 25
        self.review_weight = 25
        self.price_weight = 50
        self.total_weight = self.dist_weight + self.review_weight + self.price_weight

    def score_reviews(self, lat, long):
        return 100

    def score_listing(self, lat, long, county, state, beds, distance, price):
        fmr = self.fmrh.get_county_fmr(county, state, beds)
        review_score = self.score_reviews(lat, long)

        distance_score = 100

        # The price score will be relative to the fair market rent price for its county 
        # This is adjusted to be between (0, 100)
        c = 50 / fmr
        price_score = ((2*fmr) - price) * c

        # Keep it non negative. It will only hit 0 if it is more than twice the fair price
        if price_score < 0:
            price_score = 0

        return (distance_score*self.dist_weight + review_score*self.review_weight + 
                price_score*self.price_weight) / self.total_weight

    def recommend_listings(self, listings, lat, long, top=10):
        # Calculate the distance from the desired coords
        listings['distance'] = listings.apply(lambda row: haversine((lat, long), (row['latitude'], row['longitude']), Unit.MILES), axis=1)

        # Calculate the scores for the listings
        listings['score'] = listings.apply(lambda row: self.score_listing(row['latitude'], row['longitude'], row['distance'], row['price']), axis=1)

        # Sort by the scores
        listings.sort_values(by='score', ascending=False)

        # Return the top items
        return listings.head(top)

