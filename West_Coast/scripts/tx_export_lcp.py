from rex import Resource
import rasterio
import json
import numpy as np
import pandas as pd
import geopandas as gpd
from osgeo import gdal
from skimage.graph import route_through_array
from shapely.geometry import LineString
import time
import multiprocessing as mp
from tqdm import tqdm
from itertools import repeat



#looking at 100m land raster costs
land = rasterio.open("/shared-projects/rev/projects/goMexico/data/raster/gom_land.tif")

#points on coastline
points = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/call_area_coast_costs.gpkg")
points = points.to_crs(land.crs)
#removing costs over half billion
points = points[points['cost']<=500_000_000].reset_index(drop=True)



#project points, change to swh
proj_p = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/project_points.gpkg")
proj_p = proj_p.to_crs(land.crs)
proj_p['gid'] = proj_p.index

#from https://gis.stackexchange.com/questions/28583/gdal-perform-simple-least-cost-path-analysis



#using the cost eq. from nrwal to generate approx costs to reduce the search area
#filtering so that approx cost is less than 500 million
def fixed_export(len):
    return(len * 1725970.33 + 202049737 + 5734285.184 * 2)

def floating_export(len):
    return((0.0000000003 * len ** 5 -
            0.0000004450 * len ** 4 +
            0.0002307800 * len ** 3 -
            0.0590666309 * len ** 2 +
            9.6855829573 * len + 83.12) * 1000000 + 5734285.184 * 2)


#function that finds the approximate cost using straight line distance
def get_approx_cost(pp_gid):

    print(f"running for project point {pp_gid} out of {max(proj_p['gid'])}")

    start = time.perf_counter()   

    pp = proj_p[proj_p['gid'] == pp_gid]
    temp_points = points
    temp_points['dist_to_pp'] = np.array([pp.distance(temp_points.geometry[i]) for i in range(0, len(temp_points))])
    temp_points = temp_points[temp_points['dist_to_pp']<=300000]

    approx_cost = np.array([])
    for j in temp_points.index:
        if pp.elevation[pp_gid] > 60:
            approx_cost = np.append(approx_cost, temp_points.cost[j] + floating_export(temp_points.len_km[j]))
        else:
            approx_cost = np.append(approx_cost, temp_points.cost[j] + fixed_export(temp_points.len_km[j]))

    temp_points['approx_cost'] = approx_cost
    #this is cheapest by straight line distance, maybe enough to stop here?
    pp['land_fall_id'] = temp_points.loc[temp_points['approx_cost'].idxmin()]['startID']
    pp['dist_s_to_l'] = temp_points.loc[temp_points['approx_cost'].idxmin()]['dist_to_pp'] / 1000
    pp['spur_line_cost'] = temp_points.loc[temp_points['approx_cost'].idxmin()]['cost']

    end = time.perf_counter()

    print(f"done with project point {pp_gid} in {round(end-start, 3)} seconds; {100 * round(pp_gid/max(proj_p['gid']), 4)}% done")

    return(pp)

new_pp = gpd.GeoDataFrame(crs = land.crs)

with mp.Pool(mp.cpu_count()) as pool:
    for o in tqdm(pool.imap(get_approx_cost, proj_p['gid']), total=len(proj_p['gid'])):
        new_pp = new_pp.append(o)
gpd.GeoDataFrame(new_pp, crs=land.crs).to_file("/shared-projects/rev/projects/goMexico/data/vector/project_points_tx.gpkg")
#Below code is for lcp version--better than straight line, but too expensive


# #converts raster to array
# def raster2array(rasterfn):
#     raster = gdal.Open(rasterfn)
#     band = raster.GetRasterBand(1)
#     array = band.ReadAsArray()
#     return array  
    

# #offsets coordinates to match array indices
# def coord2pixelOffset(rasterfn,x,y):
#     raster = gdal.Open(rasterfn)
#     geotransform = raster.GetGeoTransform()
#     originX = geotransform[0]
#     originY = geotransform[3] 
#     pixelWidth = geotransform[1] 
#     pixelHeight = geotransform[5]
#     xOffset = int((x - originX)/pixelWidth)
#     yOffset = int((y - originY)/pixelHeight)
#     return xOffset,yOffset


# #this needs to be run for all the poi, and then the minimal length, cost needs to be returned
# def createPath(CostSurfacefn,costSurfaceArray,startCoordID,stopCoordID):   
    
#     startCoord = proj_p[proj_p['gid'] == startCoordID].geometry
#     stopCoord = points[points['startID'] == stopCoordID].geometry


