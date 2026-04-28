import unittest
from tests.test_data_handler import TestDataHandler
from tests.test_api_handler import TestApiHandler

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(TestDataHandler))
suite.addTests(loader.loadTestsFromTestCase(TestApiHandler))

runner = unittest.TextTestRunner()
runner.run(suite)