
# Testing pyqhtools
# By Chas Egan
from unittest import TestCase
import pyqhtools

class TestTimeseries(TestCase):
    def test_timeseries_constructor_returns_something(self):
        # Capture result of function
        result = Timeseries()
        # Check result
        self.assertTrue(result != None)
