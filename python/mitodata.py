import glob

import igraph as gr
import numpy as np
import pandas as pd


def remove_enclosing_dirs(full_path):
    """
    Inputs
    full_path (string): a Unix-based path to a file (with extension)

    Outputs
    filename (string): just the filename (with extension) from the path

    Notes
    If you pass a filename to this function, meaning it doesn't
    contain the "/" string, it will simply return the input back to you.
    """

    # full_path.find("/") will return the number of "/" in the string
    # if none exist, it will return -1.

    if full_path.find("/") != -1:
        filename = full_path.split("/")[-1]
        return filename

    elif full_path.find("/") == -1:
        filename = full_path
        print(" ".join(["Your path", full_path, "is already a filename."]))
        return filename

    else:
        print("Something went wrong. Your path isn't a path or a filename.")


def remove_extension(string):
    """
    Inputs
    string (string): either a path or a filename that for a specific file, with extension.
    (e.g. /usr/dir/sample.mitograph or sample.mitograph)

    Ouputs
    filename_without_extension: just the filename without the extension (e.g. "sample")

    Notes
    This function may fail if more than one . is in the file, such as ".tar.gz"
    """

    # Remove all enclosing directories, only get the name of file.
    cur_filename_with_extension = remove_enclosing_dirs(string)

    # Remove the extension by splitting the string at each "." and only taking first part.
    filename_without_extension = cur_filename_with_extension.split(".")[0]

    return filename_without_extension


def find_all_filetype(data_dir, extension):
    """
    Inputs
    data_dir (string): path to where your MitoGraph output data are
    extension (string): the extension to search for (e.g. ".gnet", ".mitograph")

    Outputs
    path_list (list of strings): a list where each element is a string containing the path for desired files (with extension)
    (e.g. path_list = [sample1.gnet, sample2.gnet])
    """

    # create a string to search for, include a wildcard * in place of the name of the file
    search_criteria = "".join([data_dir, "/*", extension])

    # use glob.glob to do the searching and retreive your list!
    path_list = glob.glob(search_criteria)

    return path_list


def create_edgelist_df(path):

    df = pd.read_csv(path, sep="\t").reset_index()
    df = df.rename(columns={"level_0": "Source", "level_1": "Target"})
    df = df.rename(
        columns={df.columns[2]: "Length"}
    )  # edits the third column, which is always the total # of nodes (per MitoGraph coding)

    return df


def create_automated_mitograph_df(path):

    name = remove_extension(path)
    df = pd.read_csv(path, sep="\t").reset_index()
    df = df.rename(
        columns={
            "Volume from voxels": "Vol_From_Voxels",
            "Average width (um)": "Ave_Width_um",
            "Std width (um)": "Std_Width_um",
            "Total length (um)": "Total_Length_um",
            "Volume from length (um3)": "Vol_From_Length",
            "Unnamed: 5": "remove_this",
        }
    )

    df = df.drop(columns=["remove_this", "index"])

    df["name"] = name
    df = df.set_index("name")

    return df


def initialize_network(path):
    """
    Creates a graph theory network for all of the mitochondria in each image.
    
    Inputs
    path (string): path to a single gnet file, which contains connectivity data.
    One of these exist per image.
    
    Outputs [tuple]
    0: overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
    1: edgelist_df (Pandas df): a pandas dataframe with the edgelist for the overall network
    """

    def create_map_of_dicts(row):

        # THIS NEEDS TO BE PASSED df.itertuples()

        cur_source = row.Source
        cur_target = row.Target
        cur_length = row.Length

        dict_for_igraph = {
            "source": cur_source,
            "target": cur_target,
            "length": cur_length,
        }

        return dict_for_igraph

    edgelist_df = create_edgelist_df(path)

    name = remove_extension(path)
    edgelist_df.index.name = name

    map_of_dicts = map(create_map_of_dicts, edgelist_df.itertuples())
    overall_network = gr.Graph.DictList(edges=list(map_of_dicts), vertices=None)

    return overall_network, edgelist_df


