import unittest
from tests.test_data_handler import TestDataHandler
from tests.test_api_handler import TestApiHandler
from tests.test_review_handler import TestReviewHandler

loader = unittest.TestLoader()
suite = unittest.TestSuite()

# Add all the test cases to run together
suite.addTests(loader.loadTestsFromTestCase(TestDataHandler))
suite.addTests(loader.loadTestsFromTestCase(TestApiHandler))
suite.addTests(loader.loadTestsFromTestCase(TestReviewHandler))

runner = unittest.TextTestRunner()
runner.run(suite)