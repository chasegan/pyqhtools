from .utils import *
import datetime as dt
import numpy as np

class Timeseries:
    def __init__(self):
        self.source = ""
        self.data = []
        self.start = dt.datetime.max
        self.interval = dt.timedelta(days=1)

    def __get_count(self):
        return len(self.data)

    def __get_end(self):
        return self.start + self.interval * (self.count - 1)

    def __get_min(self):
        return min(self.data)

    def __get_max(self):
        return max(self.data)

    def __get_mean(self):
        answer = np.nanmean(self.data)
        return answer

    def __get_missing(self):
        answer = count_missing(self.data)
        return answer

    def clone(self):
        answer = Timeseries()
        answer.source = self.source
        answer.data = self.data.copy()
        answer.start = self.start
        answer.interval = self.interval
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

    def scale(self, factor):
        for i in range(len(self.data)):
            self.data[i] = self.data[i] * factor

    def lookup_date(self, date):
        i = int((date - self.start) / self.interval)
        if (i >= 0 and i < self.count):
            return self.data[i]
        return self.MISSING_VALUE

    def lookup(self, year, month, day):
        date = dt.datetime(year, month, day)
        return self.lookup_date(date)

    MISSING_VALUE = float("nan")
    count = property(__get_count)
    length = property(__get_count)
    end = property(__get_end)
    min = property(__get_min)
    max = property(__get_max)
    mean = property(__get_mean)
    missing = property(__get_missing)