def decompose_individual_mitochondria(igraph_df_tuple):
    """
    Takes the overall igraph object for the whole image and breaks it down
    into individual mitochondria igraph objects comprising the greater network.

    (Not all mitochondria in the network are connected!)

    This works on ONE tuple at a time.

    Inputs
    igraph_df_tuple (tuple): tuple from initialize_network() function.

    0: overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
    1: edgelist_df (Pandas df): a pandas dataframe with the edgelist for the overall network

    Outputs [tuple]
    0: overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
    1: edgelist_df (Pandas df): a pandas dataframe with the edgelist for the overall network
    2: combined_mito_dataframe (Pandas df): a pandas dataframe where every row is a single mitochondria in the overall
                                            network and the columns describe how many nodes, edges, and how long the
                                            mitochondria is.

    """

    def analyze_each_mitochondria(decomposed_graph, name_from_edgelist):

        nodes = gr.Graph.vcount(decomposed_graph)
        edges = gr.Graph.ecount(decomposed_graph)
        sum_length_mitochondria = sum(decomposed_graph.es["length"])

        cur_graph_dict = {
            "Filename": name_from_edgelist,
            "Nodes": [nodes],
            "Edges": [edges],
            "Length": [sum_length_mitochondria],
        }

        single_mitochondria_dataframe = pd.DataFrame.from_dict(cur_graph_dict)

        return single_mitochondria_dataframe

    decomposed_network = gr.Graph.decompose(igraph_df_tuple[0])
    name = igraph_df_tuple[1].index.name

    map_of_each_mitochondria = map(
        lambda x: analyze_each_mitochondria(
            decomposed_graph=x, name_from_edgelist=name
        ),
        decomposed_network,
    )

    combined_mito_dataframe = (
        pd.concat(map_of_each_mitochondria).reset_index().drop(columns="index")
    )

    return igraph_df_tuple[0], igraph_df_tuple[1], combined_mito_dataframe


def summarize_image(big_tuple):
    """
    Takes a big tuple filled with data about a specific image, and then creates a row
    of a pandas dataframe with some metrics.

    Inputs [tuple] from decompose_individual_mitochondria
    0: overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
    1: edgelist_df (Pandas df): a pandas dataframe with the edgelist for the overall network
    2: combined_mito_dataframe (Pandas df): a pandas dataframe where every row is a single mitochondria in the overall
                                            network and the columns describe how many nodes, edges, and how long the
                                            mitochondria is.

    Outputs
    summary_dataframe (pandas dataframe): a single row to be concatonated later filled with metrics on a specific image

    """

    cur_igraph = big_tuple[0]
    name = big_tuple[1].index.name
    cur_mito_df = big_tuple[2]

    total_nodes = gr.Graph.vcount(cur_igraph)
    total_edges = gr.Graph.ecount(cur_igraph)
    total_length = sum(cur_mito_df["Length"])

    PHI = max(cur_mito_df["Length"]) / total_length
    n_mitochondria = len(cur_mito_df)

    average_edge_length = total_length / total_edges
    node_norm = total_nodes / total_length
    n_mito_norm_to_length = n_mitochondria / total_length
    n_mito_norm_to_edge = n_mitochondria / total_edges

    median_n_nodes = np.median(cur_mito_df["Nodes"])
    median_n_edges = np.median(cur_mito_df["Edges"])
    median_edge_length = np.median(cur_mito_df["Length"])

    data_dict = {
        "n_Nodes": total_nodes,
        "n_Edges": total_edges,
        "Total_Length": total_length,
        "n_Mitochondria": n_mitochondria,
        "PHI": PHI,
        "Ave_Edge_Length": average_edge_length,
        "n_Nodes_Norm_to_Length": node_norm,
        "n_Mito_Norm_to_Length": n_mito_norm_to_length,
        "n_Mito_Norm_to_Edges": n_mito_norm_to_edge,
        "Median_n_Nodes": median_n_nodes,
        "Median_n_Edges": median_n_edges,
        "Median_Edge_Length": median_edge_length,
    }
    summary_dataframe = pd.DataFrame(data_dict, index=[name])

    return summary_dataframe


