import numpy as np
from typing import Tuple, List
from math import comb
from scipy.special import gamma
from heva.utils.dist import _Distribution
from heva.utils.helper import _convert_np
import matplotlib.pylab as plt


class GEV(_Distribution):
    """
    GEV class inherits from a _Distribution class and implements methods like loc, scale, shape, cdf and pdf.
    """

    __slots__ = "mu", "mu_p", "sigma", "xi", "cov", "covariate", "unit", "time_scale"

    def __init__(
        self, mu_p, sigma_p, xi_p, cov, covariate=1, unit=None, time_scale=None
    ):
        """
        mu, sigma and xi parameters are used to initialise a GEV Distribution

        Args:
            mu (numpy.array) : Location parameter of the distribution
            sigma (numpy.array) : Scale parameter of the distribution
            xi (numpy.array) : Shape parameter of the distribution
            cov (numpy.array) : Covriance Matrix of the parameters
        """
        self.mu_p = mu_p
        self.mu = self._compute_parameter(mu_p, covariate)
        self.sigma = self._compute_parameter(sigma_p, covariate)
        self.xi = self._compute_parameter(xi_p, covariate)
        self.cov = cov
        self.covariate = covariate
        self.unit = unit
        self.time_scale = time_scale

    def loc(self):
        return self.mu

    def scale(self):
        return self.sigma

    def shape(self):
        return self.xi

    def cdf(self, x):

        x = _convert_np(x)
        s = np.divide(x - self.mu, self.sigma)

        if self.xi != 0:
            return np.exp(
                -np.power(1 + np.multiply(self.xi, s), np.divide(-1, self.xi))
            )
        else:
            return np.exp(-np.exp(-s))

    def pdf(self, x):

        x = _convert_np(x)
        s = np.divide(x - self.mu, self.sigma)

        if self.xi != 0:
            ## Equation broken down for clarity
            a = np.power(1 + np.multiply(self.xi, s), -1 * (np.divide(1, self.xi) + 1))
            pdf = np.divide(np.multiply(a, self.cdf(x)), self.sigma)
            return pdf
        else:
            return np.multiply(np.exp(-s), self.cdf(x))

    def return_level(self, p):
        """
        GEV Return level equation Coles pg 67 eq 3.10
        1/p return level
        """
        p = _convert_np(p)
        yp = -np.log(1 - p)
        if self.xi != 0:
            log_term = np.power(yp, -self.xi)
            return self.mu + self.sigma * (log_term - 1) / self.xi
        else:
            return self.mu + self.sigma * np.log(yp)

    def return_level_gradient(self, p):
        """
        Return level gradient is calculated keeping the parameters fixxed in time.
        Coles 2001, page no. 56

        Returns:
            np.ndarray : Gradient transpose is returned here.

        """
        p = _convert_np(p)
        num_p = p.shape[0]

        eps = 0
        xi = self.xi + eps
        sigma = self.sigma + eps

        yp = -np.log(1 - p)
        a1 = np.ones((num_p, 1))
        a2 = (1 - yp ** (-xi)) / xi
        a3 = sigma / xi * (a2 - yp ** -xi * np.log(yp))

        grad = np.hstack([a1, a2, a3])

        return grad

    def return_level_var(self, p):
        p = _convert_np(p)
        num_p = p.shape[0]
        grad_rl = self.return_level_gradient(p)
        var = np.zeros((num_p, 1))
        for i in range(num_p):
            _mul = np.matmul(grad_rl[i, :], self.cov)
            var[i, 0] = np.matmul(_mul, grad_rl[i, :].T)
        return var

    def set_unit(self, unit: str):
        """
        Unit of obbservation used to create plots
        """
        self.unit = unit

        return True

    def set_time_scale(self, time_scale: str):
        """
        Time scale at which maxmium is selected.

        """
        self.time_scale = time_scale
        return True

    def _compute_parameter(self, p_para, covariate):
        cov_order = len(p_para)
        if cov_order > 1:
            para = np.zeros((covariate.shape[0], 1))
            for i in range(covariate.shape[0]):
                para[i, 0] = p_para[0] + np.matmul(
                    p_para[1:cov_order], covariate[i, : cov_order - 1]
                )

        else:
            para = p_para
        return para


class GEVfit(object):

    __slots__ = (
        "max_arr",
        "covariate",
        "mu",
        "sigma",
        "xi",
        "mu_init",
        "sigma_init",
        "xi_init",
        "method",
        "max_it",
    )

    def __init__(
        self,
        max_arr,
        covariate=None,
        mu_c=0,
        sigma_c=0,
        xi_c=0,
        mu_init=None,
        sigma_init=None,
        xi_init=None,
        method="Nelder-Mead",
        max_it=10000,
    ):

        self.max_arr = max_arr
        self.covariate = covariate
