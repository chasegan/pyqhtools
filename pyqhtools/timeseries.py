from .utils import *
import datetime as dt
import numpy as np

class Timeseries:
    def __init__(self):
        self.source = ""
        self.data = []
        self.start = dt.datetime.max
        self.timestep = dt.timedelta(days=1)

    def __get_count(self):
        return len(self.data)

    def __get_end(self):
        return self.start + self.timestep * (self.count - 1)

    def __get_min(self):
        if (len(self.data) == 0):
            return self.MISSING_VALUE
        else:
            return min(self.data)

    def __get_max(self):
        if (len(self.data) == 0):
            return self.MISSING_VALUE
        else:
            return max(self.data)

    def __get_mean(self):
        if (len(self.data) == 0):
            return self.MISSING_VALUE
        else:
            return np.nanmean(self.data)

    def __get_std(self):
        if (len(self.data) == 0):
            return self.MISSING_VALUE
        else:
            return np.nanstd(self.data)

    def __get_missing(self):
        return count_missing(self.data)

    def __get_nonmissing(self):
        return self.length - self.missing

    def clone(self):
        answer = Timeseries()
        answer.source = self.source
        answer.data = self.data.copy()
        answer.start = self.start
        answer.timestep = self.timestep
        return answer

    def summary(self):
        print("Source: " + self.source)
        print("Start: " + str(self.start))
        print("End: " + str(self.end))
        print("Count: " + str(self.count))
        print("Missing: " + str(self.missing))
        print("Min: " + str(self.min))
        print("Max: " + str(self.max))
        print("Mean: " + str(self.mean))
        print("StdDev: " + str(self.std))

    def scale(self, factor):
        for i in range(len(self.data)):
            self.data[i] = self.data[i] * factor

    def scale_monthly(self, seasonal_factors=None):
        #Resample 12 factors from the provided seasonal_factors list
        monthly_factors = []
        n = len(seasonal_factors)
        if n==1 or n==2 or n==3 or n==4 or n==6 or n==12:
            for i in range(12):
                j = math.ceil(n*(i + 1.0)/12.0) - 1
                monthly_factors.append(seasonal_factors[j])
        else:
            raise Exception("seasonal_factors must have length 1, 2, 3, 4, 6, or 12.")
        dates = self.get_dates()
        for i in range(self.length):
            self.data[i] = self.data[i] * monthly_factors[dates[i].month - 1]
        return self

    def get_value(self, year, month, day, date=None):
        if (date == None):
            date = dt.datetime(year, month, day)
        i = int(period_length(self.start, date, self.timestep))
        if (i >= 0 and i < self.count):
            return self.data[i]
        return self.MISSING_VALUE

    def set_value(self, value, year, month, day, date=None):
        if (date == None):
            date = dt.datetime(year, month, day)
        i = int(period_length(self.start, date, self.timestep))
        if (i >= 0 and i < self.count):
            self.data[i] = value
        else:
            raise Exception("Specified date is outside the timeseries range.")

    def set_value_if_missing(self, value, year, month, day, date=None):
        if (date == None):
            date = dt.datetime(year, month, day)
        i = int(period_length(self.start, date, self.timestep))
        if (i >= 0 and i < self.count):
            if math.isnan(self.data[i]):
                self.data[i] = value
        else:
            raise Exception("Specified date is outside the timeseries range.")

    def get_copy_of_data(self):
        copy_of_data = self.data.copy()
        return copy_of_data

    def get_dates(self, start=None, end=None, timestep=None):
        if (start == None):
            start = self.start
        if (end == None):
            end = self.end
        if (timestep == None):
            timestep = self.timestep
        dates = []
        d = start
        while d <= end:
            dates.append(d)
            d = d + timestep
        return dates

    def get_start_end(self):
        return [self.start, self.end]

    def set_start_end(self, start_and_end):
        self.set_start(0, 0, 0, start_and_end[0])
        self.set_end(0, 0, 0, start_and_end[1])
        return self

    def set_start(self, year, month, day, date=None):
        if (date == None):
            date = dt.datetime(year, month, day)
        new_length = max(0, 1 + int(period_length(date, self.end, self.timestep)))
        append_to_start = max(0, new_length - self.length)
        self.data = [self.MISSING_VALUE] * append_to_start + self.data[:new_length]
        self.start = date
        return self

    def set_end(self, year, month, day, date=None):
        if (date == None):
            date = dt.datetime(year, month, day)
        new_length = max(0, 1 + int(period_length(self.start, date, self.timestep)))
        append_to_end = max(0, new_length - self.length)
        self.data = self.data[:new_length] + [self.MISSING_VALUE] * append_to_end
        return self

    def bias(self, other, epsilon=0.0):
        """
        Returns the bias on overlapping data.
        """
        count = 0
        stot = 0.0
        otot = 0.0
        for d in self.get_dates():
            s = self.get_value(0, 0, 0, date=d)
            o = other.get_value(0, 0, 0, date=d)
            if not math.isnan(s + o):
                count = count + 1
                stot = stot + s
                otot = otot + o
        if count == 0:
            return math.nan
        return stot / otot

    def compare_start(self, other):
        return (self.start == other.start)

    def compare_end(self, other):
        return (self.end == other.end)

    def compare_timestep(self, other):
        return (self.timestep == other.timestep)

    def compare_length(self, other):
        return (self.length == other.length)

    def compare_nonmissing(self, other, epsilon=0.0):
        """
        Returns true if all non-missing values are also non-missing in the
        other timeseries. Otherwise returns false.
        """
        for d in self.get_dates():
            s = self.get_value(0, 0, 0, date=d)
            o = other.get_value(0, 0, 0, date=d)
            if (abs(o - s) > epsilon): #nan's will be false
                return False
        return True

    def compare_missing(self, other):
        """
        Returns true if all missing values (explicitly marked missing) are
        also missing (explicitly marked missing) from the other series.
        Otherwise returns false.
        """
        if (self.start != other.start or self.timestep != other.timestep or self.length != other.length):
            return False
        for i in range(len(self.data)):
            if math.isnan(self.data[i]) ^ math.isnan(other.data[i]):
                return False
        return True

    def compare(self, other, epsilon=0.0):
        start_is_same = self.compare_start(other)
        end_is_same = self.compare_end(other)
        timestep_is_same = self.compare_timestep(other)
        length_is_same = self.compare_length(other)
        missing_is_same = self.compare_missing(other)
        nonmissing_is_same = self.compare_nonmissing(other, epsilon=epsilon)
        bias = self.bias(other)
        all_same = (start_is_same and end_is_same and
            timestep_is_same and length_is_same and
            missing_is_same and nonmissing_is_same)
        print("All same: " + str(all_same))
        print("Start date is same: " + str(start_is_same))
        print("End date is same: " + str(end_is_same))
        print("Timestep is same: " + str(timestep_is_same))
        print("Length is same: " + str(length_is_same))
        print("Missing are same: " + str(missing_is_same))
        print("Nonmissing are same: " + str(nonmissing_is_same))
        print("Bias: " + str(bias))
        return [all_same, start_is_same, end_is_same, timestep_is_same,
            length_is_same, missing_is_same, nonmissing_is_same]

    def infill_merge(self, other):
        if (self.timestep != other.timestep):
            raise Exception("Cannot infill due to differing timesteps.")
        new_start = min(self.start, other.start)
        new_end = max(self.end, other.end)
        self.set_start_end([new_start, new_end])
        for d in other.get_dates():
            s = self.get_value(0, 0, 0, date=d)
            if math.isnan(s):
                o = other.get_value(0, 0, 0, date=d)
                self.set_value(o, 0, 0, 0, date=d)
        return self

    def infill_scale(self, other, factor=None):
        if (self.timestep != other.timestep):
            raise Exception("Cannot infill due to differing timesteps.")
        if factor == None:
            factor = self.bias(other)
        other_clone = other.clone()
        other_clone.scale(factor)
        self.infill_merge(other_clone)
        return self

    def infill_scalemonthly(self, other, factors=None):
        if (self.timestep != other.timestep):
            raise Exception("Cannot infill due to differing timesteps.")
        if factors == None:
            factors = self.get_wt93_factors(other)
        other_clone = other.clone()
        other_clone.scale_monthly(factors)
        self.infill_merge(other_clone)
        return self

    def infill(self, other, method="MERGE"):
        method = method.upper()
        if (method=="MERGE" or method=="DIRECT"):
            self.infill_merge(other)
        elif (method=="SCALE" or method=="FACTOR"):
            self.infill_scale(other)
        elif (method=="SCALE_MONTHLY" or method=="WT93B"):
            self.infill_scalemonthly(other)
        else:
            raise Exception("Undefined infilling method: " + str(method))
        return self

    def get_wt93_factors(self, other):
        if (self.timestep != other.timestep or self.timestep != dt.timedelta(1)):
            raise Exception("WT93 only supports daily timesteps.")
        #Clone self and other and align their periods
        start = dt.datetime(max(self.start.year, other.start.year), 1, 1)
        end = dt.datetime(min(self.end.year, other.end.year) + 1, 1, 1)
        s = self.clone().set_start_end([start, end])
        o = other.clone().set_start_end([start, end])
        #Calculate totals over corresponding complete months
        d = s.get_dates()
        s_monthly_totals = [0] * 12
        o_monthly_totals = [0] * 12
        m = 12
        s_cum = 0; o_cum = 0
        for i in range(len(s.data)):
            if (m != d[i].month):
                #New month. Clear the previous totals
                if not math.isnan(s_cum + o_cum):
                    s_monthly_totals[m - 1] += s_cum
                    o_monthly_totals[m - 1] += o_cum
                s_cum = 0; o_cum = 0
                m = d[i].month
            s_cum += s.data[i]
            o_cum += o.data[i]
        #Calculate factors
        answer = [0] * 12
        for i in range(12):
            answer[i] = s_monthly_totals[i] / o_monthly_totals[i]
        return answer






    MISSING_VALUE = float("nan")
    count = property(__get_count)
    length = property(__get_count)
    end = property(__get_end)
    min = property(__get_min)
    max = property(__get_max)
    mean = property(__get_mean)
    std = property(__get_std)
    missing = property(__get_missing)
    nonmissing = property(__get_nonmissing)
