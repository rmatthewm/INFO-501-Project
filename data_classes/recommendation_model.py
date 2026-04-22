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

        # If a business is closed, how much should the Yelp review
        # be weighted? Open businesses are weighted 1.
        # We may want to still give a non 0 weight to closed businesses
        # for various reasons, for example if there is not a lot of data
        # in an area.
        self.closed_bus_weight = 0.1

    def score_reviews(self, lat, long):
        # Get the review data around theses coords
        reviews = self.rh.location_search(lat, long)

        open_filter = reviews['is_open'] == 1

        # Take the mean of the reviews, but accounting for the weight of
        # closed businesses
        score = reviews[open_filter]['stars'].mean()

        # Normalize the score to between (0, 100)
        return 20*score

    def score_distance(self, dist):
        # By using a quadratic score, the score won't drop as quickly
        # for closer locations but faster for longer distances
        score = -0.2*(dist**2) + 100

        if score < 0:
            return 0

        return score

    def score_price(self, county, state, beds, price):
        # The price score will be relative to the fair market rent price for its county 
        # This is adjusted to be between (0, 100)
        fmr = self.fmrh.get_county_fmr(county, state, beds)
        c = 50 / fmr
        score = ((2*fmr) - price) * c

        # Keep it non negative. It will only hit 0 if it is more than twice the fair price
        if score < 0:
            return 0

        return score

    def score_listing(self, lat, long, county, state, beds, dist, price):
        # Get the score for the reviews in the area
        review_score = self.score_reviews(lat, long)

        # Get the score for the distance
        distance_score = self.score_distance(dist)

        # Get the score for the price
        price_score = self.score_price(county, state, beds, price)

        # Return the weighted score
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
