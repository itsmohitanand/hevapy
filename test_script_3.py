from heva import ghcn_record, read_ghcn, yearly_max, max_cont_years
import matplotlib.pylab as plt
from heva import GEVPlot, GEV
import numpy as np


# This is the test script. Station UK000056225 is included in the sample data.

# file_path = "/Users/mohitanand/DocL/github/hevapy/sample_download/UK000056225.dly"
# file_path = "/Users/mohitanand/DocL/github/hevapy/sample_download/ASN00023000.dly"
# file_path = "/Users/mohitanand/DocL/github/hevapy/sample_download/CA006158350.dly"
# file_path = "/Users/mohitanand/DocL/github/hevapy/sample_download/GM000004204.dly"
# file_path = "/Users/mohitanand/DocL/github/hevapy/sample_download/GM000010962.dly"
file_path = "/Users/mohitanand/DocL/github/hevapy/sample_download/NLE00100499.dly"
# file_path = "/Users/mohitanand/DocL/github/hevapy/sample_download/UK000056225.dly"
# file_path = "/Users/mohitanand/DocL/github/hevapy/sample_download/USC00361920.dly"

x = read_ghcn(file_path)
years, max_val = yearly_max(x)


## Converting the data type in the right format
covariate = np.array([years, [x ** 2 for x in years]]).transpose()


max_val = np.array(max_val).reshape(len(max_val), 1)
dist = GEV(max_arr=max_val, covariate=covariate, nmu_cov=1)

dist.fit()
## GEV

p = [0.02]
plot = GEVPlot(max_val, years, dist.dist)
plot.non_stationary_rl_plot(p)
