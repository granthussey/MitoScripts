#!/bin/bash

#SBATCH --partition=cpu_short
#SBATCH --job-name=ini_mito
#SBATCH --mem-per-cpu=4gb
#SBATCH --time=0-12:00:00
#SBATCH --tasks=1
#SBATCH --cpus-per-task=1
#SBATCH --nodes=1
#SBATCH --output=mitograph_ini_%j.log   # Standard output and error log

## Setup
# Place all images into scratch directory. Don't store data in data directory.

## Inputs
# Directory containing folders, one image each (e.g. "NoGaussCells")

## Outputs
# New folder in ~/Results containing the processed MitoGraph files for RStudio

# Remove packages and echo status
module purge
module load vtk/7.1.1
module load slurm/18.08.8

echo "Directory:" $PWD
hostname; date

# Get the name of the base directory for naming purposes
BASEDIR=$(basename "$1")
echo "BASEDIR: "$BASEDIR

# Make a directory in the results folder where all things will be saved.
mkdir /gpfs/scratch/gh1431/Results/$BASEDIR
mkdir /gpfs/scratch/gh1431/Results/$BASEDIR"_Batch"

# Copy data to the "results" folder
cp -r $1 /gpfs/scratch/gh1431/Results/$BASEDIR

# Make a new directory with "batch" images (i.e. not in folders)
find $1 -type f -print0 | xargs -0 cp -t $1/../$BASEDIR"_Batch"

# Determine the number of folders to process
NUM_DIR=$(ls $1 -l | grep -v ^l | wc -l)
echo "You have " "$NUM_DIR" " number of directories."

# Get a list of directories to pass to program
DIRS=(/gpfs/scratch/gh1431/Results/$BASEDIR/*/)

# Initialize the array job for MitoGraph based nDir to analyze
sbatch --array=1-$NUM_DIR ~/scripts/MitoGraph/run_mitograph.sh "${DIRS[@]}"

# Copy the results to a results directory for RStudio analysis
mkdir /gpfs/scratch/gh1431/Results/Segmented_$BASEDIR
find $1 -type f -print0 | xargs -0 cp -t /gpfs/scratch/gh1431/Results/Segmented_$BASEDIR
