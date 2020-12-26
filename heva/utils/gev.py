import numpy as np
from typing import Tuple, List
from heva.utils.dist import _Distribution
from heva.utils.helper import _convert_np
import scipy.optimize
import matplotlib.pylab as plt

# from numdifftools import Hessian
from scipy import linalg


class GEVDist(_Distribution):
    """
    GEV class inherits from a _Distribution class and implements methods like loc, scale, shape, cdf and pdf.
    """

    __slots__ = (
        "mu",
        "sigma",
        "xi",
        "cov",
        "mu_cov",
        "unit",
        "time_scale",
        "mu_p",
        "sigma_p",
        "xi_p",
    )

    def __init__(self, mu_p, sigma_p, xi_p, cov, mu_cov=1, unit=None, time_scale=None):
        """
        mu, sigma and xi parameters are used to initialise a GEV Distribution

        Args:
            mu (numpy.array) : Location parameter of the distribution
            sigma (numpy.array) : Scale parameter of the distribution
            xi (numpy.array) : Shape parameter of the distribution
            cov (numpy.array) : Covriance Matrix of the parameters
        """
        self.mu_p = mu_p
        self.mu = self._compute_parameter(mu_p, cov)
        self.sigma = self._compute_parameter(sigma_p, cov)
        self.xi = self._compute_parameter(xi_p, cov)
        self.cov = cov
        self.cov = cov
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


class GEV(object):

    __slots__ = (
        "max_arr",
        "covariate",
        "nmu_cov",
        "nsigma_cov",
        "nxi_cov",
        "mu_init",
        "sigma_init",
        "xi_init",
        "method",
        "max_it",
        "mu_p",
        "sigma_p",
        "xi_p",
        "dist",
    )

    def __init__(
        self,
        max_arr,
        covariate=None,
        nmu_cov=0,
        nsigma_cov=0,
        nxi_cov=0,
        mu_init=None,
        sigma_init=None,
        xi_init=None,
        method="Nelder-Mead",
        max_it=10000,
    ):

        self.max_arr = max_arr
        self.covariate = covariate
        self.nmu_cov = nmu_cov
        self.nsigma_cov = nsigma_cov
        self.nxi_cov = nxi_cov
        self.mu_init = mu_init
        self.sigma_init = sigma_init
        self.xi_init = xi_init
        self.method = method
        self.max_it = max_it

    def fit(self):
        parameter = self._generate_parameter()
        options = {"maxiter": 10000}
        minimized_nll = scipy.optimize.minimize(
            fun=self.nll, x0=parameter, method="nelder-mead", hess=True, options=options
        )
        print(minimized_nll.x)

        strt_mu = 0
        end_mu = strt_mu + 1 + self.nmu_cov
        strt_sig = end_mu
        end_sig = strt_sig + 1 + self.nsigma_cov
        strt_xi = end_sig
        end_xi = strt_xi + 1 + self.nxi_cov

        self.mu_p = minimized_nll.x[strt_mu:end_mu]
        self.sigma_p = minimized_nll.x[strt_sig:end_sig]
        self.xi_p = minimized_nll.x[strt_xi:end_xi]

        self.dist = GEVDist(
            self.mu_p, self.sigma_p, self.xi_p, self.covariate, self.nmu_cov
        )
        # hess = Hessian(self.nll, method="complex")

        # hess_matrix = hess(minimized_nll.x)
        # print(linalg.inv(hess_matrix))

    def nll(self, parameters):

        mu_ind = self._param_index("mu")
        sigma_ind = self._param_index("sigma")
        xi_ind = self._param_index("xi")

        mu_p = parameters[mu_ind]
        sigma_p = parameters[sigma_ind]
        xi_p = parameters[xi_ind]

        mu = self._compute_variable(mu_p)
        sigma = self._compute_variable(sigma_p)
        xi = self._compute_variable(xi_p)

        x = self.max_arr
        n = x.shape[0]

        ll_1 = -n * np.log(sigma)

        y = 1 + xi * (x - mu) / sigma

        ll_2 = -(1 + 1 / xi) * np.sum(np.log(y))

        ll_3 = -np.sum(np.power(y, -1.0 / xi))

        ll = ll_1 + ll_2 + ll_3
        return -ll

    def _generate_parameter(self):

        init_1 = np.sqrt(6 * np.var(self.max_arr)) / np.pi
        init_2 = np.mean(self.max_arr) - 0.57722 * init_1

        # We just initialise bias with init_1 and other values are
        param_mu = (1 + self.nmu_cov) * [0]
        param_mu[0] = init_1

        param_sigma = (1 + self.nsigma_cov) * [1]
        param_sigma[0] = init_2
        param_xi = [0.1]

        param = param_mu + param_sigma + param_xi

        return np.array(param)

    def _compute_variable(self, param):

        var = param
        n_cov = param.shape[0]
        t_step = self.covariate.shape[0]

        if n_cov > 1:

            param_mat = np.tile(param, (t_step, 1))
            bias = param_mat[:, 0].reshape(t_step, 1)
            weights = param_mat[:, 1:].reshape(t_step, n_cov - 1)

            var_mat = bias + weights * self.covariate[:, 0 : n_cov - 1]
            var = var_mat.reshape(t_step, 1)

        return var

    def _param_index(self, param_str):

        if param_str == "mu":
            strt_ind = 0
            end_ind = self.nmu_cov + 1
        elif param_str == "sigma":
            strt_ind = self.nmu_cov + 1
            end_ind = strt_ind + self.nsigma_cov + 1
        elif param_str == "xi":
            strt_ind = self.nmu_cov + self.nsigma_cov + 2
            end_ind = strt_ind + self.nxi_cov + 1
        index_list = [x for x in range(strt_ind, end_ind)]

        return index_list
