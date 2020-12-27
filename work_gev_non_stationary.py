from heva import GEV, GEVPlot, read_ghcn, yearly_max

import numpy as np

file_path = "heva/aux_files/sample_station/NLE00100499.dly"
data = read_ghcn(file_path)
max_val = yearly_max(data)

x = max_val[:, 0].reshape(max_val.shape[0], 1)
max_arr = max_val[:, 1].reshape(max_val.shape[0], 1) / 10.0

dist = GEV(max_arr, x, nmu_cov=1)

dist.fit()

plot = GEVPlot(max_arr, x, dist.dist)
plot.non_stationary_plot("readme_plots/ns.png")
