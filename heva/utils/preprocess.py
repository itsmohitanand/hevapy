from typing import List, Tuple
import numpy as np


def yearly_max(data: np.ndarray) -> Tuple:
    """
    A valid year is one with atleast 330 days of data.

    Args:
        data (np.ndarray) : A numpy array of two columns, first with datetime and second with corresponding value

    Returns:
        Tuple : A tuple of two lists containing years and corresponding max_value
    """
    years = []
    values = []
    max_val = []

    for i in range(data.shape[0]):
        if _day_first(data[i, 0]):
            values = []
        values.append(data[i, 1])
        if _day_last(data[i, 0]):
            num_valid_data = _count_data(values)

            if num_valid_data > 330:
                years.append(data[i, 0].year)
                max_val.append(max(values))

            values = []
    return (years, max_val)


def _day_first(x):
    """
    Finds if the given day is the first day of the year or not
    Args:
        x (datetime.datetime)
    Returm:
        bool : True if first day of the year else false
    """
    return (x.month == 1) and (x.day == 1)


def _day_last(x):
    """
    Finds if the given day is the first day of the year or not
    Args:
        x (datetime.datetime)
    Returm:
        bool : True if first day of the year else false
    """
    return (x.month == 12) and (x.day == 31)


def _count_data(values: List, no_data_value: int = -9999) -> int:
    """
    No data value by default is given by -9999
    Args:
        values (np.ndarray) : A list of values, with no data given by -9999
    Returns:
        int : num of datapoints with valid data
    """
    return sum([1 for each in values if each != no_data_value])


def max_cont_years(years: List):

    cont_count = 1
    prev = 0
    max_count = 0
    for each in years:
        if each == prev + 1:
            cont_count += 1
        else:
            cont_count = 1
        prev = each

        max_count = max(cont_count, max_count)

    return max_count
