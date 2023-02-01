#!/bin/bash

#SBATCH --account=boempac
#SBATCH --time=200:00:00
#SBATCH -o /shared-projects/rev/projects/goMexico/scripts/lcp_to_ports.o
#SBATCH -e /shared-projects/rev/projects/goMexico/scripts/lcp_to_ports.e
#SBATCH --job-name=lcp_to_ports
#SBATCH --nodes=1
#SBATCH --mem=200000

echo Running on: $HOSTNAME, Machine Type: $MACHTYPE
echo CPU: $(cat /proc/cpuinfo | grep "model name" -m 1 | cut -d:  -f2)
echo RAM: $(free -h | grep  "Mem:" | cut -c16-21)

source ~/.bashrc
echo "sourced bashrc"

source ~/.bashrc_conda
echo "sourced bashrc_conda"

conda activate /home/gzuckerm/anaconda3/envs/devruns/
echo "activated devruns"


python -u ./lcp_to_ports.py
