#!/bin/bash

# Convert .grib to .nc files

# using cdo (Climate data operator), developed at Max Planck Institute 
# for Meteorology

grb_filepath='/shared-projects/rev/projects/National_LCOE/West_Coast/data/ERA5/'

nc_filepath='/shared-projects/rev/projects/National_LCOE/West_Coast/data/ERA5/ncfiles/'


# gulf_of_mexico_2004.grib # example ifilename

#for year in {1992..1993}
#do
#	echo ${year}
#	grb_filename="${grb_filepath}gulf_of_mexico_100m_u_and_v_swh_${year}.grib"
#	nc_filename="${nc_filepath}gulf_of_mexico_100m_u_and_v_swh_${year}.nc"
#	cdo -f nc copy $grb_filename $nc_filename
#done


cdo -f nc copy "${grb_filepath}mean_swh_west_coast_2002thru2022.grib" "${nc_filepath}/mean_swh_west_coast_2002thru2022.nc"
