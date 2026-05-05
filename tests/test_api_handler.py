import unittest
import os
import pandas as pd
from dotenv import load_dotenv
from data_classes.api_handler import APIHandler

# Load in our environment variables
load_dotenv()
API_URL = os.getenv('LISTINGS_API_URL')
API_KEY = os.getenv('LISTINGS_API_KEY')

class TestApiHandler(unittest.TestCase):

    def setUp(self):
        """ Set up the APIHandler class """
        self.api = APIHandler(API_URL, API_KEY)

    def test_get_listings_by_city(self):
        """ Check that we get rental listings back """
        results = self.api.get_listings_by_city('Indianapolis', 'IN', limit=5)
        self.assertEqual(type(results), pd.DataFrame, 'get_listings_by_city does not return dataframe.')

        # Check the data has some of the key information
        columns = list(results.columns)
        self.assertTrue('price' in columns, 'get_listings_by_city result does not contain a price column.')
        self.assertTrue('addressLine1' in columns, 'get_listings_by_city result does not contain an addressLine1 columns.')

    def test_get_listings_by_coords(self):
        """ Check that we get rental listings back """
        results = self.api.get_listings_by_coords(39.774235, -86.175278, 10, beds=1, limit=5)
        self.assertEqual(type(results), pd.DataFrame, 'get_listings_by_city does not return dataframe.')

        # Check the data has some of the key information
        columns = list(results.columns)
        self.assertTrue('price' in columns, 'get_listings_by_coords result does not contain a price column.')
        self.assertTrue('addressLine1' in columns, 'get_listings_by_coords result does not contain an addressLine1 columns.')
