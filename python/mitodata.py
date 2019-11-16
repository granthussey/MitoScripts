import glob

import igraph as gr
import numpy as np
import pandas as pd


def remove_path(full_path):
    """"
    Inputs
    full_path (string): a Unix-based path to a file (with extension)

    Outputs
    filename (string): just the filename (with extension) from the path
    """ ""

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
    search_criteria = ''.join([data_dir, "/*", extension])

    path_list = glob.glob(search_criteria)

    return path_list


def get_dfs(data_dir, extension, rename_columns):

    def change_third_column(df):

        total_nodes = df.columns[2]
        df = df.rename(columns={total_nodes: "Length"})

        return df


    path_list = get_paths(data_dir, extension)

    dfs = map(lambda x: pd.read_csv(x, sep="\t").reset_index(), path_list)
    dfs = map(lambda x: x.rename(columns=rename_columns), dfs)


    if extension == ".gnet":
        dfs = map(change_third_column, dfs)

    if extension == ".mitograph":
        dfs = map(lambda x: x.drop(columns="remove_this"))


    return list(dfs)


def get_raw_dataframe(decomp_graph, name):
    # Inputs
    # decomp_graph:
    # filename:

    def extract_raw_dataframe(single_decomp_graph, name):

        nodes = gr.Graph.vcount(single_decomp_graph)
        edges = gr.Graph.ecount(single_decomp_graph)
        sum_length_mitochondria = sum(single_decomp_graph.es["length"])

        cur_graph_dict = {
            "Filename": name,
            "Nodes": [nodes],
            "Edges": [edges],
            "Length": [sum_length_mitochondria],
        }

        single_mitochondria_dataframe = pd.DataFrame.from_dict(cur_graph_dict)

        return single_mitochondria_dataframe

    raw_dataframe = list(map(lambda x: extract_raw_dataframe(single_decomp_graph=x, name=name), decomp_graph))

    combined_raw_dataframe = pd.concat(raw_dataframe).reset_index().drop(columns="index")

    return raw_dataframe


def create_igraph_from_pandas(df):

    def create_map_of_dicts(row):

        # THIS NEEDS TO BE PASSED df.itertuples()

        cur_source = row.Source
        cur_target = row.Target
        cur_length = row.Length

        dict = {"source": cur_source, "target": cur_target, "length": cur_length}

        return dict

    map_of_dicts = map(create_map_of_dicts, df.itertuples())

    g = gr.Graph.DictList(edges=list(map_of_dicts), vertices=None)

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
