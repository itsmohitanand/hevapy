import numpy as np
from hevapy.helper import _convert_2d_np
from typing import Tuple
import matplotlib.pylab as plt
from matplotlib.offsetbox import AnchoredText
from matplotlib.markers import MarkerStyle


class GEVPlot(object):
    __slots__ = "obs", "dist", "x", "c1", "c2", "c3", "c4"

    def __init__(self, obs, x, dist):
        self.obs = obs
        self.dist = dist
        self.x = x

        self.c1 = "firebrick"
        self.c2 = "rebeccapurple"
        self.c3 = "mediumpurple"
        self.c4 = "c"

    def _d_data(self):
        obs = self.obs
        GEV = self.dist
        x = [x for x in range(int(min(obs)), int(max(obs)))]
        y = GEV.pdf(x)
        bins = int(obs.shape[0] / 5)

        return x, y, bins

    def _d_ax(self, ax):
        GEV = self.dist
        obs = self.obs
        x, y, bins = self._d_data()

        ax.plot(x, y, color=self.c1, linewidth=1.5)
        ax.hist(obs, density=True, bins=bins, edgecolor=self.c2, color=self.c3)

        xlabel = "Z"
        ylabel = "pdf(Z)"

        if GEV.unit is not None and GEV.time_scale is not None:
            xlabel = xlabel + " : " + GEV.time_scale + " " + GEV.unit
        ax.set_title("Density Plot")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.axvline(GEV.mu, color=self.c4, linestyle="--")

        mu = str(np.round(GEV.mu, 2))
        sigma = str(np.round(GEV.sigma, 2))
        xi = str(np.round(GEV.xi, 3))

        if GEV.xi > 0:
            dist = "Frèchet (II)\n"
        elif GEV.xi < 0:
            dist = "Reversed Weibull (III)\n"
        else:
            dist = "Gumbel (I)\n"

        text = dist + "$\mu$ : " + mu + "\n$\sigma$ : " + sigma + "\n$\\xi$: " + xi
        anchored_text = AnchoredText(text, loc=1)
        ax.add_artist(anchored_text)
        return ax

    def _q_data(self):
        GEV = self.dist
        obs = self.obs
        obs = _convert_2d_np(obs)
        obs = np.sort(obs, axis=0)
        r = [1 - x / (obs.shape[0] + 1) for x in range(1, obs.shape[0] + 1)]
        sim = GEV.return_level(r)

        return sim, obs

    def _q_ax(self, ax):
        GEV = self.dist
        obs = self.obs

        sim, obs = self._q_data()

        ax.plot(sim, sim, color=self.c1)
        ax.scatter(sim, obs, alpha=0.6, color=self.c2)
        xlabel = "Model "
        ylabel = "Empirical "

        if GEV.time_scale is not None and GEV.unit is not None:
            xlabel += GEV.unit
            ylabel += GEV.unit

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        ax.set_title("Quantile Plot")

        return ax

    def _rl_data(self):
        GEV = self.dist
        obs = self.obs

        obs = _convert_2d_np(obs)
        obs = np.sort(obs, axis=0)

        t_emp = np.arange(1, obs.shape[0] + 1).reshape(obs.shape[0], 1)
        f_emp = [x / (t_emp.shape[0] + 1) for x in range(1, obs.shape[0] + 1)]

        # f_sup_fine = [x/1000 for x in range(5, 10, 1)]
        f_fine = [x / 100 for x in range(1, 10, 1)]
        f_med = [x / 10 for x in range(1, 10, 1)]
        f_coarse = [0.95, 0.99, 0.995, 0.999]
        # f = f_sup_fine + f_fine+f_med+f_coarse
        f = f_fine + f_med + f_coarse

        p = [1 - each for each in f]

        var = GEV.return_level_var(p)
        rl = GEV.return_level(p)
        rl_up = rl + 1.96 * np.sqrt(var)
        rl_lo = rl - 1.96 * np.sqrt(var)

        return f, f_emp, rl_lo, rl, rl_up, obs

    def _rl_ax(self, ax):
        GEV = self.dist
        obs = self.obs

        f, f_emp, rl_lo, rl, rl_up, obs = self._rl_data()

        ax.fill_between(
            -1 / np.log(f),
            rl_lo[:, 0],
            rl_up[:, 0],
            color=self.c1,
            alpha=0.3,
            label="95 % CI",
        )

        ax.plot(-1 / np.log(f), rl, color=self.c1, label="Mean return level")
        ax.scatter(
            -1 / np.log(f_emp), obs, alpha=0.6, color=self.c2, label="Observation"
        )
        ax.set_xscale("log")
        ax.legend(loc=2)
        ax.set_title("Return Level Plot")

        ylabel = "Return Level"
        xlabel = "Return Period"

        if GEV.time_scale is not None and GEV.unit is not None:
            ylabel += " (" + GEV.time_scale + ")"
            xlabel += " (" + GEV.unit + ")"

        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        return ax
        # ax.set_xlim(left= min(-1/np.log(f_emp)), right = max(-1/np.log(f_emp)))

    def _p_data(self):
        GEV = self.dist
        obs = self.obs

        obs = np.sort(obs, axis=0)
        emp_frequency = [x / len(obs) for x in range(len(obs))]
        model_frequency = GEV.cdf(obs)

        return model_frequency, emp_frequency

    def _p_ax(self, ax):

        model_frequency, emp_frequency = self._p_data()

        ax.scatter(emp_frequency, model_frequency, alpha=0.6, color=self.c2)
        ax.plot(model_frequency, model_frequency, color=self.c1)
        ax.set_title("Probability Plot")
        ax.set_xlabel("Empirical")
        ax.set_ylabel("Model")

        return ax

    def diag_plot(self, save_path: str):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 8))

        ax1 = self._p_ax(ax1)
        ax2 = self._q_ax(ax2)
        ax3 = self._rl_ax(ax3)
        ax4 = self._d_ax(ax4)

        fig.tight_layout()
        plt.savefig(save_path)

    def non_stationary_plot(self, save_path: str):
        fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=(12, 4))
        ax1 = self._ns_ts(ax1)
        ax2 = self._ns_density(ax2)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path)
            plt.close()
        else:
            plt.show()

    def _ns_ts(self, ax: type(plt.axes)) -> type(plt.axes):
        obs = self.obs
        GEV = self.dist
        x = self.x
        p = [0.05]
        mu_p = GEV.mu_p

        rl = GEV.return_level(p)

        del_rl = np.round(rl[-1] - rl[0], 2)[0]
        slope = np.round(mu_p[1], 3)
        # ax.plot(x, mu, color=self.c1)
        ax.plot(x, obs, marker="*", color=self.c2, label="observation")
        ax.plot(x, obs, color=self.c3)
        ax.plot(x, rl, color=self.c1, label="20 Yr Return Level")

        text = (
            "$\Delta$RL (p = "
            + str(p[0])
            + ") : "
            + str(del_rl)
            + "\n $\Delta$$\mu$/$\Delta$t : "
            + str(slope)
        )
        anchored_text = AnchoredText(text, loc=1)
        ax.add_artist(anchored_text)
        ax.legend()

        xlabel = "Covariate"
        ylabel = "Max Val"

        if GEV.unit is not None and GEV.time_scale is not None:
            xlabel = xlabel + " : " + GEV.time_scale + " " + GEV.unit
        ax.set_title("Time Series")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        return ax

    def _ns_density_data(self) -> Tuple:

        obs = self.obs
        GEV = self.dist
        x = [x for x in range(int(min(obs)), int(max(obs)))]
        y1 = GEV.pdf(x, mu=GEV.mu[0])
        y2 = GEV.pdf(x, mu=GEV.mu[-1])

        t1 = self.x[0]
        t2 = self.x[-1]

        return (x, (t1, y1), (t2, y2))

    def _ns_density(self, ax: type(plt.axes)) -> type(plt.axes):

        GEV = self.dist

        (x, (t1, y1), (t2, y2)) = self._ns_density_data()

        ax.plot(x, y1)
        ax.fill_between(
            x, 0, y1[:, 0], color=self.c3, alpha=0.8, label="year : " + str(int(t1[0]))
        )
        ax.plot(x, y2)
        ax.fill_between(
            x, 0, y2[:, 0], color=self.c1, alpha=0.5, label="year : " + str(int(t2[0]))
        )
        ax.legend()
        xlabel = "Z"
        ylabel = "pdf(Z)"

        if GEV.unit is not None and GEV.time_scale is not None:
            xlabel = xlabel + " : " + GEV.time_scale + " " + GEV.unit
        ax.set_title("Density Plot")
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)

        return ax
