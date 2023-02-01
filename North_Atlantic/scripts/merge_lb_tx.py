import geopandas as gpd
import rasterio


# cost_1GW = rasterio.open("/shared-projects/rev/projects/goMexico/data/raster/costs_clipped_wea.tif")

# #coast points
# points = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/wea_coast_points.gpkg")
# points = points.to_crs(cost_1GW.crs)
# points['startID'] = points.index

# #replace this with the updated route



# #routes
# routes = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/test_lcp.gpkg")

# points.merge(routes.drop("geometry", axis=1)).to_file("/shared-projects/rev/projects/goMexico/data/vector/wea_coast_costs.gpkg")


#above was just for wea, this is for all call area
cost_1GW = rasterio.open("/shared-projects/rev/projects/goMexico/data/raster/costs_1500MW_clipped_tight.tif")

#coast points
points = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/coast_points_update2.gpkg")
points = points.to_crs(cost_1GW.crs)
points['startID'] = points.index

#replace this with the updated route



#routes
routes = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/lb_tx_results/call_area_lcp_final.gpkg")

points.merge(routes.drop("geometry", axis=1)).to_file("/shared-projects/rev/projects/goMexico/data/vector/call_area_coast_costs.gpkg")
