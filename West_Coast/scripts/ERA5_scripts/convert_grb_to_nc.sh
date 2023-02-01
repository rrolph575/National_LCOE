#!/bin/bash

# Convert .grib to .nc files

# using cdo (Climate data operator), developed at Max Planck Institute 
# for Meteorology

grb_filepath='/shared-projects/rev/projects/goMexico/data/ERA5/'

nc_filepath='/shared-projects/rev/projects/goMexico/data/ERA5/netcdf/'


# gulf_of_mexico_2004.grib # example ifilename

for year in {1992..1993}
do
	echo ${year}
	grb_filename="${grb_filepath}gulf_of_mexico_100m_u_and_v_swh_${year}.grib"
	nc_filename="${nc_filepath}gulf_of_mexico_100m_u_and_v_swh_${year}.nc"
	cdo -f nc copy $grb_filename $nc_filename
done
