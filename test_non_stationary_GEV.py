from heva import GEV, GEVPlot

import numpy as np

x = np.array([1, 2, 3, 2, 4, 7, 2, 1, 8, 9, 2, 3, 4, 2, 4, 3, 10]).reshape(17, 1)
covariate = np.array(
    [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
).reshape(17, 1)

dist = GEV(x, covariate, nmu_cov=1)

dist.fit()


p = [0.02]
plot = GEVPlot(x, covariate, dist.dist)
plot.non_stationary_rl_plot(p)
