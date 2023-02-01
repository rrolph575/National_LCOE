import matplotlib.pyplot as plt
from netCDF4 import Dataset as netcdf_dataset
import numpy as np

from cartopy import config
import cartopy.crs as ccrs


# get the path of the file. It can be found in the repo data directory.
fname = '/shared-projects/rev/projects/goMexico/data/ERA5/netcdf/gulf_of_mexico_100m_u_and_v_swh_1992.nc'


# read file
dataset = netcdf_dataset(fname)
u100 = dataset.variables['var246'][0, :, :]
v100 = dataset.variables['var247'][0, :, :]
lats = dataset.variables['lat'][:]
lons = dataset.variables['lon'][:]



# calculate wind speed from u and v components
ws = np.sqrt(u100**2 + v100**2)



### plot wind speed
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
plt.contourf(lons, lats, ws, 60,
             transform=ccrs.PlateCarree())
ax.coastlines()
cbar = plt.colorbar()
cbar.ax.set_ylabel('100 m wind speed [m/s]')
plt.show()



#### plot swh (this is on a 0.5 grid while 0.25 grid is for wind)
# read file
dataset = netcdf_dataset(fname)
swh = dataset.variables['var229'][0, :, :]
lats = dataset.variables['lat_2'][:]
lons = dataset.variables['lon_2'][:]

# figure
fig = plt.figure(figsize=(8,6))
ax = fig.add_subplot(1,1,1, projection=ccrs.PlateCarree())
plt.contourf(lons, lats, swh, 60,
             transform=ccrs.PlateCarree())
ax.coastlines()
cbar = plt.colorbar()
cbar.ax.set_ylabel('Combined wind waves and swell [m]')
plt.show()
