import math


def is_a_digit(char):
    """
    Check if the provided character is a digit.
    Returns a boolean result.
    """
    if (char == '0' or char == '1'
        or char == '2' or char == '3'
        or char == '4' or char == '5'
        or char == '6' or char == '7'
        or char == '8' or char == '9'):
        return True
    else:
        return False


def first_non_digit(string):
    """
    Finds the first non-digit character in the provided string.
    Returns the location and the char.
    """
    for i in range(len(string)):
        if not is_a_digit(string[i]):
            return [i, string[i]]
    return [-1, ' ']


def parse_date(datestring):
    """
    Parses a date string into a datetime object.
    It expects no more than 2 digits for the day, and uses this
    to determine whether the format is dmy or ymd. The delimit
    character is automatically determined.
    Returns the datetime or None.
    """
    [delimit_loc, delimit_char] = first_non_digit(datestring)
    if (delimit_loc < 3):
        formatter = "%d" + delimit_char + "%m" + delimit_char + "%Y"
    else:
        formatter = "%Y" + delimit_char + "%m" + delimit_char + "%d"
    answer = dt.datetime.strptime(datestring, formatter)
    return answer


def parse_value(valuestring):
    """
    Parses a string to a float value. Whitespaces are parsed as nan.
    Returns a float.
    """
    s = valuestring.strip()
    if (s == ""):
        s = "nan"
    return float(s)


def is_data_row(row):
    """
    Guesses if a csvreader 'row' object contains data, i.e. not
    headder information. It does this by checking if the zeroth
    char of the zeroth element is a digit (which would be a date).
    Returns boolean result.
    """
    zeroth_element = row[0]
    if (len(zeroth_element) == 0):
        return False
    else:
        zeroth_char = zeroth_element[0]
        return is_a_digit(zeroth_char)


def count_missing(data):
    """
    Counts the number of nan in a list of float.
    Return an integer.
    """
    answer = 0
    for d in data:
        if math.isnan(d):
            answer = answer + 1
    return answer