import glob

import igraph as gr
import numpy as np
import pandas as pd


def remove_path(full_path):
    """
    Inputs
    full_path (string): a Unix-based path to a file (with extension)

    Outputs
    filename (string): just the filename (with extension) from the path
    """

    # full_path: a Unix-based path to the directory

    if full_path.find("/") == -1:
        pass

    if full_path.find("/") != -1:
        filename = full_path.split("/")[-1]

    return filename


def remove_extension(path_or_filename_with_extension):
    """""
    Inputs
    path_or_filename_with_extension: either a path or a filename that for a specific file, with extension.
    (e.g. /usr/dir/sample.mitograph or sample.mitograph)

    Ouputs
    filename_without_extension: just the filename without the extension (e.g. "sample")

    Notes
    This function will fail if more than one . is in the file, such as ".tar.gz"
    """ ""

    cur_filename_with_extension = remove_path(path_or_filename_with_extension)

    filename_without_extension = cur_filename_with_extension.split(".")[0]

    return filename_without_extension


def get_paths(data_dir, extension):
    """""
    Inputs
    data_dir (string): path to where your MitoGraph output data are
    extension (string): the extension to search for (e.g. ".gnet")


    Outputs
    path_list (list of strings): a list where each element is a string that contains the path (with extension)
    pointing to the files with that extension
    (e.g. path_list = [sample1.gnet, sample2.gnet])
    """ ""

    path_list = []

    search_criteria = "/*" + extension

    for ipath in glob.glob(data_dir + search_criteria):
        path_list.append(ipath)

    return path_list


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


def get_raw_dataframe(decomp_graph, name):
    # Inputs
    # decomp_graph:
    # filename:

    col = ["Filename", "Nodes", "Edges", "Length"]
    raw_dataframe = pd.DataFrame(columns=col)

    iter_graph = 0
    for iter_graph in range(len(decomp_graph)):
        every_graph = decomp_graph[iter_graph]

        cur_nodes = gr.Graph.vcount(every_graph)
        cur_edges = gr.Graph.ecount(every_graph)
        cur_length_mitochondria = sum(every_graph.es["length"])

        cur_graph_dict = {
            "Filename": name,
            "Nodes": [cur_nodes],
            "Edges": [cur_edges],
            "Length": [cur_length_mitochondria],
        }

        new_rows = pd.DataFrame.from_dict(cur_graph_dict)

        raw_dataframe = raw_dataframe.append(new_rows)

    return raw_dataframe


def create_igraph_from_pandas(df):
    list_of_dicts = []

    pair_list = df[["Source", "Target"]].values

    for irow in range(len(df)):
        cur_source = df["Source"][irow]
        cur_target = df["Target"][irow]
        cur_length = df["Length"][irow]

        cur_dict = {"source": cur_source, "target": cur_target, "length": cur_length}

        list_of_dicts.append(cur_dict)

    g = gr.Graph.DictList(edges=list_of_dicts, vertices=None)

    return g


def do_the_thing(df, filename):

    col = ["Filename", "Nodes", "Edges", "Length"]
    summary = pd.DataFrame(columns=col)

    cur_graph = create_igraph_from_pandas(df)
    cur_decomp_graph = gr.Graph.decompose(cur_graph)

    for each_graph in cur_decomp_graph:

        cur_raw_dataframe = get_raw_dataframe(
            decomp_graph=cur_decomp_graph, name=filename
        )
        summary = summary.append(cur_raw_dataframe)

    return summary


# Get the paths of the gnet files for processing
