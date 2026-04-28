import unittest
import pandas as pd
from dotenv import load_dotenv
from data_classes.data_handler import DataHandler

# Load in our development environment variables
load_dotenv()

class TestDataHandler(unittest.TestCase):

    def setUp(self):
        """ Set up the DataHandler class """
        self.dh = DataHandler('data/rental_data.csv', 'data/rental_data_columns.csv')


    def test_get_dataframe(self):
        """ Check that we get a dataframe """
        df = self.dh.get_dataframe()
        self.assertEqual(type(df), pd.DataFrame, 'get_dataframe did not return dataframe.')
        self.assertFalse(df.empty, 'get_dataframe returned empty dataframe.')

    def test_get_state_codes(self):
        """ Check that we get a list of state codes back """
        state_codes = self.dh.get_state_codes()
        self.assertEqual(type(state_codes), list, 'get_state_codes does not return a list.')
        self.assertGreaterEqual(len(state_codes), 50, 'get_state_codes does not return enough values.')

    def test_get_columns(self):
        """ Check that we get an index of column names back """
        columns = self.dh.get_columns()
        self.assertEqual(type(columns), pd.Index, 'get_columns does not return index.')
        self.assertEqual(len(columns), 14, 'get_columns does not return the number of columns matching the data.')

    def test_get_col_fancy_name(self):
        """ Check that we get the correct fancy name back """
        county_name = self.dh.get_col_fancy_name('countyname')
        self.assertEqual(county_name, 'County Name', 'get_col_fancy_name did not return correct name for countyname.')

    def test_get_county_fmr(self):
        """ Check that we get the correct fmr value """
        fmr = self.dh.get_county_fmr('Marion', 'IN', 1)
        self.assertEqual(fmr, 1267, 'get_county_fmr did not return correct fmr.')

    def test_get_average_rate(self):
        """ Check we get a reasonable number for the average fmr """
        country = self.dh.get_average_rate(bed_count=1)
        state = self.dh.get_average_rate(state='IN', bed_count=1)
        self.assertGreater(country, 500, 'get_average_rate returned unreasonably low value for country.')
        self.assertGreater(state, 500, 'get_average_rate returned unreasonably low value for Indiana.')

    def test_get_cheapest_counties(self):
        """ Check we get data back for the cheapest counties """
        country = self.dh.get_cheapest_counties(n_results=5)
        state = self.dh.get_cheapest_counties(state='IN', n_results=5)
        self.assertEqual(type(country), pd.DataFrame, 'get_cheapest_counties did not return dataframe for country.')
        self.assertEqual(type(state), pd.DataFrame, 'get_cheapest_counties did not return dataframe for Indiana.')
        self.assertEqual(len(country), 5, 'get_cheapest_counties did not return n_results for country.')
        self.assertEqual(len(state), 5, 'get_cheapest_counties did not return n_results for Indiana.')


if __name__ == '__main__':
    unittest.main()