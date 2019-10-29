#!/bin/bash

#SBATCH --partition=cpu_short
#SBATCH --job-name=mitograph
#SBATCH --mem-per-cpu=4gb
#SBATCH --time=0-12:00:00
#SBATCH --tasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --output=mitograph_r_%j.log   # Standard output and error log
#SBATCH --array=0-238                 # Array range

module purge
module load vtk/7.1.1

echo "Directory:" $PWD

hostname; date

DIRS=($1*/)

echo "DIRS[Slum_Array_Task_ID" ${DIRS[$SLURM_ARRAY_TASK_ID]}
echo "Slurm_Array_Task_ID" $SLURM_ARRAY_TASK_ID

echo "Doot"


~/bin/MitoGraph -xy 0.0973499 -z 0.2 -scales 1.0 1.3 4 -adaptive 10 -path ${DIRS[$SLURM_ARRAY_TASK_ID]}

date
