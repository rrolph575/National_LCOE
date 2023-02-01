#!/bin/bash

# This script calls download_ERA5.py in a loop to download multiple 
# years of ERA5 data.

#SBATCH --account=boempac
#SBATCH --time=02:59:00
#SBATCH --job-name=download_ERA5
#SBATCH --nodes=1 # This should be number_cores/36 (36 cores on Eagle)
#SBATCH --ntasks-per-node=36
#SBATCH --mail-user rrolph@nrel.gov
#SBATCH --mail-type BEGIN,END,FAIL
#SBATCH --output=EagleLogs/%j.%n.download_ERA5.log

number_cores=36

# this needs to be activated before submitting this batch script.
#conda activate /shared-projects/rev/projects/goMexico/becca/myCDO

for year in {2022..2022}
do
	echo ${year}
	export year=$year
	python3 download_ERA5.py ${year}
done




