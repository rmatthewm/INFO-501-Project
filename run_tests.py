import unittest
from tests.test_data_handler import TestDataHandler

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromTestCase(TestDataHandler))

runner = unittest.TextTestRunner()
runner.run(suite)