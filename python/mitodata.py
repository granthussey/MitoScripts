import glob

import igraph as gr
import numpy as np
import pandas as pd


def remove_enclosing_dirs(full_path):
    """""
    Inputs
    full_path (string): a Unix-based path to a file (with extension)

    Outputs
    filename (string): just the filename (with extension) from the path

    Notes
    If you pass a filename to this function, emaning it doesn't
    contain the "/" string, it will simply return the input back to you.
    """ ""

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


def remove_extension(path_or_filename_with_extension):
    """""
    Inputs
    path_or_filename_with_extension: either a path or a filename that for a specific file, with extension.
    (e.g. /usr/dir/sample.mitograph or sample.mitograph)

    Ouputs
    filename_without_extension: just the filename without the extension (e.g. "sample")

    Notes
    This function may fail if more than one . is in the file, such as ".tar.gz"
    """ ""

    # Remove all enclosing directories, only get the name of file.
    cur_filename_with_extension = remove_enclosing_dirs(path_or_filename_with_extension)

    # Remove the extension by splitting the string at each "." and only taking first part.
    filename_without_extension = cur_filename_with_extension.split(".")[0]

    return filename_without_extension


def find_all_filetype(data_dir, extension):
    """""
    Inputs
    data_dir (string): path to where your MitoGraph output data are
    extension (string): the extension to search for (e.g. ".gnet", ".mitograph")

    Outputs
    path_list (list of strings): a list where each element is a string containing the path for desired files (with extension)
    (e.g. path_list = [sample1.gnet, sample2.gnet])
    """ ""

    # create a string to search for, include a wildcard * in place of the name of the file
    search_criteria = "".join([data_dir, "/*", extension])

    # use glob.glob to do the searching and retreive your list!
    path_list = glob.glob(search_criteria)

    return path_list


def analyze_images(data_dir):

    path_list_gnet = find_all_filetype(data_dir, ".gnet")
    path_list_mitograph = find_all_filetype(data_dir, ".mitograph")

    overall_networks = map(initialize_networks, path_list_gnet)

    overall_networks_with_mitochondria = map(analyze_each_image, overall_networks)

    # mitograph_automated_summaries = map(create_automated_mitograph_df, path_list_mitograph)

    summaries = map(summarize_image, overall_networks_with_mitochondria)

    summary_sheet = pd.concat(summaries)

    return summary_sheet


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
    df = df.index.name = name

    return df


def initialize_networks(path):
    """""
    Creates an overall network (graph theory graph) for the image at large.
    
    Inputs
    path to the single gnet file, which contains connectivity data
    
    Outputs
    Graph
    
    """ ""

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

    gnet_df = create_gnet_df(path)

    name = remove_extension(path)
    gnet_df.index.name = name

    map_of_dicts = map(create_map_of_dicts, gnet_df.itertuples())
    overall_network = gr.Graph.DictList(edges=list(map_of_dicts), vertices=None)

    return overall_network, gnet_df


def analyze_each_image(igraph_df_tuple):
    # Takes the output of initialize_networkss and processes is,
    # adding a new data element onto the tuple.

    def analyze_each_mitochondria(decomp, name):

        nodes = gr.Graph.vcount(decomp)
        edges = gr.Graph.ecount(decomp)
        sum_length_mitochondria = sum(decomp.es["length"])

        cur_graph_dict = {
            "Filename": name,
            "Nodes": [nodes],
            "Edges": [edges],
            "Length": [sum_length_mitochondria],
        }

        single_mitochondria_dataframe = pd.DataFrame.from_dict(cur_graph_dict)

        return single_mitochondria_dataframe

    decomp = gr.Graph.decompose(igraph_df_tuple[0])
    name = igraph_df_tuple[1].index.name

    map_of_each_mitochondria = map(
        lambda x: analyze_each_mitochondria(decomp=x, name=name), decomp
    )

    combined_mito_dataframe = (
        pd.concat(map_of_each_mitochondria).reset_index().drop(columns="index")
    )

    return igraph_df_tuple[0], igraph_df_tuple[1], combined_mito_dataframe


def analyze_network_components(overall_mitochondrial_network, name):
    """""
    Takes each overall network and decomposes it into individual mitochondrion
    Analyzes those and outputs that into a sheet
    
    """ ""


def create_gnet_df(path):

    df = pd.read_csv(path, sep="\t").reset_index()
    df = df.rename(columns={"level_0": "Source", "level_1": "Target"})
    df = df.rename(columns={df.columns[2]: "Length"})  # edits the third column

    return df


def summarize_image(igraph_df_indiv_tuple):

    # if igraph_df_indiv_tuple[3].index.name != igraph_df_indiv_tuple[1].index.name:
    #    print('STOP!!!!!')

    name = (igraph_df_indiv_tuple[1].index.name,)
    cur_igraph = igraph_df_indiv_tuple[0]
    cur_mito_df = igraph_df_indiv_tuple[2]

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

    #'Image' : igraph_df_indiv_tuple[1].index.name,

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

    #   'Volume_from_Voxels_um3' : ,
    #'Ave_Width_Tubule_um' : ,
    # 'Std_Width_Tubule' : ,
    # 'Volume_from_Length'

    summary_dataframe = pd.DataFrame(data_dict, index=[name])

    return summary_dataframe