#     # coordinates to array index
#     startCoordX = startCoord.x
#     startCoordY = startCoord.y
#     startIndexX,startIndexY = coord2pixelOffset(CostSurfacefn,startCoordX,startCoordY)
    
#     stopCoordX = stopCoord.x
#     stopCoordY = stopCoord.y
#     stopIndexX,stopIndexY = coord2pixelOffset(CostSurfacefn,stopCoordX,stopCoordY)
    
#     # create path, no diagonal moves
#     indices, weight = route_through_array(costSurfaceArray, (startIndexY,startIndexX), (stopIndexY,stopIndexX),geometric=False,fully_connected=False)

#     #this really should be using weight, but some coast points are on land and some are slightly off    
#     len_km = (len(indices) * 100) / 1000 #km

#     #floating export cost
#     if proj_p[proj_p['gid'] == startCoordID].elevation[startCoordID] > 60:
#         cost = len_km * 1725970.33 + 202049737 + 5734285.184 * 2
#     #fixed export cost
#     else:
#         cost = (0.0000000003 * len_km ** 5 -
#                         0.0000004450 * len_km ** 4 +
#                         0.0002307800 * len_km ** 3 -
#                         0.0590666309 * len_km ** 2 +
#                         9.6855829573 * len_km + 83.12) * 1000000 + 5734285.184 * 2

#     line = pd.DataFrame(columns={"export_length"}, data={len_km})
#     line['export_cost'] = cost
#     line['startID'] = startCoordID
#     line['endID'] = stopCoordID

#     return line



# # creates array from cost surface raster
# costSurfaceArray = raster2array("/shared-projects/rev/projects/goMexico/data/raster/gom_land.tif")
# CostSurfacefn = "/shared-projects/rev/projects/goMexico/data/raster/gom_land.tif"


# #iterates through all starting points and finds LCP for each
# for i in proj_p['gid']:

#     ind_cost_table = pd.DataFrame()

#     print(f"running for project point {i} out of {max(proj_p['gid'])}")

#     start = time.perf_counter()

#     #only running for points within 300km (valid export cable range)
#     pp = proj_p[proj_p['gid'] == i]
#     temp_points = points
#     temp_points['dist_to_pp'] = np.array([pp.distance(temp_points.geometry[i]) for i in range(0, len(temp_points))])
#     temp_points = temp_points[temp_points['dist_to_pp']<=300000]

#     approx_cost = np.array([])
#     for j in temp_points.index:
#         if pp.elevation[i] > 60:
#             approx_cost = np.append(approx_cost, temp_points.cost[j] + floating_export(temp_points.len_km[j]))
#         else:
#             approx_cost = np.append(approx_cost, temp_points.cost[j] + fixed_export(temp_points.len_km[j]))


#     # # #this is cheapest by straight line distance, maybe enough to stop here?
#     # temp_points.loc[temp_points['approx_cost'].idxmin()]


#     #or potentially take the 20 lowest points
#     temp_points = temp_points.iloc[np.argpartition(approx_cost, 20)[:20]]
#     # temp_points = temp_points.reset_index(drop=True)

#     with mp.Pool(mp.cpu_count()) as pool:
#         for o in tqdm(pool.starmap(createPath, zip(repeat(CostSurfacefn), repeat(costSurfaceArray), repeat(i), temp_points['startID'])), total=len(temp_points['startID'])):
#             ind_cost_table = pd.concat([ind_cost_table, o])
#     ind_cost_table = ind_cost_table.reset_index(drop=True)
    
#     #change to add the above
#     overall_cost_table = pd.concat([overall_cost_table, ind_cost_table.loc[ind_cost_table['export_cost'].idxmin()]])
    
#     end = time.perf_counter()

#     print(f"done with project point {i} in {round(end-start, 3)} seconds; {100 * round(i/max(proj_p['gid']), 4)}% done")
#     if i%100 == 0:
#         print("saving every 100 points")
#         overall_cost_table.reset_index(drop=True).to_csv(f"/shared-projects/rev/projects/goMexico/data/tables/tx_export_results/call_area_tx_export_{i+1}_done.csv")
#         print("done saving")


# #this is lines file, called paths.gpkg in deliverable, merged with the coast points in coast_point_costs.gpkg
# overall_cost_table.reset_index(drop=True).to_csv("/shared-projects/rev/projects/goMexico/data/tables/tx_export_results/call_area_tx_export_final.csv")