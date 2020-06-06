import cartopy.crs as ccrs
import matplotlib.pylab as plt
import numpy as np


class CartPlot(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.c1 = "firebrick"
        self.c2 = "rebeccapurple"
        self.c3 = "mediumpurple"
        self.c4 = "c"

    def plot_stations(self):
        x = self.x
        y = self.y

        fig = plt.figure()
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        ax.scatter(x, y, marker="o", color=self.c2, linewidth=1, alpha=1)
        ax.coastlines()
        # ax.stock_img()
        ax.set_global()
        ax.gridlines()
        plt.show()

    def p_color_mesh(self, lon_list, lat_list, val_list):

        dx = 1
        dy = -1

        _lat, _lon = np.mgrid[slice(90, -90 + dy, dy), slice(-180, 180 + dx, dx)]

        fig = plt.figure()
        ax = fig.add_subplot(projection=ccrs.PlateCarree())
        _z = np.NaN * np.ones_like(_lat)[:-1, :-1]

        for i in range(len(lon_list)):
            index_x = int((lon_list[i] + 180) / dx)
            index_y = int((lat_list[i] - 90) / dy)
            _z[index_y, index_x] = val_list[i]

        ax.coastlines()

        x = ax.pcolormesh(_lon, _lat, _z, cmap="Spectral")
        ax.set_title("Change in return level [mm/10]")
        plt.colorbar(x, fraction=0.023, pad=0.04)
        plt.show()
