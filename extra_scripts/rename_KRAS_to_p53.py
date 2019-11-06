import os

# 1. Rename KRAS to XXX
# 2. Rename p53 to YYY
# 3. Rename XXX to p53
# 4. Rename YYY to KRAS

# 1-2 and 3-4 must be done in separate step or duplicate filenames wont be changed.

def rename_files_in_directory(dir):

    cur_filenames = os.listdir(dir)
    intermediate_filenames = cur_filenames[:]
    final_filenames = cur_filenames[:]

    for iter in range(0,len(cur_filenames)):

        oldString = cur_filenames[iter]
        dummyString = oldString.replace('KRAS','XXX').replace('p53','YYY')

        intermediate_filenames[iter] = dummyString

    for iter2 in range(0,len(cur_filenames)):
        os.rename(dir + cur_filenames[iter2], dir + intermediate_filenames[iter2])

    for iter3 in range(0,len(cur_filenames)):

        oldString = intermediate_filenames[iter3]
        finalString = oldString.replace('YYY','KRAS').replace('XXX','p53')

        final_filenames[iter3] = finalString

    for iter4 in range(0,len(cur_filenames)):
        os.rename(dir + intermediate_filenames[iter4], dir + final_filenames[iter4])

#dirs = ['C:/Users/holtlab/Desktop/GREG2019 Backup Oct/GrantHussey_Experiments/20191010_grant_mito/deconvolve/',
#'C:/Users/holtlab/Desktop/GREG2019 Backup Oct/GrantHussey_Experiments/20191010_grant_mito/deconvolve/TiffFiles/',
#'C:/Users/holtlab/Desktop/GREG2019 Backup Oct/GrantHussey_Experiments/20191010_grant_mito/all_images/']

#for iter in range(0,len(dirs)):
#    rename_files_in_directory(dirs[iter])
