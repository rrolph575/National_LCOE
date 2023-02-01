""" 
Extract lat/lon/swh .

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#import xarray as xr
import os
from os.path import exists
#import cfgrib
#from cdo import *
#cdo = Cdo()
import geopandas as gpd
import h5py
 

## Specify filepaths
sitename = 'north_atlantic'
#datapath = '/projects/boemgom/data/ERA5/swh_combined_windwaves_swell/grib/'
datapath_ifiles = '/datasets/US_wave/v1.0.0/Atlantic/'
# example ifile:  Atlantic_wave_1979.h5
datapath_ofiles = '/shared-projects/rev/projects/National_LCOE/North_Atlantic/data/raster/swh/'



# Take annual average from hourly data
# this is commented because it was already done.
#for year in np.arange(1979,1981):
year = 1979

swh_data_ifile_h5 = datapath_ifiles + 'Atlantic_wave_' + str(year) + '.h5'

# read lat, lon, swh data from the h5 file.
# https://stackoverflow.com/questions/28170623/how-to-read-hdf5-files-in-python
f = h5py.File(swh_data_ifile_h5, 'r')
ds_swh = f['significant_wave_height'] # hdf5 dataset
	


# save that to a df wiht a year timestamp
# ...



# take the avg of all df so you have a shape (lat, lon, swh).
# ...



# take the lat , lon, climatology_swh values and add it as a column to the closest lat/lon in the point file (see 
# below for example)
# ...


''' # This is if you want to convert h5 to nc by calling bash and then use cdo to take year mean.  cdo cannot handle 
#.h5 files so that is why you have to convert to .nc first.
#argList = swh_data_ifile_h5 + ' ' + swh_data_ofile_nc
#os.system("nccopy " + argList) # since os.system here is bash, then this is ok (nccopy is bash cmd)
# https://stackoverflow.com/questions/28170623/how-to-read-hdf5-files-in-python

# Take the annual average swh
#cdo.yearmean(input=swh_data_ifile_grb,output=swh_data_ofile_grb).variables['significant_wave_height']'''
print(year)


# take the average swh across all available years
'''time_period_mean_swh_ifile = '/shared-projects/rev/projects/goMexico/data/mean_1992thru2021_swh.grib'

## Open dataset
ds = cfgrib.open_datasets(time_period_mean_swh_ifile)
ds_waves = ds[0]
ds_waves_data = ds_waves['swh'].values
ds_lats = ds[0].latitude.values
ds_lons = ds[0].longitude.values

points = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/project_points.gpkg").to_crs(3174) 


## fill in ERA5 significant wave height to the closest matching lat lon in points
points['swh'] = np.nan # set placeholder for swh 
'''


## you need to append swh to the correct row based on latitude and longitude from points 
# points[['latitude','longitude']]

# Find lat/lon that is contained in the ncfile which is closest to the input lat/lon
def geo_idx(dd, dd_array):
   """search for nearest decimal degree in an array of decimal degrees and return the index.
     np.argmin returns the indices of minium value along an axis.
     so subtract dd from all values in dd_array, take absolute value and find index of minium.
    """
   geo_idx = (np.abs(dd_array - dd)).argmin()
   return geo_idx


## commented below because already ran
'''for i in np.arange(0,points.latitude.shape[0]):
	print(i)
	idx_lat = geo_idx(points.latitude[i], ds_lats)
	idx_lon = geo_idx(points.longitude[i], ds_lons)
	swh_closest_to_points_array1 = ds_waves['swh'][idx_lat,idx_lon].data
	print('lat from points file: ' + str(points.latitude[i]) + ' lat from ERA5 waves: ' + str(ds_lats[idx_lat]))
	print('lon from points file: ' + str(points.longitude[i]) + ' lon from ERA5 waves: ' + str(ds_lons[idx_lon]))
	# append data to points
	points.loc[i, 'swh'] = swh_closest_to_points_array1
	
# save new points file that now includes swh
points.to_file('/shared-projects/rev/projects/goMexico/data/vector/project_points_with_swh.gpkg')

'''

