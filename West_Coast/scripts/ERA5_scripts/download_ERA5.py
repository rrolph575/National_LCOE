# -*- coding: utf-8 -*-

""" This script downloads ERA5 data from a bounded lat/lon box. To get the required packages this script needs to run, see the Climate Data Store at 
https://cds.climate.copernicus.eu/api-how-to

Inputs:
- year (you can loop this py script by calling it in a bash script so that multiple years are saved into separate files). 
- month start & end
- lat lon bounds (upper left corner, lower right corner)
- site name

Becca Rolph rebecca.rolph@nrel.gov
18 May 2022
"""

import cdsapi
import numpy as np
import pandas as pd
from datetime import time
import os


# Specify sitename and variables
sitename = 'west_coast'
varnames='swh' # change the long varname in the c.retreive functions below, depending on how many there are.

# Specify path that the ERA5 data should be saved to
data_path = '/shared-projects/rev/projects/National_LCOE/West_Coast/data/ERA5/'
print('Data is being downloaded to ' + data_path)

# Specify months
month_start = 1
month_end = 12 # Inclusive

# Specify lat and lon bounds
north_lat = 49.76
west_lon = -131.17 # this should be from -180 to 180
south_lat = 32.35
east_lon = -116.75  # this should be from -180 (western) to 180

c = cdsapi.Client()

def download_ERA5(sitename, varnames, year, month_start, month_end, data_path, north_lat, west_lon, south_lat, east_lon):

	# Convert inputs into the format needed for cdsapi
	year_str = ['{0}'.format(year)]
	print(year_str)
	months = np.arange(month_start,month_end+1)
	months_str = ['{0}'.format(month).zfill(2) for month in months]
	print(months_str)
	days = np.arange(1,32)
	days_str = ['{0}'.format(day).zfill(2) for day in days]
	date_range = pd.date_range('00:00', '23:00', freq='h')
	hours_str = date_range.strftime("%H:%M:%S").to_list()
   	
	grb_out_filename = data_path + sitename + '_' + varnames + '_' + str(year) + '.grib'
    	
	# Call cdsapi
	c.retrieve(
		'reanalysis-era5-single-levels',
		{
		'product_type': 'reanalysis',
		'format': 'grib',
		'variable': [
		#'100m_u_component_of_wind',
		#'100m_v_component_of_wind',
		'significant_height_of_combined_wind_waves_and_swell',
		],
		'year': year_str,
		'month': months_str,
		'day': days_str,
		'time': hours_str,
		'area': [
		north_lat, west_lon, south_lat, east_lon],
		},
		grb_out_filename)

	return 'ERA5 data is now saved in ' + grb_out_filename

download_ERA5(sitename, varnames, os.environ["year"], month_start, month_end, data_path, north_lat, west_lon, south_lat, east_lon)
