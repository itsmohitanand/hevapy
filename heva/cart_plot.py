import cartopy.crs as ccrs
import matplotlib.pylab as plt
import numpy as np


class CartPlot(object):
    def __init__(
        self,
    ):

        self.c1 = "firebrick"
        self.c2 = "rebeccapurple"
        self.c3 = "mediumpurple"
        self.c4 = "c"

    def plot_stations(self, lat_list, lon_list, save_path: str):
        x = lon_list
        y = lat_list

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.scatter(x, y, marker="o", s=0.5, color=self.c2, linewidth=1, alpha=0.6)
        ax.coastlines()
        # ax.stock_img()
        ax.set_global()
        ax.gridlines()
        plt.tight_layout()
        plt.savefig(save_path)

    def p_color_mesh(
        self, lat_list: list, lon_list: list, val_list: list, stat: str, save_path: str
    ):

        dx = 1
        dy = -1

        _lat, _lon = np.mgrid[slice(90, -90 + dy, dy), slice(-180, 180 + dx, dx)]

        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        _z = np.NaN * np.ones_like(_lat)[:-1, :-1]

        val_dict = dict()
        for i in range(len(lon_list)):
            index_x = int((lon_list[i] + 180) / dx)
            index_y = int((lat_list[i] - 90) / dy)

            key = str(index_x) + "_" + str(index_y)

            if key in val_dict:
                val_dict[key].append(val_list[i])
            else:
                val_dict[key] = [val_list[i]]

        for key, val in val_dict.items():
            index_x = int(key.split("_")[0])
            index_y = int(key.split("_")[1])

            if stat == "mean":
                _z[index_y, index_x] = sum(val) / len(val)
            elif stat == "min":
                _z[index_y, index_x] = min(val)
            elif stat == "max":
                _z[index_y, index_x] = max(val)

        ax.coastlines()

        x = ax.pcolormesh(_lon, _lat, _z, cmap="coolwarm", vmin=-10, vmax=10)
        ax.set_title("Change in return level [mm]")
        plt.colorbar(x, fraction=0.023, pad=0.04)
        ax.set_global()
        ax.gridlines()
        plt.savefig(save_path)
