import glob

import igraph as gr
import numpy as np
import pandas as pd


def remove_path(full_path):
    # full_path: a Unix-based path to the directory

    if full_path.find("/") == -1:
        pass

    if full_path.find("/") != -1:
        filename = full_path.split("/")[-1]

    return filename


def get_filename(path_or_filename_with_extension):
    # Inputs
    # path_or_filename_with_extension: either a path or a filename that points to a specific file, with extension.
    # (e.g. /usr/dir/sample.mitogrpah)

    # Ouputs:
    # noExtension: just the filename without the extension (e.g. "sample")

    # This function will fail if more than one . is in the file, such as ".tar.gz"

    cur_filename_with_extension = remove_path(path_or_filename_with_extension)

    filename_without_extension = cur_filename_with_extension.split(".")[0]

    return filename_without_extension


def get_gnet_paths(data_dir):
    # Inputs
    # data_dir: Directory pointing to where MitoGraph outputs are

    # Outputs
    # gnet_path_list: a list containing all the paths to the gnet files

    # gnet_filename_list = []
    gnet_path_list = []

    for ipath in glob.glob(data_dir + "/*.gnet"):
        gnet_path_list.append(ipath)
        # gnet_filename_list.append(get_filename(ipath))

    return gnet_path_list


def get_gnet_dfs(data_dir):
    # Inputs
    # data_dir: Directory pointing to where MitoGraph outputs are

    # Outputs
    # gnet_dfs: dictionary as {filename_without_extension: individual_gnet_df}
    # Unused outpit is total_nodes, similar dictionary

    gnet_dfs = {}
    total_nodes = {}

    gnet_path_list = get_gnet_paths(data_dir)

    for ignet_paths in gnet_path_list:
        cur_filename = get_filename(ignet_paths)

        gnet_dfs[cur_filename] = pd.read_csv(ignet_paths, sep="\t").reset_index()

        total_nodes[cur_filename] = int(gnet_dfs[cur_filename].columns[2])

        gnet_dfs[cur_filename] = gnet_dfs[cur_filename].rename(
            columns={
                "level_0": "Source",
                "level_1": "Target",
                str(total_nodes[cur_filename]): "Length",
            }
        )

    return gnet_dfs


def get_edge_list_from_df(df):
    uncleaned_edges = df.values[:, [0, 1]]

    edge_list = []

    for iter_edges in uncleaned_edges:
        cur_element = [int(iter_edges[0]), int(iter_edges[1])]

        edge_list.append(cur_element)

    return edge_list


def create_igraph_from_edgelist(edge_list):
    n_vertices = max(max(edge_list))
    g = gr.Graph()
    g.add_vertices(n_vertices + 1)
    g.add_edges(edge_list)

    return g


def calc_logic_vector(df, col, value):
    query_vector = value * np.ones(len(test_df))
    logic = df[col] == query_vector

    return logic


def find_correct_rows(df, edge_list):
    logical_indices = []

    for cur_pair in edge_list:
        cur_source = int(cur_pair[0])
        cur_target = int(cur_pair[1])

        source_logical_vector = calc_logic_vector(df=df, col="Source", value=cur_source)

        target_logical_vector = calc_logic_vector(df=df, col="Target", value=cur_target)

        combined_vector = source_logical_vector & target_logical_vector
        logical_indices.append(combined_vector)

    base_logical_vector = np.zeros(len(df)) == np.ones(len(df))

    for logical_index in logical_indices:
        base_logical_vector = base_logical_vector | logical_index

    return base_logical_vector


def wrong_get_raw_dataframe(decomp_graph, df):

    col = ["Filename", "Nodes", "Edges", "Length"]
    raw_dataframe = pd.DataFrame(columns=col)

    for every_graph in decomp_graph:

        cur_decomp_edgelist = every_graph.get_edgelist()
        cur_logic = find_correct_rows(df=df, edge_list=cur_decomp_edgelist)
        cur_nodes = gr.Graph.vcount(every_graph)
        cur_edges = gr.Graph.ecount(every_graph)
        cur_length = sum(df.loc[cur_logic].Length.values)

        cur_graph_dict = {
            "Filename": cur_filename,
            "Nodes": cur_nodes,
            "Edges": cur_edges,
            "Length": cur_length,
        }

        new_rows = pd.DataFrame.from_dict([cur_graph_dict])

        raw_dataframe = raw_dataframe.append(new_rows)

    return raw_dataframe


def get_raw_dataframe(decomp_graph, name):
    # Inputs
    # decomp_graph:
    # filename:

    col = ["Filename","Nodes", "Edges", "Length"]
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


def find_where(logic):
    A = [i for i, x in enumerate(logic) if x]
    return A


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


def get_mitograph_paths(data_dir):
    # Inputs
    # data_dir: Directory pointing to where MitoGraph outputs are

    # Outputs
    # mitograph_path_list: a list containing all the paths to the gnet files

    mitograph_path_list = []

    for ipath in glob.glob(data_dir + "/*.mitograph"):
        mitograph_path_list.append(ipath)

    return mitograph_path_list


def get_mitograph_dfs(data_dir):
    # Inputs
    # data_dir: Directory pointing to where MitoGraph outputs are

    # Outputs
    # mitograph_dfs: dictionary as {filename_without_extension: individual_gnet_df}
    # Unused outpit is total_nodes, similar dictionary

    mitograph_dfs = {}

    mitograph_path_list = get_mitograph_paths(data_dir)

    for imitograph_path in mitograph_path_list:
        cur_filename = get_filename(imitograph_path)

        mitograph_dfs[cur_filename] = pd.read_csv(imitograph_path, sep="\t")

        mitograph_dfs[cur_filename] = mitograph_dfs[cur_filename].rename(
            columns={
                "Volume from voxels": "Vol_From_Voxels",
                "Average width (um)": "Ave_Width_um",
                "Std width (um)": "Std_Width_um",
                "Total length (um)": "Total_Length_um",
                "Volume from length (um3)": "Vol_From_Length",
                "Unnamed: 5": "remove_this",
            }
        )

        mitograph_dfs[cur_filename] = mitograph_dfs[cur_filename].drop(columns="remove_this")

    return mitograph_dfs


# Get the paths of the gnet files for processing


def test_gnet():
    data_dir = "/Users/granthussey/github/MitoScripts/MitoScripts/data"
    gnet_dfs = get_gnet_dfs(data_dir)
    gnet_filenames = list(gnet_dfs.keys())

    # THIS IS WHERE THE LOOP GOES!

    cur_filename = "KRAS_mdivi_2W_001_000"
    test_df = gnet_dfs[cur_filename]

    cur_graph = create_igraph_from_pandas(test_df)

    cur_decomp_graph = gr.Graph.decompose(cur_graph)

    A = get_raw_dataframe(decomp_graph=cur_decomp_graph, name=cur_filename)

    # and contin ue until you get da big A and that's the final thing

    return A


data_dir = "/Users/granthussey/github/MitoScripts/MitoScripts/data"

mitograph_dfs = get_mitograph_dfs(data_dir)
mitograph_filenames = list(mitograph_dfs.keys())
cur_filename = mitograph_filenames[1]
test_df = mitograph_dfs[cur_filename]


# What I need to do next
# create a loop to go over all of the files
# create the "raw_data" but also the "summary data" that includes .mitograph data and "raw" data
# output it all in the end in a summary-like thing!
# doot.

