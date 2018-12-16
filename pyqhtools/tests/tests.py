
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

    def test_loading_data_twice_gives_same_timeseries(self):
        # Capture result of function
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        ts2 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        comparison_results = ts1.compare(ts2)
        # Check result
        self.assertTrue(comparison_results[0] == True)
        self.assertTrue(ts1.source == ts2.source)

    def test_scaling_dataset_positive(self):
        # Capture result of function
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        ts1.scale(10.0)
        # Check result
        self.assertTrue(ts1.min == 0.0)
        self.assertTrue(ts1.max == 4940.0)
        self.assertTrue(abs(ts1.mean - 51.9659885) < 0.01)
        self.assertTrue(abs(ts1.std - 168.0) < 1)

    def test_scaling_dataset_negative(self):
        # Capture result of function
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        ts1.scale(-0.1)
        # Check result
        self.assertTrue(abs(ts1.min - (-49.4)) < 0.01)
        self.assertTrue(ts1.max == 0.0)
        self.assertTrue(abs(ts1.mean - (-0.519659885)) < 0.01)
        self.assertTrue(abs(ts1.std - 1.68) < 0.1)
