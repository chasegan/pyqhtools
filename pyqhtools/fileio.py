from .timeseries import *
import csv
import datetime


def read_csv(filename):
    """
    Load the specified csv file.
    Returns a Timeseries object.
    """
    answer = Timeseries()
    answer.source = filename.strip()
    with open(filename) as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        missing_value = float('nan')
        for row in csvreader:
            if is_data_row(row):
                value = parse_value(row[1])
                answer.data.append(value)
                if answer.count == 1:
                    date = parse_date(row[0])
                    answer.start = date
    return answer


def write_csv(timeseries, filename):
    """
    Save the given timeseries to csv file.
    """
    file = open(filename, "w")
    file.write("Date, Value\n")
    t = timeseries.start
    for v in timeseries.data:
        datestring = t.strftime('%Y-%m-%d')
        valuestring = ""
        if not math.isnan(v):
            valuestring = str(v)
        file.write(datestring + ", " + valuestring + "\n")
        t = t + timeseries.timestep
    file.close()


def load_csv(filename):
    """
    Same as read_csv
    """
    answer = read_csv(filename)
    return answer


def save_csv(timeseries, filename):
    """
    Same as write_csv
    """
    write_csv(timeseries, filename)
