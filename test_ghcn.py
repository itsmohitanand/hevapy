from heva import ghcn_record
import matplotlib.pylab as plt

sorted_dict_station = ghcn_record(req_len=75, till_year=1940)
print(len(sorted_dict_station))

# fig , ax = plt.subplots(1,1, figsize=(5,20))
# y = 1
# for key, value in sorted_dict_station:
#     ax.barh(y, width = value[0], left = value[1], color = "rebeccapurple")
#     y+=1
#     ax.axvline(1800, linestyle = '--', color = 'c')
#     ax.axvline(1850, linestyle = '--', color = 'c')
#     ax.axvline(1900, linestyle = '--', color = 'c')
#     ax.axvline(1950, linestyle = '--', color = 'c')
#     ax.axvline(2000, linestyle = '--', color = 'c')
# plt.tight_layout()
# plt.savefig('plots/test.png')
