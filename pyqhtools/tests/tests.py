
# Testing pyqhtools
# By Chas Egan
from unittest import TestCase
import math
import datetime as dt
import pyqhtools as pqh

class TestTimeseries(TestCase):
    def test_timeseries_constructor_returns_something(self):
        '''
        Code tested:
            Timeseries.__init__()
        '''
        result = pqh.Timeseries()
        self.assertTrue(result != None)

    def test_start_end(self):
        '''
        Code tested:
            Timeseries.__get_end()
            Timeseries.get_start_end()
            Timeseries.start
            Timeseries.end
        '''
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\r040168.csv")
        start_end = result.get_start_end()
        self.assertTrue(start_end[0] == dt.datetime(1892, 11, 1))
        self.assertTrue(start_end[1] == dt.datetime(1980, 9, 30))

    def test_length_with_complete_dataset(self):
        '''
        Code tested:
            Timeseries.__get_count()
            Timeseries.__get_missing()
            Timeseries.__get_nonmissing()
            Timeseries.length
            Timeseries.count
            Timeseries.missing
            Timeseries.nonmissing
        '''
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\p040134.csv")
        self.assertTrue(result.length == 47463)
        self.assertTrue(result.count == 47463)
        self.assertTrue(result.missing == 0)
        self.assertTrue(result.nonmissing == 47463)

    def test_length_with_gappy_dataset(self):
        '''
        Code tested:
            As above
        '''
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        self.assertTrue(result.length == 39271)
        self.assertTrue(result.count == 39271)
        self.assertTrue(result.missing == 784)
        self.assertTrue(result.nonmissing == 38487)

    def test_length_with_multiline_headder(self):
        '''
        Code tested:
            As above
        '''
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\p040850_headder_missing_start_end.csv")
        self.assertTrue(result.length == 47463)
        self.assertTrue(result.count == 47463)
        self.assertTrue(result.missing == 26671)
        self.assertTrue(result.nonmissing == 20792)

    def test_min_max_mean_std_with_gappy_dataset(self):
        '''
        Code tested:
            Timeseries.__get_min()
            Timeseries.__get_max()
            Timeseries.__get_mean()
            Timeseries.__get_std()
            Timeseries.min
            Timeseries.max
            Timeseries.mean
            Timeseries.std
        '''
        result = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        self.assertTrue(result.min == 0.0)
        self.assertTrue(result.max == 494.0)
        self.assertTrue(abs(result.mean - 5.19659885) < 0.01)
        self.assertTrue(abs(result.std - 16.8) < 0.1)

    def test_loading_data_twice_gives_same_timeseries(self):
        '''
        Code tested:
            Timeseries.source
        '''
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        ts2 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        ts3 = pqh.load_csv(r".\pyqhtools\tests\test_data\p040168.csv")
        comparison_results = ts1.compare(ts2)
        self.assertTrue(comparison_results[0] == True)
        self.assertTrue(ts1.source == ts2.source)
        self.assertTrue(ts1.source != ts3.source)

    def test_clone_gives_same_timeseries(self):
        '''
        Code tested:
            Timeseries.clone()
        '''
        original = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        theclone = original.clone()
        #Clones should look the same
        comparison_results = original.compare(theclone)
        self.assertTrue(comparison_results[0] == True)
        #But should not be the same after I manually edit some data
        theclone.data[0] = 53.0
        comparison_results = original.compare(theclone)
        self.assertTrue(comparison_results[0] == False)

    def test_summary_has_no_errors(self):
        '''
        Code tested:
            Timeseries.summary()
        '''
        #emtpy_ts = pqh.Timeseries()
        #empty_ts.summary()
        loaded_ts = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        loaded_ts.summary()
        self.assertTrue(True)

    def test_scaling_dataset(self):
        '''
        Code tested:
            Timeseries.scale(value)
        '''
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        ts1.scale(10.0) #apply some positive scaling
        self.assertTrue(ts1.min == 0.0)
        self.assertTrue(ts1.max == 4940.0)
        self.assertTrue(abs(ts1.mean - 51.9659885) < 0.01)
        self.assertTrue(abs(ts1.std - 168.0) < 1)
        ts1.scale(-0.01) #apply some negative scaling
        self.assertTrue(abs(ts1.min - (-49.4)) < 0.01)
        self.assertTrue(ts1.max == 0.0)
        self.assertTrue(abs(ts1.mean - (-0.519659885)) < 0.01)
        self.assertTrue(abs(ts1.std - 1.68) < 0.1)

    def test_get_value(self):
        '''
        Code tested:
            Timeseries.get_value(year, month, day, date=None)
        '''
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        #Value before ts
        value = ts1.get_value(1910, 5, 1)
        self.assertTrue(math.isnan(value))
        #Value at start of ts
        value = ts1.get_value(1910, 6, 1)
        self.assertTrue(value == 26.9)
        #Value inside ts
        value = ts1.get_value(1910, 6, 2)
        self.assertTrue(value == 204.2)
        #Value inside ts (using datetime)
        value = ts1.get_value(0, 0, 0, date=pqh.parse_date("02-06-1910"))
        self.assertTrue(value == 204.2)
        #Missing value inside ts
        value = ts1.get_value(2012, 6, 26)
        self.assertTrue(math.isnan(value))
        #Value at end of ts
        value = ts1.get_value(2017, 12, 6)
        self.assertTrue(value == 36.0)
        #Value after ts
        value = ts1.get_value(2017, 12, 7)
        self.assertTrue(math.isnan(value))

    def test_set_value(self):
        '''
        Code tested:
            Timeseries.set_value(value, year, month, day, date=None)
        '''
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        #Value at start of ts
        ts1.set_value(99.9, 1910, 6, 1)
        self.assertTrue(ts1.get_value(1910, 6, 1) == 99.9)
        #Value inside ts
        ts1.set_value(99.9, 1910, 6, 2)
        self.assertTrue(ts1.get_value(1910, 6, 2) == 99.9)
        #Value at end of ts
        ts1.set_value(99.9, 2017, 12, 6)
        self.assertTrue(ts1.get_value(2017, 12, 6) == 99.9)

    def test_set_value_if_missing(self):
        '''
        Code tested:
            Timeseries.set_value(value, year, month, day, date=None)
        '''
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        #Value 26.9 is not missing and should not be changed
        ts1.set_value_if_missing(99.9, 1910, 6, 1)
        self.assertTrue(ts1.get_value(1910, 6, 1) == 26.9)
        #Value for 2012, 6, 26 is missing and should be changed
        ts1.set_value_if_missing(99.9, 2012, 6, 26)
        self.assertTrue(ts1.get_value(2012, 6, 26) == 99.9)

    def test_get_dates(self):
        '''
        Code tested:
            Timeseries.get_dates()
        '''
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        dates = ts1.get_dates()
        self.assertTrue(len(dates) == 39271)
        self.assertTrue(dates[0] == pqh.parse_date("01/06/1910"))

    def test_set_start_end(self):
        '''
        Code tested:
            Timeseries.set_start_end(start_and_end)
            Timeseries.set_start(year, month, day)
            Timeseries.set_end(year, month, day)
        '''
        #Load some patched-point data
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\p040134.csv")
        ts1_start_end = ts1.get_start_end()
        #Load some raw data and check length is different to above
        ts2 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        self.assertTrue(ts1.length != ts2.length)
        self.assertTrue(ts2.get_value(1910, 6, 1) == 26.9)
        #Extend the dates to be same as above and check lengths are now same
        ts2.set_start_end(ts1_start_end)
        self.assertTrue(ts1.length == ts2.length)
        self.assertTrue(ts2.get_value(1910, 6, 1) == 26.9)
        #Save the result for visual inspection
        pqh.save_csv(ts2, r".\pyqhtools\tests\test_data\r040134_redated.csv")

    def test_bias(self):
        '''
        Code tested:
            Timeseries.bias(other)
        '''
        #For cloned data the bias should be 1.0
        original = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        clone = original.clone()
        bias = clone.bias(original)
        self.assertTrue(abs(bias - 1.0) < 0.000000001)
        #Now scale ts2 up 40% and measure the bias again
        clone.scale(1.4)
        bias = clone.bias(original)
        self.assertTrue(abs(bias - 1.4) < 0.000000001)

    def test_infill_scale_auto_factor(self):
        '''
        Code tested:
            Timeseries.infill_scale(other)
        '''
        gappy_data = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        all_ones = pqh.load_csv(r".\pyqhtools\tests\test_data\all_ones.csv")
        mean_before_infilling = gappy_data.mean
        #infilling by infill_scale should preserve the mean
        gappy_data.infill_scale(all_ones)
        pqh.save_csv(gappy_data, r".\pyqhtools\tests\test_data\r040134_infilled.csv")
        #Check the results
        mean_after_infilling = gappy_data.mean
        self.assertTrue(abs(mean_before_infilling - mean_after_infilling) < 0.00001)
        self.assertTrue(gappy_data.get_value(1910, 6, 1) == 26.9)
        self.assertTrue(gappy_data.missing == 0)

    def test_infill_scale_force_factor(self):
        '''
        Code tested:
            Timeseries.infill_scale(other, factor=None)
        '''
        gappy_data = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        all_ones = pqh.load_csv(r".\pyqhtools\tests\test_data\all_ones.csv")
        gappy_data.infill_scale(all_ones, factor = 0.6666)
        pqh.save_csv(gappy_data, r".\pyqhtools\tests\test_data\r040134_infilled2.csv")
        #Check the results
        self.assertTrue(abs(gappy_data.mean - 4.339904801) < 0.00001)

    def test_infill_scalemonthly(self):
        '''
        Code tested:
            Timeseries.infill_scalemonthly(other)
        '''
        self.assertTrue(False)








