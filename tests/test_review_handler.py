import unittest
import pandas as pd
import os
from data_classes.review_handler import ReviewHandler
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('REVIEWS_API_URL') 
api_key = os.getenv('REVIEWS_API_KEY')

class TestReviewHandler(unittest.TestCase):

    def setUp(self):
        """ Set up the ReviewHandler class """
        self.rh = ReviewHandler(url, api_key)

    def test_location_search(self):
        results = self.rh.location_search(39.774235, -86.175278, results=5)
        self.assertEqual(type(results), pd.DataFrame, 'location_search did not return dataframe.')

        # Check that the data has certain columns
        columns = list(results.columns)
        self.assertTrue('name' in columns, 'location_search result missing business name column.')
        self.assertTrue('stars' in columns, 'location_search result missing stars column.')
