""" 

This script calculates wind speeds and directions from ERA5 (met convention) u and v wind components.

It also plots a wind rose of the results.  Place windrose.py also in the same folder where you are running this script.

A csv file of wave heights and calculated wind speeds is saved.

Becca Rolph rebecca.rolph@nrel.gov
18 May 2022

"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import xarray as xr
import os
from os.path import exists
from windrose import WindroseAxes
import cfgrib

FigDir = 'ERA5_plots/windroses/'
 
## Specify site/filename to create windrose from

sitename = 'UMaine'
lat = 43.46
lon = -69.45


## Specify ifile/ofile names
wind_data_ifile_grb = 'data/grbfiles/' + sitename + '.grib'
wind_data_ifile_nc = 'data/ncfiles/' + sitename + '.nc'


## Open dataset
ds = cfgrib.open_datasets(wind_data_ifile_grb)


## Create dataframe from dataset at specified lat/lon
# When variables have an inconsistent grid spacing (e.g. ERA5 waves and wind have different resolutions) then you need to manually create the dataset that can be converted to the ncfile.
# ds.to_netcdf(wind_data_ifile_nc) # use this if all variables have same grid resolution
if isinstance(ds, list):
    # Read in waves
    ds_waves = ds[0]
    ds_waves_data = ds_waves['swh'].values
    ds_winds = ds[1]

# Find lat/lon that is contained in the ncfile which is closest to the input lat/lon
def geo_idx(dd, dd_array):
   """search for nearest decimal degree in an array of decimal degrees and return the index.
     np.argmin returns the indices of minium value along an axis.
     so subtract dd from all values in dd_array, take absolute value and find index of minium.
    """
   geo_idx = (np.abs(dd_array - dd)).argmin()
   return geo_idx

lat_in_file = geo_idx(lat, ds_winds.latitude.values)
lon_in_file = geo_idx(lon, ds_winds.longitude.values)

# Extract wind speed and direction from ifile, using data closest to the input lat/lon 
u100 = ds_winds['u100'].isel(longitude=lon_in_file, latitude=lat_in_file)
v100 = ds_winds['v100'].isel(longitude=lon_in_file, latitude=lat_in_file)

wind_speed = np.sqrt(u100**2 + v100**2) # [m/s]

# Calculate wind direction
def wind_uv_to_dir(U,V):
    """Calculates the wind direction from the u and v component of wind.
    Takes into account the wind direction coordinates is different than the 
    trig unit circle coordinate. If the wind directin is 360 then returns zero
    (by %360)
    Inputs:
      U = west/east direction (wind from the west is positive, from the east is negative)
      V = south/noth direction (wind from the south is positive, from the north is negative)
    """
    WDIR= (270-np.rad2deg(np.arctan2(V,U)))%360
    return WDIR

wind_dir = wind_uv_to_dir(u100, v100)
wind_speed_bins = np.histogram(wind_speed, 5)[1]


## Plot windrose
fig = plt.figure()
ax1 = fig.add_subplot(111, projection='windrose')
ax1.bar(wind_dir, wind_speed, normed=True, opening=0.8, edgecolor='white', bins=wind_speed_bins)
#ax1.set_title(sitename)

ax1.legend(bbox_to_anchor=(1.2 , -0.1))
plt.tight_layout()
fig.savefig(os.path.join(FigDir + sitename + '_windrose.png'), bbox_inches='tight')
plt.show()


## Save data to csv
data = {'datetime': ds_winds.coords['time'].values,
        'windspeed': wind_speed.values,
        'waveheight': ds_waves_data, 
       }

df = pd.DataFrame(data=data)
#df.set_index('datetime').astype

df['datetime'] = df['datetime'].dt.strftime('%m/%d/%y %H:%M')
df.set_index('datetime')

## Write data to csv
# Specify outfile name
csv_file = 'data/csvfiles/' + sitename + '.csv'
df.to_csv(csv_file, index=False)

"""Example weather csv file should look like this:
    
datetime,windspeed,waveheight
10/21/09 23:00,5.075226,0.59
10/22/09 0:00,5.4384003,0.65
"""




