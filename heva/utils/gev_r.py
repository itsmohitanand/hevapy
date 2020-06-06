import rpy2.robjects as ro
import rpy2.robjects.packages as rp
import rpy2.robjects.numpy2ri
import numpy as np
from rpy2.robjects import FloatVector

rpy2.robjects.numpy2ri.activate()


def r_gev_param_estimate(x, covariates=None, mu_v=None, sig_v=None, xi_v=None):
    """
    The R ismev package is used extensively for parameter estimation.

    Args:
        x (np.array) :  Data to which GEV needs to be fitted. Shape of the numpy array needs to be consistent (num_data,1)
        covariates (np.array)  : A 2-D array of data on which the parameters depends. For Non-Stationary GEV estimate
        mu_v (int) : The nunmber of colums with which the parameter mu varying
        sig_v (int) : The number of columns with which the parameter sig is varying
        xi_v (int) : The number of columns with which the parameter xi is varying
    Returns:
        Dict : A dictionary of negative log likelihood (nll) and the parameters

    """
    # Bring ismev package in scope
    rp.importr("ismev")

    # Type Conversion
    max_val = p2r(x)

    covariates = p2r(covariates)

    mu_v = _None_to_Null(mu_v)
    sig_v = _None_to_Null(sig_v)
    xi_v = _None_to_Null(xi_v)

    # load the r function
    gev_fit = ro.r["gev.fit"]
    # call the GEV fit
    model = gev_fit(max_val, ydat=covariates, mul=mu_v, sigl=sig_v, shl=xi_v)

    nllh = model[4][0]
    mle = [each for each in model[6]]
    se = [each for each in model[8]]

    mu_shape = _param_shape(model[1][0])
    sigma_shape = _param_shape(model[1][1])
    xi_shape = _param_shape(model[1][2])

    mu = np.array(mle[0:mu_shape])
    sigma = np.array(mle[mu_shape : mu_shape + sigma_shape])
    xi = np.array(mle[mu_shape + sigma_shape : mu_shape + sigma_shape + xi_shape])
    mle = (mu, sigma, xi)

    cov = np.zeros((3, 3))

    row = 0
    for i in range(3):
        for j in range(3):
            cov[i, j] = model[7][3 * row + j]
        row += 1

    gev_dict = {"nllh": nllh, "mle": mle, "se": se, "cov": cov}

    return gev_dict, model


def _None_to_Null(value):
    if value is None:
        return ro.NULL
    return value


def _np_to_rmatrix(matrix):
    nr, nc = matrix.shape
    return ro.r.matrix(matrix, nrow=nr, ncol=nc)


def p2r(obj):
    if obj is None:
        return _None_to_Null(obj)
    else:
        return _np_to_rmatrix(obj)


def r_gev_diag(rmodel, fpath):
    """
    The function requires r object given from r_gev_parameter_estimate to generate diagonostic plots
    Args:
        rmodel (robject) : The fitted model given by gev.fit
        fpath (str) :  File path to save the image
    Returns:
        plots : 4 plots for stationary model and 2 plots for non-stationary model
    """
    rp.importr("ismev")
    gev_diag = ro.r["gev.diag"]
    png = ro.r["png"]
    png(fpath)
    gev_diag(rmodel)

    return 1


def _isRNull(robject):
    """
    IF an R object is null return True else False
    Args:
        robject (robject) : An R object
    Returns:
        bool : True if type is ro.NULL else False
    """
    if robject == ro.NULL:
        return True
    else:
        return False


def _param_shape(param):
    """
    Infers the parameter shape from model structure

    Args:
        param (Rmodel[1/2/3])
    Returns:
        int : The shape of the mu
    """
    if _isRNull(param):
        param_shape = 1
    else:
        param_shape = 1 + int(param[0])

    return param_shape
