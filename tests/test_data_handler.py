import unittest
import pandas as pd
from dotenv import load_dotenv
from ..data_classes.data_handler import DataHandler

# Load in our development environment variables
load_dotenv()

class TestDataHandler(unittest.TestCase):

    def setUp(self):
        """ Set up the DataHandler class """
        self.dh = DataHandler('data/rental_data.csv', 'data/rental_data_columns.csv')


    def test_get_dataframe(self):
        """ Check that we get a dataframe """
        df = self.dh.get_dataframe()
        self.assertEqual(type(df), pd.DataFrame)
        self.assertFalse(df.empty)

    def test_get_state_codes(self):
        """ Check that we get a series of state codes back """
        state_codes = self.dh.get_state_codes()
        self.assertEqual(type(state_codes), pd.Series)
        self.assertGreaterEqual(len(state_codes), 50)

if __name__ == '__main__':
    unittest.main()