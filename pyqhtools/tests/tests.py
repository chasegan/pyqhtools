
# Testing pyqhtools
# By Chas Egan
from unittest import TestCase
import pyqhtools as pqh

class TestTimeseries(TestCase):
    def test_timeseries_constructor_returns_something(self):
        # Capture result of function
        result = pqh.Timeseries()
        # Check result
        self.assertTrue(result != None)

    def test_load_csv_returns_something(self):
        # Capture result of function
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\p040134.csv")
        # Check result
        self.assertTrue(result != None)

    def test_length_and_missing_with_complete_dataset(self):
        # Capture result of function
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\p040134.csv")
        # Check result
        self.assertTrue(result.length == 47463)
        self.assertTrue(result.count == 47463)
        self.assertTrue(result.missing == 0)
        self.assertTrue(result.nonmissing == 47463)

    def test_length_and_missing_with_gappy_dataset(self):
        # Capture result of function
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        # Check result
        self.assertTrue(result.length == 39271)
        self.assertTrue(result.count == 39271)
        self.assertTrue(result.missing == 784)
        self.assertTrue(result.nonmissing == 38487)

    def test_min_max_mean_std_with_gappy_dataset(self):
        # Capture result of function
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        # Check result
        self.assertTrue(result.min == 0.0)
        self.assertTrue(result.max == 494.0)
        self.assertTrue(abs(result.mean - 5.19659885) < 0.01)
        self.assertTrue(abs(result.std - 16.8) < 0.1)
