from heva import read_ghcn, yearly_max
from heva import record_length_plot


data_path = "heva/aux_files/sample_station/"
station_list = [
    "ASN00023000",
    "CA006158350",
    "GM000004204",
    "GM000010962",
    "NLE00100499",
    "UK000056225",
]
ext = ".dly"

dict_max_val = dict()
for each_station in station_list:

    file_path = data_path + each_station + ext
    data_station = read_ghcn(file_path)
    max_val = yearly_max(data_station)
    dict_max_val[each_station] = max_val


record_length_plot(dict_max_val, "readme_plots/record_length.png")
