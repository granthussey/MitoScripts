
import os


# 1. Rename KRAS to XXX
# 2. Rename p53 to YYY
# 3. Rename XXX to p53
# 4. Rename YYY to KRAS

dir = 'E:\GrantHussey_Experiments\2019_10_09_correctMitoTracker_Comp\deconvolve'

def rename_files_in_directory(dir):

    cur_names = os.listdir(dir)


    # First, we copy what the current names are.
    new_names = cur_names

    # Second, we edit that list with the new names, indexed in the same way.
    new_names =  new_names.replace('KRAS','XXX').replace('p53','YYY').replace('YYY','KRAS').replace('XXX','p53')


    for iter in len(cur_names):
        os.rename(cur_names[iter], new_names[iter])
