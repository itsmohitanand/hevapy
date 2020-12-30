from typing import List, Tuple, Dict


def ghcn_stn_info(stn_id: str) -> Tuple:
    """
    Station details for the ghcn stations.
    Args:
        stn_name (str) : Name of the station

    Returns:
        Tuple : Tuple containg three elements (Cordinates(x,y), elevation, name)
    """
    file_path = "heva/aux_files/ghcnd-stations.txt"
    stn_info = []
    for id in stn_id:
        with open(file_path) as f:
            for line in f:
                if line[:11] == id:
                    x = float(line[12:20])
                    y = float(line[22:30])
                    elev = float(line[31:37])
                    stn_name = line[41:71]
        try:
            stn_info.append(((x, y), elev, stn_name))
        except ValueError:
            stn_info.append(((None, None), None, None))
            print(
                f"Station with id {stn_id} could not be found. Thus returning a Tuple of None"
            )
    return stn_info


def ghcn_key_map():
    """
    Generates the Dictionary of country and country keys.
    Args:

    Returns:
        Dict : A dictionary of country keys and country
    """
    file_path = "heva/aux_files/ghcnd-countries.txt"
    c_key_map = dict()
    with open(file_path) as f:
        for line in f:
            x = line.split(" ")
            c_key_map[x[0]] = x[1]
    return c_key_map


def ghcn_record(req_length: int = 75, till_year=2015, var: str = "PRCP") -> dict:
    """
    Provides the station name with the length of record greater than a threshold, given for a variable. The five core elements as variables are:
    PRCP = Precipitation (tenths of mm)
    SNOW = Snowfall (mm)
    ßSNWD = Snow depth (mm)
    TMAX = Maximum temperature (tenths of degrees C)
    TMIN = Minimum temperature (tenths of degrees C)

    Args:
        t_year (int) : Threshold number of years, or the record length
        var (str) : The string representing the variables

    Return
        set : Set of station having records greater than t_years for the given var

    A copy of the text file. Can be updated.
    https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd-inventory.txt

    """
    file_path = "heva/aux_files/ghcnd-inventory.txt"

    with open(file_path) as f:

        station_dict = dict()
        for line in f:
            lat = float(line[12:20])
            lon = float(line[21:30])
            end_year = int(line[41:45])
            start_year = int(line[36:40])
            record_length = end_year - start_year
            variable = line[31:35]
            if (
                (record_length > req_length)
                and (variable == var)
                and (end_year >= till_year)
            ):
                station_dict[line[0:11]] = [
                    record_length,
                    start_year,
                    end_year,
                    lat,
                    lon,
                ]

    return station_dict
