import glob

import igraph as gr
import numpy as np
import pandas as pd


def remove_enclosing_dirs(full_path):
    """ Remove any directories in a filepath

    If you pass a filename to this function, meaning it doesn't
    contain the "/" string, it will simply return the input back to you.

    Args:
        full_path (str): a Unix-based path to a file (with extension)

    Returns:
        filename (string): just the filename (with extension) from the path

    """

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
    """ Removes the extention from a string, as well as the directories.

    This function may fail if more than one . is in the file, such as ".tar.gz"

    Args:
        string: (string): either a path or a filename that for a specific file, with extension.
                (e.g. /usr/dir/sample.mitograph or sample.mitograph)

    Returns:
        filename_without_extension (str): just the filename without the extension (e.g. "sample")

    """

    # Remove all enclosing directories, only get the name of file.
    cur_filename_with_extension = remove_enclosing_dirs(string)

    # Remove the extension by splitting the string at each "." and only taking first part.
    filename_without_extension = cur_filename_with_extension.split(".")[0]

    return filename_without_extension


def find_all_filetype(data_dir, extension):
    """ Finds all files in a directory, returns their path

    Args:
        data_dir (str): path to where your MitoGraph output data are
        extension (str): the extension to search for (e.g. ".gnet", ".mitograph")

    Returns:
        path_list (list of strings): a list where each element is a string containing the path for desired files (with extension)
                                    (e.g. path_list = [sample1.gnet, sample2.gnet])

    """

    # create a string to search for, include a wildcard * in place of the name of the file
    search_criteria = "".join([data_dir, "/*", extension])

    # use glob.glob to do the searching and retreive your list!
    path_list = glob.glob(search_criteria)

    return path_list


def create_edgelist_df(path):
    """ Reads in a path to a .gnet file, produces a df of an edgelist for use in igraph

    Args:
        path (str): This must be a path to a .gnet file

    Returns:
        df (pandas df): This is an edgelist to be then processed by igraph to create a graph
                        theory representation of the mitochondria within that .gnet file's image

    """

    df = pd.read_csv(path, sep="\t").reset_index()
    df = df.rename(columns={"level_0": "Source", "level_1": "Target"})

    # edits the third column, which is always the total # of nodes (per MitoGraph coding)
    df = df.rename(columns={df.columns[2]: "Length"})

    return df


def create_automated_mitograph_df(path):
    """ Creates a cleanly-formatted df containing metrics that are automatic exports from the MitoGraph C code

    Args:
        path (str): path to a .mitograph file

    Returns:
        df (pandas df): a cleanly-formatted df of MitoGraph automated outputs

    """

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
    """ Creates a graph theory network of all mitochondria in an image.

    Args:
        path (str): path to a single gnet file, which contains connectivity data.
                    One exists per image.

    Returns:
        (tuple): a tuple containing:
            overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
            edgelist_df (pandas df) the pandas df a pandas dataframe with the edgelist for the overall network
    """

    def create_map_of_dicts(row):
        """ for use in creating a list of dictionaries to be turned into pandas df in parent func
        THIS NEEDS TO BE PASSED df.itertuples()
        """

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
    """ Breaks down a whole-image igraph obj into its constituate mitochondria as separate igraph objs

     (Not all mitochondria in the network are connected!)

    Args:
        igraph_df_tuple (tuple): a tuple from initialize_network() containing:
            overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
            edgelist_df (Pandas df): a pandas dataframe with the edgelist for the overall network

    Returns:
        (tuple): a tuple containing:
            overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.

            edgelist_df (Pandas df): edgelist for the overall network

            combined_mito_dataframe (Pandas df): a pandas dataframe where every row is a single mitochondria in the overall
                                                    network and the columns describe how many nodes, edges, and how long the
                                                    mitochondria is.

    """

    def analyze_each_mitochondria(decomposed_graph, name_from_edgelist):
        """ creates a single-row pandas df of the total nodes, edges, and length of a single mitochondria

        Args:
            decomposed_graph (igraph obj): a single mitochondria decomposed from an whole-image igraph obj

            name_from_edgelist (str): name of the overall image mitochondria came from
                                     This is derived from an edgelist df, hence its name "name_from_edgelist"

        Returns:
            single_mitochondria_dataframe (pandas df): a single row df with nodes, edges, and length metrics for
                                                       decomposed_graph's mitochondria

        """

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
    """ Takes a big tuple filled with data about a specific image, then summarizes it into a single pandas df row

    Args:
        big_tuple (tuple): containing:
            overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
            edgelist_df (Pandas df): a pandas dataframe with the edgelist for the overall network
            combined_mito_dataframe (Pandas df): a pandas dataframe where every row is a single mitochondria in the overall
                                            network and the columns describe how many nodes, edges, and how long the
                                            mitochondria is.

    Returns:
        summary_dataframe (pandas df): a single row to be concatonated later filled with metrics on a specific image

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


def create_degree_distribution_df(big_tuple):
    """ Creates a degree distribution df for processing in the analyze_image() func

    Args:
        big_tuple (tuple): containing:
            overall_network (igraph object): igraph object for a single image. Contains "length" data for each edge.
            edgelist_df (Pandas df): a pandas dataframe with the edgelist for the overall network
            combined_mito_dataframe (Pandas df): a pandas dataframe where every row is a single mitochondria in the overall
                                            network and the columns describe how many nodes, edges, and how long the
                                            mitochondria is.

    Returns:
        degree_dist_df (pandas df): dataframe containing data on degree distributions of an image

    """

    def calculate_degree_distribution(cur_graph):
        """Takes a single graph, works on it"""

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


def append_conditions(sheet, name_dict):
    """ Add row "Conditions" describing the treatment of each image (+/- drug, +/- compression, etc)

    Args:
        sheet (pandas df): existing sheet with data on images from data_dir
        name_dict (dict): dict containing key:value pairs with keys of filename at time of
                          acquisition and values of what they should be labeled

                          (ex: KRAS_control: KRAS_ctrl, p53_aga: p53_aga)
                          This will make anything labeled KRAS_control_001_041 etc named "KRAS_control"
    Returns:
        sheet (pandas df): updated sheet with

    """


    index_list = sheet.index.values

    sheet["Conditions"] = None

    for each_replacement in name_dict:

        indices_to_replace = [elm for elm in index_list if each_replacement in elm]

        for each_index in indices_to_replace:
            sheet.at[each_index, "Conditions"] = name_dict[each_replacement]

    return sheet


def analyze_images(data_dir, name_dict=None, data_name="index"):
    """ Runs image analysis on each sample within a data directory

    Args:
        data_dir (str): path to where the data is.
        name_dict (dict): dict containing key:value pairs with keys of filename at time of
                          acquisition and values of what they should be labeled
                          (ex: KRAS_control: KRAS_ctrl)

    Returns:
        full_summary_sheet (pandas df)

    """

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

    full_summary_sheet.index.name = data_name

    return full_summary_sheet
