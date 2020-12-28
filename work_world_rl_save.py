from heva import ghcn_record, read_ghcn, yearly_max, GEV

station_dict = ghcn_record(req_length=50, till_year=2015)

data_path = "data/ghcnd_all/"
ext = ".dly"

strt_year = 1965
end_year = 2015
data_list = []

counter = 0

rl_dict = dict()

with open("data/rl_1965_2015.csv", "w+") as f:

    f.write("station_name,strt_yr,rl_strt_yr,end_yr,rl_end_yr,lat,lon\n")

    for key, val in station_dict.items():
        file_path = data_path + key + ext
        data = read_ghcn(file_path)
        max_val = yearly_max(data)

        num_years = max_val.shape[0]
        strt_index = None
        end_index = None
        if max_val != []:
            for i in range(num_years):
                if strt_year == max_val[i, 0]:
                    strt_index = i
                if end_year == max_val[i, 0]:
                    end_index = i
            if strt_index is not None and end_index is not None:
                short_max_val = max_val[strt_index:end_index, :]
                num_years = end_year - strt_year
                if short_max_val.shape[0] == num_years:
                    covariate = short_max_val[:, 0].reshape(num_years, 1)
                    max_arr = short_max_val[:, 1].reshape(num_years, 1) / 10.0
                    p = [0.02]
                    gev = GEV(max_arr=max_arr, covariate=covariate, nmu_cov=1)
                    try:
                        gev.fit()
                        rl = gev.return_level(p)
                        counter += 1
                        rl_dict[key] = [covariate[0], rl[0], covariate[-1], rl[-1]]
                        f.write(
                            key
                            + ","
                            + str(int(covariate[0, 0]))
                            + ","
                            + str(rl[0, 0])
                            + ","
                            + str(int(covariate[-1, 0]))
                            + ","
                            + str(rl[-1, 0])
                            + ","
                            + str(val[3])
                            + ","
                            + str(val[4])
                            + "\n"
                        )
                        print(f"Number of stations completed {counter}")
                    except RuntimeError:
                        print(f"NaN encountered")
        else:
            pass
