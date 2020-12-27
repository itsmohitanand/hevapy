from heva import read_ghcn, yearly_max
from heva.utils.gev import GEV
from heva.utils.gev_plot import GEVPlot

file_path = "heva/aux_files/sample_station/UK000056225.dly"

data = read_ghcn(file_path)

max_val = yearly_max(data)

x = max_val[:, 0].reshape(max_val.shape[0], 1)
max_arr = max_val[:, 1].reshape(max_val.shape[0], 1)
# In mm
max_arr = max_arr / 10.0

gev = GEV(max_arr, x)
gev.fit()

gev_plot = GEVPlot(max_arr, x, gev.dist)
gev_plot.diag_plot("readme_plots/s.png")
