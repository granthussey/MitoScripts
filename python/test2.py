
import mitodata as mito

"""
def get_dfs(data_dir, extension, rename_columns):

    dfs = {}

    path_list = get_paths(data_dir, extension)

    for ipath in path_list:

        cur_filename = remove_extension(ipath)

        dfs[cur_filename] = pd.read_csv(ipath, sep="\t").reset_index()

        dfs[cur_filename] = dfs[cur_filename].rename(columns=rename_columns)

        if extension == ".gnet":
            total_nodes = dfs[cur_filename].columns[2]
            additional_rename_dict = {total_nodes: "Length"}
            dfs[cur_filename] = dfs[cur_filename].rename(columns=additional_rename_dict)

        if extension == ".mitograph":
            dfs[cur_filename] = dfs[cur_filename].drop(columns="remove_this")

    return dfs
"""

data_dir = "/Users/granthussey/github/MitoScripts/MitoScripts/data"
extension = ".gnet"
rename_columns = {"level_0": "Source", "level_1": "Target"}


# Get dfs

path_list = mito.get_paths(data_dir=data_dir, extension=ext)


# now make the path_list proper for mapping

input_list = set(map(lambda x: ))

filenames = set(map(mito.remove_extension, path_list))


dfs = map(lambda x: pd.read_csv(x, sep="\t"), path_list)

import pandas as pd

def gay(path):

    df = pd.read_csv(path, sep="\t")

    return df






