

import time
import glob

import mitodata



data_dir = "/Users/granthussey/github/MitoScripts/MitoScripts/data"
ext = ".mitograph"


# Test 1

start = time.time()

search_criteria = ''.join([data_dir,"/*", ext])
path_list1 = glob.glob(search_criteria)

end = time.time()



# Test 2

start2 = time.time()

path_list2 = []

search_criteria = "/*" + ext

for ipath in glob.glob(data_dir + search_criteria):
    path_list2.append(ipath)



end2 = time.time()


print("Elapsed (after edit) = %s" % (end2 - start2))
print("Elapsed (before edit) = %s" % (end - start))

