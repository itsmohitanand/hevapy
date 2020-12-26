# from heva.utils.io import read_ghcn, download_ghcn
# from heva.utils.details import ghcn_record, ghcn_stn_info
# from heva.utils.cart_plot import CartPlot
# from heva.utils.preprocess import yearly_max
# from heva.utils.gev import GEV
# from heva.utils.gev_plot import GEVPlot

# # from heva.utils.cart_plot import

# import numpy as np

# station_list = ghcn_record(t_year=150)
# # station_list = ["ASN00023000", "CA006158350", "GM000004204", "GM000010962", "NLE00100499", "UK000056225" ]

# # download_ghcn(station_list, "sample_download")
# print(f"Total number of stations {len(station_list)}")

# lon_list = []
# lat_list = []
# delta_rl_list = []
# slope_list = []
# p = [0.02]
# root_path = "/Users/mohit/Documents/project_oxford/data/ghcnd_all/"
# info = ghcn_stn_info(station_list)

# for i in range(len(station_list)):

#     ### Data preperation
#     fpath = root_path + station_list[i] + ".dly"
#     data = read_ghcn(fpath)
#     years, max_val = yearly_max(data)
#     max_val = np.array(max_val).reshape(len(max_val), 1)
#     covariate = np.array([years]).transpose()
#     gev_estimate, rmodel = r_gev_param_estimate(max_val, covariates=covariate, mu_v=1)

#     mu, sigma, xi = gev_estimate["mle"]
#     cov = gev_estimate["cov"]

#     model = GEV(mu, sigma, xi, cov, covariate=covariate)
#     rl_list = model.return_level([p])
#     delta_rl = rl_list[-1] - rl_list[0]
#     slope = mu[1]
#     # plot = GEVPlot(max_val, years, model)
#     # save_path = "test_images/ns_rl_"+station_list[i]+".png"
#     # plot.non_stationary_rl_plot(p,save_path=save_path)

#     # lat is y value and lon is x values
#     lat, lon = info[i][0]

#     delta_rl_list.append(delta_rl[0])
#     slope_list.append(slope)
#     lat_list.append(lat)
#     lon_list.append(lon)

# cart_plot = CartPlot(lon_list, lat_list)
# # cart_plot.plot_stations()
# cart_plot.p_color_mesh(lon_list, lat_list, delta_rl_list)

# ## GEV
