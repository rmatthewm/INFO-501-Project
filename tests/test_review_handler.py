import unittest
import pandas as pd
from data_classes.review_handler import ReviewHandler

class TestReviewHandler(unittest.TestCase):

    def setUp(self):
        """ Set up the ReviewHandler class """
        self.rh = ReviewHandler('data/yelp_businesses.csv')

    def test_get_business(self):
        """ Check that we get a business back """
        business = self.rh.get_business(0)
        name = business.split(',')[3]
        self.assertEqual(name, 'Dos Pueblos Orchid Farm', f'get_business did not return correct business (returned {name}).')

    def test_location_search(self):
        results = self.rh.location_search(39.774235, -86.175278, results=5)
        self.assertEqual(type(results), pd.DataFrame, 'location_search did not return dataframe.')

        # Check that the data has certain columns
        columns = list(results.columns)
        self.assertTrue('name' in columns, 'location_search result missing business name column.')
        self.assertTrue('stars' in columns, 'location_search result missing stars column.')
