# A model to recommend listings to the user

class RecommendationModel:
    def __init__(self):
        self.__fmr_data_cache = {}

    def recommend_listings(self, listings):
