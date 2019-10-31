#!/bin/bash

#SBATCH --partition=cpu_short
#SBATCH --job-name=run_mito
#SBATCH --mem-per-cpu=4gb
#SBATCH --time=0-12:00:00
#SBATCH --tasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --output=mitograph_run_%j_ARRAY_ID_"$SLURM_ARRAY_TASK_ID".log   # Standard output and error log

## Inputs
# $1 is the directory list

# Remove packages, load vtk, echo status
module purge
module load vtk/7.1.1
echo "Directory:" $PWD
hostname; date

DIRS=( "$@" )

# Get a list of directories for analysis

echo "Current data directory is: " ${DIRS[$SLURM_ARRAY_TASK_ID]}
echo "Current Slurm_Array_Task_ID: " $SLURM_ARRAY_TASK_ID

~/bin/MitoGraph -xy 0.0973499 -z 0.2 -scales 1.0 1.3 4 -adaptive 10 -path ${DIRS[$SLURM_ARRAY_TASK_ID]}

echo "Now moving all files to " ${DIRS[-1]}
cp -r ${DIRS[$SLURM_ARRAY_TASK_ID]} ${DIRS[-1]}

date
