import os

import geopandas as gpd
import numpy as np
import pandas as pd
from rex import Resource

import sys
from revruns import rr

import rioxarray as rxr
from rasterstats import zonal_stats

os.chdir("/shared-projects/rev/projects/National_LCOE/North_Atlantic/data")

#clipped from conus offshore bath
BATHYMETRY = "raster/gom_bathymetry.tif"


res = Resource("/datasets/WIND/North_Atlantic/yearly/North_Atlantic_2020.h5") # Available from 2000 thru 2020.

#resource data
meta = res.meta
meta_geo = meta.rr.to_geo()
#utm zone 15N
meta_geo = meta_geo.to_crs(32615)

# add gid
meta_geo = meta_geo.reset_index()

#call area
call_area = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/GOM-CallAreaTo400m/GOM_CallAreaTo400m.shp").to_crs(32615)

#resource points within the call area
meta_geo = meta_geo.overlay(call_area, how='intersection')

#adding bathymetry
bath = rxr.open_rasterio(BATHYMETRY, masked=True).squeeze()


print("extracting depths from raster")
#temporarily reprojecting meta to match that of the raster layer
#takes 20 mins
zs = zonal_stats(meta_geo.to_crs("ESRI:102008"), bath.values,affine=bath.rio.transform(), 
    copy_properties=True, stats="mean", nodata=np.nan)

#depths are now positive
meta_geo['elevation'] = np.negative(np.array([d['mean'] for d in zs], dtype=float))

#depth must be greater than five meters
meta_geo = meta_geo[meta_geo['elevation'] > 5]

print("saving")

# save to file. This is the lat/lons for all the points that we will use. THis is what is used to match the 
# wave height grid, etc to project grid.
meta_geo.to_file("/shared-projects/rev/projects/goMexico/data/vector/project_points.gpkg")


meta_geo = meta_geo.assign(config = ["fixed" if d <= 60 else "floating" for d in meta_geo['elevation']])

# this is the input to SAM (rev generation). This shows which grid cells use floating or fixed. Then NRWAL 
# knows which cost equations to use.
meta_geo[['gid','config']].to_csv("/shared-projects/rev/projects/goMexico/data/tables/project_points.csv", index=False)
meta_geo.drop(["geometry", "offshore", "OBJECTID", "Shape_Leng", "Shape_Area" ], axis=1). \
    to_csv("/shared-projects/rev/projects/goMexico/data/tables/points_for_floris.csv", index=False)
print("done")
