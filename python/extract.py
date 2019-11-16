import glob

import igraph as gr
import numpy as np
import pandas as pd

import mitodata as doot
import time


from numba import jit, prange
from numba.types import List


rename_gnet_columns = {"level_0": "Source", "level_1": "Target"}


rename_mitograph_columns = {
    "Volume from voxels": "Vol_From_Voxels",
    "Average width (um)": "Ave_Width_um",
    "Std width (um)": "Std_Width_um",
    "Total length (um)": "Total_Length_um",
    "Volume from length (um3)": "Vol_From_Length",
    "Unnamed: 5": "remove_this",
}


data_dir = "/Users/granthussey/github/MitoScripts/MitoScripts/data"
gnet_dfs = get_dfs(
    data_dir=data_dir, extension=".gnet", rename_columns=rename_gnet_columns
)


def generate_summaries(dfs):

    summaries = []

    for each_key in dfs:

        cur_summary = doot.do_the_thing(df=dfs[each_key], filename=each_key)

        summaries.append(cur_summary)

    return summaries


start = time.time()
doot = generate_summaries(gnet_dfs)
end = time.time()
print("Elapsed (after compilation) = %s" % (end - start))


"""

data_dir = "/Users/granthussey/github/MitoScripts/MitoScripts/data"

mitograph_dfs = mito.get_mitograph_dfs(data_dir)
mitograph_filenames = list(mitograph_dfs.keys())
cur_filename = mitograph_filenames[1]
test_df = mitograph_dfs[cur_filename]

"""
