from heva import ghcn_record, read_ghcn, yearly_max, max_cont_years
import matplotlib.pylab as plt
from heva import r_gev_param_estimate, r_gev_diag, GEV, GEVPlot
import numpy as np


# This is the test script. Station UK000056225 is included in the sample data.

file_path = "sample_download/GM000004204.dly"
# file_path = "sample_download/NLE00100499.dly"
# file_path = "sample_download/UK000056225.dly"

x = read_ghcn(file_path)


years, max_val = yearly_max(x)


## Converting the data type in the right format
covariate = np.array([years, [x ** 2 for x in years]]).transpose()

max_val = np.array(max_val).reshape(len(max_val), 1)

## GEV

gev_estimate, rmodel = r_gev_param_estimate(max_val, covariates=covariate, mu_v=1)

path_to_save = "test_images/non_stationary.png"
r_gev_diag(rmodel, path_to_save)


mu, sigma, xi = gev_estimate["mle"]
cov = gev_estimate["cov"]

model = GEV(mu, sigma, xi, cov, covariate=covariate)
# model.set_unit("Rainfall [(mm/10)/day]")
# model.set_time_scale("Annual Maximum")
plot = GEVPlot(max_val, model)
plot.non_stationary_rl_plot()
# # plot.return_level_plot()
# # plot.density_plot()
# # plot.probability_plot()
# # plot.quantile_plot()

# plot.diag_plot()
