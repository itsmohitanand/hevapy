import numpy as np
import matplotlib.pylab as plt
from heva import CartPlot

file_dir = "data/rl_1965_2015.csv"

station_name_list = []
rl_list = []
with open(file_dir) as f:
    header = f.readline().split(",")
    for lines in f.readlines():
        station_name, strt_yr, rl_strt, end_yr, rl_end, lat, lon = lines.split(",")

        station_name_list.append(station_name)

        rl_val = [
            int(float(strt_yr)),
            float(rl_strt),
            int(float(end_yr)),
            float(rl_end),
            float(lat),
            float(lon),
        ]
        rl_list.append(rl_val)


rl_mat = np.array(rl_list)


del_rl = rl_mat[:, 3] - rl_mat[:, 1]

lat_list = list(rl_mat[:, 4])
lon_list = list(rl_mat[:, 5])

del_rl_list = list(del_rl)

plt.hist(del_rl_list, bins=100)
plt.savefig("readme_plots/hist_change_rl.png")


# stat = 'max'

# save_path_delrl = 'readme_plots/del_rl_'+stat+'.png'
# save_path_location = "readme_plots/loc.png"
# cart_plot = CartPlot()
# cart_plot.plot_stations(lat_list, lon_list, save_path_location)
# cart_plot.p_color_mesh(
#     lat_list, lon_list, del_rl_list, stat, save_path=save_path_delrl
# )
