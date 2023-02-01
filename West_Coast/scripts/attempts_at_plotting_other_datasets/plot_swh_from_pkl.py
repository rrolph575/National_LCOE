import geopandas as gpd
from revruns import rr
from rex import Resource
import pandas as pd



datapath = '/shared-projects/rev/projects/National_LCOE/West_Coast/data/raster/'
ifile = datapath + 'Pacific_swh.pkl'


data = Resource(ifile)











'''## from other script..

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
plt.show()'''

