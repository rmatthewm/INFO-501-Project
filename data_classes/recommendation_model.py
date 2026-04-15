# A model to recommend listings to the user
from review_handler import ReviewHandler
from data_handler import DataHandler

class RecommendationModel:
    def __init__(self, review_handler, fmr_handler):
        # We will need a review handler and data handler
        self.rh = review_handler
        self.fmrh = fmr_handler

    def recommend_listings(self, listings):

