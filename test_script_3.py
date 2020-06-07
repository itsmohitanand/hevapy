from heva import ghcn_record, read_ghcn, yearly_max, max_cont_years
import matplotlib.pylab as plt
from heva import GEVPlot, GEVfit
import numpy as np


# This is the test script. Station UK000056225 is included in the sample data.

file_path = "/Users/mohit/Documents/project_oxford/data/ghcnd_all/UK000056225.dly"

x = read_ghcn(file_path)
years, max_val = yearly_max(x)


## Converting the data type in the right format
covariate = np.array([years, [x ** 2 for x in years]]).transpose()


max_val = np.array(max_val).reshape(len(max_val), 1)
fit = GEVfit(max_arr=max_val, covariate=covariate, nmu_cov=0)

fit.fit()
## GEV
