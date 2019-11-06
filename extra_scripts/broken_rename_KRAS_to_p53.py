import os


# 1. Rename KRAS to XXX
# 2. Rename p53 to YYY
# 3. Rename XXX to p53
# 4. Rename YYY to KRAS

def rename_files_in_directory(dir):

    cur_filenames = os.listdir(dir)
    new_filenames = cur_filenames[:]

    for iter in range(0,len(cur_filenames)):

        oldString = cur_filenames[iter]

        newString = oldString.replace('KRAS','XXX').replace('p53','YYY').replace('YYY','KRAS').replace('XXX','p53')

        new_filenames[iter] = newString


    for iter2 in range(0,len(cur_filenames)):
        os.rename(dir + cur_filenames[iter2], dir + new_filenames[iter2])

dir = '/Volumes/GREG2019/GrantHussey_Experiments/2019_10_09_correctMitoTracker_Comp/deconvolve/TiffFiles/'
rename_files_in_directory(dir)
