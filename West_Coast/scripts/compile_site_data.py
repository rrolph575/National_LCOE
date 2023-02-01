import geopandas as gpd
import pandas as pd


#start with project points
pp = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/project_points.gpkg")

#now we need to add the significant wave height as a column called hs_average

#read in swh, add as column
hs_avg_1992_thru_2021 = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/project_points_with_swh.gpkg") 
pp['hs_average'] = hs_avg_1992_thru_2021['swh']

#read in export cable length and spur line cost
#Gabe to do, how to incorporate spurline into nrwal
tx_lcp = gpd.read_file("/shared-projects/rev/projects/goMexico/data/vector/project_points_tx.gpkg")


pp['dist_s_to_l'] =  tx_lcp['dist_s_to_l']
pp['spur_line_cost'] = tx_lcp['spur_line_cost']

#read in distances to port, dist_op_to_s = dist_p_to_s = dist_p_to_s_nolimit
lcp_ports = pd.read_csv("/shared-projects/rev/projects/goMexico/data/tables/port_distance_results/call_area_port_distance_final.csv")


pp['dist_p_to_s'] = lcp_ports['len_km']
pp['dist_op_to_s'] = pp['dist_p_to_s']
pp['dist_p_to_s_nolimit'] = pp['dist_p_to_s']

site_data = pp[['gid', 'latitude', 'longitude', 'country', 'state', 'county',
       'timezone', 'elevation', 'offshore', 'hs_average',
       'dist_s_to_l','dist_op_to_s', 'dist_p_to_s', 'dist_p_to_s_nolimit']]


site_data = site_data.rename(columns={'elevation':'depth'})


#for some points, distances to port are less than 1, making them at a minimum 1 km
site_data = site_data.assign(dist_op_to_s = [1 if d < 1 else d for d in site_data['dist_op_to_s']])
site_data = site_data.assign(dist_p_to_s = [1 if d < 1 else d for d in site_data['dist_p_to_s']])
site_data = site_data.assign(dist_p_to_s_nolimit = [1 if d < 1 else d for d in site_data['dist_p_to_s_nolimit']])


#array efficiency used to calculate losses--but patrick running FLORIS for all points
# so each point will have different value
#AEFF: setting as .9 for now, probably won't use
site_data['aeff'] = 0.9

site_data = site_data.assign(fixed_downtime = [0.175 if hs >= 1 else 0.1 for hs in site_data['hs_average']])
site_data = site_data.assign(floating_downtime = [0.175 if hs >= 1 else 0.1 for hs in site_data['hs_average']])

site_data = site_data.assign(config = ["fixed" if d <= 60 else "floating" for d in site_data['depth']])

site_data.to_csv("/shared-projects/rev/projects/goMexico/data/tables/site_data.csv", index=False)