def analyze_images(data_dir, name_dict=None):

    path_list_gnet = find_all_filetype(data_dir, ".gnet")
    path_list_mitograph = find_all_filetype(data_dir, ".mitograph")

    overall_networks = map(initialize_network, path_list_gnet)
    overall_networks_analyzed = map(decompose_individual_mitochondria, overall_networks)

    mitograph_automated_summaries = pd.concat(
        map(create_automated_mitograph_df, path_list_mitograph)
    )

    degree_distribution_summaries = pd.concat(
        map(create_degree_distribution_df, overall_networks_analyzed)
    )

    overall_networks = map(initialize_network, path_list_gnet)
    overall_networks_analyzed = map(decompose_individual_mitochondria, overall_networks)

    summaries = map(summarize_image, overall_networks_analyzed)

    summary_sheet = pd.concat(summaries)

    # use axis=1 so it concats columnar!!!
    full_summary_sheet = pd.concat(
        [summary_sheet, mitograph_automated_summaries, degree_distribution_summaries],
        axis=1,
        sort=True,
    )

    # a new column that requires the whole df

    full_summary_sheet["MitoGraphCS"] = (
        full_summary_sheet["PHI"]
        + full_summary_sheet["Ave_Edge_Length"]
        + full_summary_sheet["AveDeg"]
    ) / (
        full_summary_sheet["n_Nodes_Norm_to_Length"]
        + 1 / full_summary_sheet["Ave_Edge_Length"]
        + full_summary_sheet["n_Mito_Norm_to_Length"]
    )

    if name_dict is not None:
        full_summary_sheet = append_conditions(
            sheet=full_summary_sheet, name_dict=name_dict
        )

    return full_summary_sheet


def append_conditions(sheet, name_dict):
    """
    :param
    name_dict (dict): key/value pairs of the search parameter/what to replace it with
    sheet (pandas dataframe): the sheet to append these on

    :return
    Updated sheet
    """

    index_list = sheet.index.values

    sheet["Conditions"] = None

    for each_replacement in name_dict:

        indices_to_replace = [elm for elm in index_list if each_replacement in elm]

        for each_index in indices_to_replace:
            sheet.at[each_index, "Conditions"] = name_dict[each_replacement]

    return sheet


def create_degree_distribution_df(big_tuple):
    """

    Inputs [tuple] from decompose_individual_mitochondria
    0: overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
    1: edgelist_df (Pandas df): a pandas dataframe with the edgelist for the overall network
    2: combined_mito_dataframe (Pandas df): a pandas dataframe where every row is a single mitochondria in the overall
                                            network and the columns describe how many nodes, edges, and how long the
                                            mitochondria is.

    """

    # need to index same

    def calculate_degree_distribution(cur_graph):
        # Takes a single graph, works on it.

        # Bins will be used as such:
        # [0, 1) (including 0, excluding 1)
        # [1, 2) and so on.
        bins = [0, 1, 2, 3, 4, 5, 6, 7, 10]

        # Get the histogram
        cur_hist = np.histogram(cur_graph.degree(), bins=bins)

        # ============================================================================================

        # cur_graph.degree() lists for each vertex in the graph the number of edges adjacent to it.

        # For example, if a node has 2 edges, two mitochondrial edges, coming out of it, then
        # that vertex would have a degree of 2.

        # cur_graph.degree() returns an array n_vertices long, with a degree measurement for each vertex
        # as an integer.

        # We are simply taking a numpy histogram of this matrix.

        # ============================================================================================

        # Histogram values are in the first element of the array.
        hist_values = cur_hist[0]

        # remove the first element, which should be 0
        hist_values = hist_values[1:]

        # ============================================================================================

        # Brief interlude on cur_hist_values
        # Data will be like this: [  0, 580,   0, 371, 131]
        # Where each element describes how many k-1 neighbors it has,

        # ============================================================================================

        return hist_values

    name = big_tuple[1].index.name

    cur_igraph = big_tuple[0]

    cur_hist_values = calculate_degree_distribution(cur_igraph)

    # note: higher order junc arent in the ave degree bc we don't know what they're doing yet
    degree_dict = {
        "FreeEnds": cur_hist_values[0],
        "OneWayJunc": cur_hist_values[1],
        "TwoWayJunc": cur_hist_values[2],
        "ThreeWayJunc": cur_hist_values[3],
        "FourWayJunc": cur_hist_values[4],
        "HigherOrderJunc": sum(cur_hist_values[5:]),
        "AveDeg": (cur_hist_values[0])
        + (cur_hist_values[1])
        + (cur_hist_values[2] * 2)
        + (cur_hist_values[3] * 3)
        + (cur_hist_values[4] * 4),
    }

    degree_dist_df = pd.DataFrame(degree_dict, index=[name])

    return degree_dist_df
