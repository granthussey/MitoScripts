#!/bin/bash
                                                                                                                                           #SBATCH --partition=cpu_short
#SBATCH --job-name=mitograph
#SBATCH --mem-per-cpu=4gb
#SBATCH --time=0-12:00:00
#SBATCH --tasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --output=mitograph_r_%j.log   # Standard output and error log

## Goal
# Copy folder-based images into a batch folder
# Dispatch

module purge
echo "Directory:" $PWD
hostname; date

DIRS=($1*/)
BASEDIR=$(basename "$1")

echo "BASEDIR: "$BASEDIR

#mkdir $1/../$BASEDIR"_Doot"
#find $1 -type f -print0 | xargs -0 cp -t $1/../$BASEDIR"_Doot"

NUM_DIR=$(ls $1 -l | grep -v ^l | wc -l)
