# hevapy

### The main functionality of the package is to :  

1. ##### Work with hydrological data
    - [X] GHCN data implemeted
    - [X] Do some preprocessing, to find record length, valid year, etc
2. ##### Do some extreme value analysis
    - [X] Stationary GEV estimation implemeted
    - [X] Non-stationary GEV estimation implemeted (Only changing mean)
    - [ ] Non-stationarit in variance and xi not implemented

3. ##### Generate good plots
    - [X] Plots for stationary GEV estimation 
    - [X] Plots for non-statinary GEV estimation (needs improvement)
    - [ ] World plots, still needs to be done


This is where the data can be downloaded
[GHCN](https://www1.ncdc.noaa.gov/pub/data/ghcn/daily/)

Some plots for fun.
![Stationary GEV Plot](readme_plots/s.png)

### Some Todo's in terms of the figure 

- [X]  Figure 1: Data completeness in every year
- [X]  Figure 2: Time-series plot, 20 year return level plot
- [ ]  Figure 3: Composite world map, 50yr return level in start and end year
- [ ]  Figure 4: Composite world map, magnitude of event for 50 year return level event in start year, evaluate the the new return level (end year) of the same event, A map for change in years for return levels

Figure 1 : 
A map to show the length of the record for valid years. A valid year is one where there is data for 90% (329) or more number of days  in a year. 
![Record Length for 6 custom station](readme_plots/record_length.png)

Figure 2 : 
Creating a composite is not a good idea. It can be done manually later

![Non-stationary GEV Plot](readme_plot/ns.png)