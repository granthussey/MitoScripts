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

# Make a directory for all of the data!
mkdir /gpfs/scratch/gh1431/Results/$BASEDIR

BATCHDIR=/gpfs/scratch/gh1431/Results/$BASEDIR/Batch
ORIGDIR=/gpfs/scratch/gh1431/Results/$BASEDIR/Orig
SEGDIR=/gpfs/scratch/gh1431/Results/$BASEDIR/Segmented

# Make results directories.

# Batch of .tiff files
mkdir $BATCHDIR
find $1 -type f -print0 | xargs -0 cp -t $BATCHDIR

# Original form of files in folders
mkdir $ORIGDIR
cp -r $1 $ORIGDIR

# Segmented batch folder
mkdir $SEGDIR

# Determine the number of folders to process
NUM_DIR=$(ls $1 -l | grep -v ^l | wc -l)
echo "You have " "$NUM_DIR" " number of directories."

# Get a list of directories to pass to program
DIRS=($1*/)

# Initialize the array job for MitoGraph based nDir to analyze
sbatch --array=0-$NUM_DIR ~/MitoScripts/Shell/run_mitograph.sh "${DIRS[@]}"

# Copy the results to a results directory for RStudio analysis
#mkdir /gpfs/scratch/gh1431/Results/Segmented_$BASEDIR
#find $1 -type f -print0 | xargs -0 cp -t /gpfs/scratch/gh1431/Results/Segmented_$BASEDIR
