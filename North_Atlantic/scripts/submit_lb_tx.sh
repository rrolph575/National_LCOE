#!/bin/bash

#SBATCH --account=boempac
#SBATCH --time=24:00:00
#SBATCH -o /shared-projects/rev/projects/goMexico/scripts/lb_tx.o
#SBATCH -e /shared-projects/rev/projects/goMexico/scripts/lb_tx.e
#SBATCH --job-name=lb_tx
#SBATCH --nodes=1
#SBATCH --mail-user=gzuckerm@nrel.gov
#SBATCH --mem=70000

echo Running on: $HOSTNAME, Machine Type: $MACHTYPE
echo CPU: $(cat /proc/cpuinfo | grep "model name" -m 1 | cut -d:  -f2)
echo RAM: $(free -h | grep  "Mem:" | cut -c16-21)

source ~/.bashrc
echo "sourced bashrc"

source ~/.bashrc_conda
echo "sourced bashrc_conda"

conda activate /home/gzuckerm/anaconda3/envs/devruns/
echo "activated devruns"


python -u ./build_lb_tx_costs.py 
