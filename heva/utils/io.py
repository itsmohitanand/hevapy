import numpy as np
from typing import List, Tuple, Dict
from datetime import datetime, timedelta
import requests
import os


def read_ghcn(file_path: str, var: str = "PRCP") -> np.ndarray:
    """
    Read the data for a given station in GHCN format, provided the file path and the variable. The five core elements as variables are:
    PRCP = Precipitation (tenths of mm)
    SNOW = Snowfall (mm)
    SNWD = Snow depth (mm)
    TMAX = Maximum temperature (tenths of degrees C)
    TMIN = Minimum temperature (tenths of degrees C)


    Args:
        file_path (str) : The path of a particular GHCN file
        var (str) : Variable whose series is to be extracted

    Returns:
        np.ndarray : A numpy array of having shape (num_days, 2)
    """
    data = []
    date_time = []
    with open(file_path) as f:
        first_line = f.readline()
        strt_year = int(first_line[11:15])
        strt_month = int(first_line[15:17])
        strt_datetime = datetime(strt_year, strt_month, 1)
        for line in f:
            element = line[17:21]
            if element == var:
                year = int(line[11:15])
                month = int(line[15:17])
                num_days = _num_days_month(year, month)
                for k in range(num_days):
                    strt_ind = 21 + 8 * k
                    end_ind = 26 + 8 * k
                    value = float(line[strt_ind:end_ind])
                    data.append(value)
                    date_time.append(strt_datetime)
                    strt_datetime += timedelta(days=1)
            else:
                continue

        return np.stack([np.array(date_time), np.array(data)]).transpose()


def _num_days_month(year, month):
    """
    Calculates the numnber of days in  a given month
    Args:
        year (int) : Year
        month (int) : Month
    Returns
        int : Number of days in that month
    """
    nxt_year = year
    nxt_month = month
    if month == 12:
        nxt_year += 1
        nxt_month = 1
    else:
        nxt_month += 1
    strt_dt = datetime(year, month, 1)
    end_dt = datetime(nxt_year, nxt_month, 1)
    return (end_dt - strt_dt).days


def download_ghcn(station_id: List, filepath: str):
    """
    GHCN data is available through ncdc noaa site and can be downloaded at
    https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/

    Args:
        station_id (List) : A list of station id for which the data needs to be downloaded
        filepath (str) : The path where the data will be downloaded
    Returns:
        bool : True if sucessfully downloaded else False
    """

    url_root = "https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/all/"
    extension = ".dly"
    counter = 1
    num_files = len(station_id)
    for each in station_id:
        print(f"Downloading {each}.dly | File {counter} of {num_files}")
        url = url_root + each + extension
        with requests.get(url, allow_redirects=True) as r:
            r.raise_for_status()
            fpath = filepath + "/" + each + extension
            with open(fpath, "wb") as f:
                for chunk in r.iter_content(chunk_size=1):
                    f.write(chunk)
        counter += 1
    return True
