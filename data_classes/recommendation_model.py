# A model to recommend listings to the user
import pandas as pd
from data_classes.review_handler import ReviewHandler
from data_classes.data_handler import DataHandler
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

    def score_reviews(self, id, reviews):
        # Get the means from the review data
        open_score = float(reviews[id]['open']) 
        closed_score = float(reviews[id]['closed']) 

        # We have 4 scenarios of what data we might have
        # Case 1: No open or closed data
        score = 0 

        # Case 2: Both open and closed data
        if int(reviews[id]['open_total']) > 0 and int(reviews[id]['closed_total']) > 0:
            score = (open_score + closed_score*self.closed_bus_weight) / (1 + self.closed_bus_weight)
        
        # Case 3: Only open data
        elif int(reviews[id]['open_total']) > 0:
            score = open_score

        # Case 4: Only closed data, in this case we will weight it 1 since its all we have
        elif int(reviews[id]['closed_total']) > 0:
            score = closed_score

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
        # If there are more than 4 beds, compare it to the rate for 4 bedrooms
        if beds > 4:
             beds = 4

        # The price score will be relative to the fair market rent price for its county 
        # This is adjusted to be between (0, 100)
        fmr = self.fmrh.get_county_fmr(county, state, beds)
        c = 50 / fmr
        score = ((2*fmr) - price) * c

        # Keep it non negative. It will only hit 0 if it is more than twice the fair price
        if score < 0:
            return 0

        return score

    def score_listing(self, id, reviews, county, state, beds, dist, price):
        # Get the score for the reviews in the area
        review_score = self.score_reviews(id, reviews)

        # Get the score for the distance
        distance_score = self.score_distance(dist)

        # Get the score for the price
        price_score = self.score_price(county, state, beds, price)

        # Return the weighted score
        return (distance_score*self.dist_weight + review_score*self.review_weight + 
                price_score*self.price_weight) / self.total_weight

    def recommend_listings(self, listings, lat, long, top=10):
        # Make sure we have floats for coords
        lat = float(lat)
        long = float(long)

        # Gather all the locations to request the reviews
        locations = {}
        for i in range(len(listings)):
            locations[listings.iloc[i]['id']] = [listings.iloc[i]['latitude'], listings.iloc[i]['longitude']]
        reviews = self.rh.location_search(locations)

        # Calculate the distance from the desired coords
        listings['distance'] = listings.apply(lambda row: haversine((lat, long), (float(row['latitude']), float(row['longitude'])), Unit.MILES), axis=1)

        # Calculate the scores for the listings
        listings['score'] = listings.apply(lambda row: self.score_listing(row['id'], reviews, row['county'], row['state'], row['bedrooms'], row['distance'], row['price']), axis=1)

        # Sort by the scores
        listings = listings.sort_values(by='score', ascending=False)

        # Return the top items
        return listings.head(top)
