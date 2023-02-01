import rasterio
import numpy as np
import pandas as pd
import geopandas as gpd
from osgeo import gdal
from skimage.graph import route_through_array
from shapely.geometry import LineString, Point
import time
import multiprocessing as mp
from tqdm import tqdm
from itertools import repeat

#looking at 100m land raster costs
land = rasterio.open("/shared-projects/rev/projects/goMexico/data/raster/gom_land.tif")

#ports
PORTS = [
    ["Houston", 29.656921, -94.991210],
    # ["New Orleans", 29.961842, -89.668618],
    ["Beaumont", 29.632313, -93.886709],
    ["Corpus Christi", 27.7209, -97.09], # 20 miles away
    # ["Mobile", 30.519163, -88.083522],
    ["Lake Charles", 29.735931, -93.315428], # 25 miles away
    # ["Plaquemines", 29.699681, -89.271768],
    ["Texas City", 29.350886, -94.875401],
    ["Port Arthur", 29.6644, -93.87], # 10 miles away
    # ["Pascagoula", 30.306418, -88.555],
    ["Freeport", 28.925031, -95.29],
    ["Matagorda Port", 28.57, -95.929],
    ["Galveston", 29.320671, -94.837713],
    ["Port Fourchon", 29.05, -90.144],
    ["Brownsville", 26.081653915114643, -97.14947400782103],
    ["Terrebonne", 29.03, -90.641], # 20 miles away
    ["Iberia", 29.804709, -91.898562],
    # ["Gulfport", 30.237, -88.986],
    ["Morgan City", 29.378, -91.38], # 20 miles away
    ["Orange", 29.666, -93.696], # 20 miles away
]


#removed port tier
ports_df = pd.DataFrame(PORTS, columns = ['name', 'latitude', 'longitude'])


#creating geometry
port_geom = [Point(xy) for xy in zip(ports_df.longitude, ports_df.latitude)] 
ports_df = ports_df.drop(['longitude', 'latitude'], axis=1)
ports_df = gpd.GeoDataFrame(ports_df, crs="EPSG:4326", geometry=port_geom).to_crs(land.crs)

#project points, change to swh
proj_p = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/project_points.gpkg")
proj_p = proj_p.to_crs(land.crs)
proj_p['gid'] = proj_p.index

#from https://gis.stackexchange.com/questions/28583/gdal-perform-simple-least-cost-path-analysis

#converts raster to array
def raster2array(rasterfn):
    raster = gdal.Open(rasterfn)
    band = raster.GetRasterBand(1)
    array = band.ReadAsArray()
    return array  
    

#offsets coordinates to match array indices
def coord2pixelOffset(rasterfn,x,y):
    raster = gdal.Open(rasterfn)
    geotransform = raster.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3] 
    pixelWidth = geotransform[1] 
    pixelHeight = geotransform[5]
    xOffset = int((x - originX)/pixelWidth)
    yOffset = int((y - originY)/pixelHeight)
    return xOffset,yOffset


#this needs to be run for all the poi, and then the minimal length, cost needs to be returned
def createPath(CostSurfacefn,costSurfaceArray,startCoordID,port_name):   
    
    startCoord = proj_p[proj_p['gid'] == startCoordID].geometry
    stopCoord = ports_df[ports_df['name'] == port_name].geometry


    # coordinates to array index
    startCoordX = startCoord.x
    startCoordY = startCoord.y
    startIndexX,startIndexY = coord2pixelOffset(CostSurfacefn,startCoordX,startCoordY)
    
    stopCoordX = stopCoord.x
    stopCoordY = stopCoord.y
    stopIndexX,stopIndexY = coord2pixelOffset(CostSurfacefn,stopCoordX,stopCoordY)
    
    # create path, no diagonal moves
    indices, weight = route_through_array(costSurfaceArray, (startIndexY,startIndexX), (stopIndexY,stopIndexX),geometric=False,fully_connected=False)

    #this really should be using weight, but some coast points are on land and some are slightly off    
    len_km = (len(indices) * 100) / 1000 #km


    if port_name == "Terrebonne":
        len_km = len_km + 32
    if port_name == "Morgan City":
        len_km = len_km + 32 
    if port_name == "Orange":
        len_km = len_km + 32 
    if port_name == "Corpus Christi":
        len_km = len_km + 32 
    if port_name == "Lake Charles":
        len_km = len_km + 40
    if port_name == "Port Arthur":
        len_km = len_km + 16

    line = pd.DataFrame(columns={"len_km"}, data={len_km})
    line['gid'] = startCoordID
    line['port'] = port_name


    return line



# creates array from cost surface raster
costSurfaceArray = raster2array("/shared-projects/rev/projects/goMexico/data/raster/gom_land.tif")
CostSurfacefn = "/shared-projects/rev/projects/goMexico/data/raster/gom_land.tif"

overall_distance_table = pd.DataFrame()


#iterates through all starting points and finds LCP for each
for i in proj_p['gid']:

    ind_dist_table = pd.DataFrame()

    print(f"running for project point {i} out of {max(proj_p['gid'])}")

    start = time.perf_counter()

    with mp.Pool(mp.cpu_count()) as pool:
        for o in tqdm(pool.starmap(createPath, zip(repeat(CostSurfacefn), repeat(costSurfaceArray), repeat(i), ports_df['name'])), total=len(ports_df['name'])):
            ind_dist_table = ind_dist_table.append(o)
    ind_dist_table = ind_dist_table.reset_index(drop=True)
    overall_distance_table = overall_distance_table.append(ind_dist_table.loc[ind_dist_table['len_km'].idxmin()])
    
    end = time.perf_counter()

    print(f"done with project point {i} in {round(end-start, 3)} seconds; {100 * round(i/max(proj_p['gid']), 4)}% done")
    if i%100 == 0:
        print("saving every 100 points")
        overall_distance_table.reset_index(drop=True).to_csv(f"/shared-projects/rev/projects/goMexico/data/tables/port_distance_results/call_area_port_distance_{i+1}_done.csv", index=False)
        print("done saving")


#this is lines file, called paths.gpkg in deliverable, merged with the coast points in coast_point_costs.gpkg
overall_distance_table.reset_index(drop=True).to_csv("/shared-projects/rev/projects/goMexico/data/tables/port_distance_results/call_area_port_distance_final.csv", index=False)