class TestUtils(TestCase):
    def test_is_a_digit(self):
        '''
        Code tested:
            is_a_digit(char)
        '''
        self.assertTrue(pqh.is_a_digit('0'))
        self.assertTrue(pqh.is_a_digit('1'))
        self.assertTrue(pqh.is_a_digit('2'))
        self.assertTrue(pqh.is_a_digit('3'))
        self.assertTrue(pqh.is_a_digit('4'))
        self.assertTrue(pqh.is_a_digit('5'))
        self.assertTrue(pqh.is_a_digit('6'))
        self.assertTrue(pqh.is_a_digit('7'))
        self.assertTrue(pqh.is_a_digit('8'))
        self.assertTrue(pqh.is_a_digit('9'))
        self.assertTrue(not pqh.is_a_digit(' '))
        self.assertTrue(not pqh.is_a_digit('.'))
        self.assertTrue(not pqh.is_a_digit('-'))
        self.assertTrue(not pqh.is_a_digit('+'))
        self.assertTrue(not pqh.is_a_digit('a'))
        self.assertTrue(not pqh.is_a_digit('A'))

    def test_first_non_digit(self):
        '''
        Code tested:
            first_non_digit(char)
        '''
        #Check empty string input
        result_1 = pqh.first_non_digit("")
        self.assertTrue(result_1[0] == -1)
        self.assertTrue(result_1[1] == ' ')
        #Check string with all digits
        result_2 = pqh.first_non_digit("123")
        self.assertTrue(result_2[0] == -1)
        self.assertTrue(result_2[1] == ' ')
        #Check string starting with non-digit
        result_3 = pqh.first_non_digit("Hello world")
        self.assertTrue(result_3[0] == 0)
        self.assertTrue(result_3[1] == 'H')
        #Check string starting with non-digit (whitespace)
        result_4 = pqh.first_non_digit(" Hello world")
        self.assertTrue(result_4[0] == 0)
        self.assertTrue(result_4[1] == ' ')
        #Check string with digits followed by non-digits
        result_5 = pqh.first_non_digit("123World")
        self.assertTrue(result_5[0] == 3)
        self.assertTrue(result_5[1] == 'W')

    def test_parse_date(self):
        '''
        Code tested:
            parse_date(datestring)
        '''
        date1_string = r"04_02_2017"
        date1 = pqh.parse_date(date1_string)
        date2_string = r"2017\02\04"
        date2 = pqh.parse_date(date2_string)
        self.assertTrue(date1 == date2)
        self.assertTrue(date1.year == 2017)
        self.assertTrue(date1.month == 2)
        self.assertTrue(date1.day == 4)

    def test_parse_value(self):
        '''
        Code tested:
            parse_value(valuestring)
        '''
        self.assertTrue(pqh.parse_value("0.123") == pqh.parse_value("  0.123    "))
        self.assertTrue(pqh.parse_value("-0.123") == pqh.parse_value("  -0.123    "))
        self.assertTrue(math.isnan(pqh.parse_value("")))
        self.assertTrue(math.isnan(pqh.parse_value(" ")))
        self.assertTrue(math.isnan(pqh.parse_value("nan")))
        self.assertTrue(math.isnan(pqh.parse_value("NAN")))

    def test_is_data_row(self):
        '''
        Code tested:
            is_data_row(row)
        '''
        self.assertTrue(pqh.is_data_row("2017_01_01, 0.01"))
        self.assertTrue(not pqh.is_data_row("Lorem ipsum"))
        self.assertTrue(not pqh.is_data_row("Date, Value"))

    def test_count_missing(self):
        '''
        Code tested:
            count_missing(data)
        '''
        self.assertTrue(pqh.count_missing([]) == 0)
        self.assertTrue(pqh.count_missing([1, 2, 3]) == 0)
        self.assertTrue(pqh.count_missing([1, math.nan, 3]) == 1)
        self.assertTrue(pqh.count_missing([math.nan, math.nan, math.nan]) == 3)

    def test_period_length(self):
        '''
        Code tested:
            period_length(start_datetime, end_datetime, interval)
        '''
        dt1 = dt.datetime(2017, 1, 1)
        dt2 = dt.datetime(2017, 1, 3)
        self.assertTrue(pqh.period_length(dt1, dt1) == 0)
        self.assertTrue(pqh.period_length(dt1, dt2) == 2)
        self.assertTrue(pqh.period_length(dt2, dt1) == -2)
        one_hour = dt.timedelta(seconds=3600)
        self.assertTrue(pqh.period_length(dt2, dt1, one_hour) == -2 * 24)


class TestFileio(TestCase):
    def test_load_save_load(self):
        '''
        Code tested:
            load_csv
            save_csv
        '''
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        pqh.save_csv(ts1, r".\pyqhtools\tests\test_data\r040134_resaved.csv")
        ts2 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134_resaved.csv")
        comparison_results = ts1.compare(ts2)
        self.assertTrue(comparison_results[0] == True)

    def test_load_save_load(self):
        '''
        Code tested:
            read_csv
            write_csv
        '''
        ts1 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134.csv")
        pqh.save_csv(ts1, r".\pyqhtools\tests\test_data\r040134_resaved.csv")
        ts2 = pqh.load_csv(r".\pyqhtools\tests\test_data\r040134_resaved.csv")
        comparison_results = ts1.compare(ts2)
        self.assertTrue(comparison_results[0] == True)
