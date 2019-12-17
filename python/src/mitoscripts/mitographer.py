import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np
import mitoscripts.mitodata as mt


DEFAULT_STYLE = "tableau-colorblind10"


def scattered_box_plot(
    data, column, sample_order, data_name="", ax=None, x="Conditions", logscale=False
):
    sns.set(style="ticks")

    if ax is None:
        f, ax = plt.subplots(figsize=(7, 6))
    else:
        f = None

    if logscale:
        data[column] = np.log10(data[column])

    # Plot the orbital period with horizontal boxes
    sns.boxplot(
        x=x,
        y=column,
        data=data,
        order=sample_order,
        whis="range",
        palette="vlag",
        ax=ax,
    )

    # Add in points to show each observation
    sns.swarmplot(
        x=x,
        y=column,
        data=data,
        order=sample_order,
        size=2,
        color=".3",
        linewidth=0,
        ax=ax,
    )

    # Tweak the visual presentation
    ax.xaxis.grid(True)
    ax.set(ylabel=column, title=" ".join([data_name, column]))
    sns.despine(trim=True, left=True)
    plt.xticks(rotation=45)
    plt.show()

    return f


def create_graph_suite(data_dir, data_name, name_dict, savefigs=False):
    """currently working"""
    cur_data = mt.analyze_images(
        data_dir=data_dir, name_dict=name_dict, data_name=data_name
    )

    columns = list(cur_data.columns.values)
    columns.remove("Conditions")

    figures = map(
        lambda x: scattered_box_plot(
            data=cur_data,
            column=x,
            sample_order=name_dict.values(),
            data_name=data_name,
        ),
        columns,
    )

    if savefigs:
        i = 0
        for item in list(figures):
            cur_col = columns[i]
            item.savefig("".join([data_name, "_", cur_col, ".png"]))
            i = i + 1

    return cur_data


def create_graph_array(cur_data, name_dict, savefigs=False):
    """currently not working"""

    cur_data_graph = cur_data.drop(
        columns=[
            "MitoGraphCS",
            "n_Nodes_Norm_to_Length",
            "n_Nodes",
            "Median_n_Nodes",
            "Median_n_Edges",
            "Vol_From_Voxels",
            "Std_Width_um",
            "Total_Length_um",
            "OneWayJunc",
            "HigherOrderJunc",
            "AveDeg",
        ]
    )

    col = list(cur_data_graph.columns.values)
    col.remove("Conditions")

    fig, ax = plt.subplots(nrows=7, ncols=2, resize=True)

    i = 0
    j = 0
    for each_col in col:
        scattered_box_plot(
            data=cur_data_graph,
            column=each_col,
            sample_order=name_dict.values(),
            data_name=cur_data_graph.index.name,
            ax=ax[i][j],
        )

        i += 1
        j += 1

        if i > 6:
            i = 0
        if j > 1:
            j = 0

    if savefigs:
        filename = "".join([cur_data_graph.index.name, "_graphs.png"])
        fig.savefig(filename, dpi=300)


def clean_df_and_get_corr(df):

    df_graph = df.drop(
        columns=[
            "MitoGraphCS",
            "Conditions",
            "n_Nodes_Norm_to_Length",
            "n_Nodes",
            "Median_n_Nodes",
            "Median_n_Edges",
            "Vol_From_Voxels",
            "Std_Width_um",
            "Total_Length_um",
            "OneWayJunc",
            "HigherOrderJunc",
            "AveDeg",
            "PHI",
        ]
    )

    df_graph_corr = df_graph.corr()

    return df_graph_corr


def heatmap(df, title="", data_name="", savefig=False):

    df_graph_corr = clean_df_and_get_corr(df)

    cmap = sns.diverging_palette(10, 220, sep=80, as_cmap=True)
    fig = plt.figure(figsize=[6, 6])
    ax = plt.axes()
    sns.heatmap(df_graph_corr, ax=ax, cmap=cmap, square=True, vmax=1, vmin=-1)
    ax.set_title("".join(["Heatmap for ", data_name, " ", title]))
    fig.subplots_adjust(bottom=0.30, left=0.3)

    if savefig:
        filename = "".join([data_name, "_heatmap_", title, "_.png"])
        fig.savefig(filename, dpi=300)

    plt.show()

    return fig


def clustermap(df, title="", data_name="", savefig=False):

    df_graph_corr = clean_df_and_get_corr(df)
    cmap = sns.diverging_palette(10, 220, sep=80, as_cmap=True)
    g = sns.clustermap(
        data=df_graph_corr, cmap=cmap, figsize=[10, 7], square=True, vmin=-1, vmax=1
    )
    g.ax_row_dendrogram.set_visible(False)
    g.ax_col_dendrogram.set_visible(False)
    fig = g.fig
    ax = fig.axes
    fig.subplots_adjust(bottom=0.30, left=0.3)
    g.fig.suptitle("".join(["Clustermap for ", data_name, " ", title]))

    if savefig:
        filename = "".join([data_name, "_clustermap_", title, "_.png"])
        g.cax.set_visible(False)
        fig.savefig(filename, dpi=300, bbox_inches="tight")

    plt.show()

    return fig


def get_default_col_to_drop():

    to_drop = [
        "MitoGraphCS",
        "Conditions",
        "n_Nodes_Norm_to_Length",
        "n_Nodes",
        "Median_n_Nodes",
        "Median_n_Edges",
        "Vol_From_Voxels",
        "Std_Width_um",
        "Total_Length_um",
        "OneWayJunc",
        "HigherOrderJunc",
        "AveDeg",
        "FreeEnds",
        "FourWayJunc",
        "Vol_From_Length",
    ]

    return to_drop


def run_pca(df, to_drop=None):

    if not "Conditions" in df.columns:
        print("Error. Please have a Conditions column in df.")

    if to_drop is None:
        to_drop = get_default_col_to_drop()

    cond_series = df["Conditions"].copy()

    to_graph = df.drop(columns=to_drop)

    if "Conditions" in to_graph.columns:
        to_graph = to_graph.drop(columns="Conditions")

    x = to_graph.values
    y = cond_series.values

    pca = PCA(n_components=2)

    scaled_x = StandardScaler().fit_transform(x)
    pc_values = pca.fit_transform(scaled_x)

    principal_df = pd.DataFrame(
        data=pc_values, columns=["PC1", "PC2"], index=cond_series.index,
    )

    pca_plottable_df = pd.concat([principal_df, cond_series], axis=1)

    return pca_plottable_df, pca


def make_pca_plot(df, to_drop=None, style=DEFAULT_STYLE):

    pca_plottable_df, pca = run_pca(df, to_drop=to_drop)

    pca_var_ratio = pca.explained_variance_ratio_

    labels = pca_plottable_df["Conditions"].unique()

    plt.figure(figsize=[8, 8])

    plt.style.use(style)

    for i_label in labels:

        logic = pca_plottable_df["Conditions"] == i_label

        plt.scatter(
            x=pca_plottable_df.loc[logic, "PC1"],
            y=pca_plottable_df.loc[logic, "PC2"],
            label=i_label,
        )

    plt.xlabel("".join(["PC 1: ", str(round(pca_var_ratio[0], 2))]), fontsize=15)
    plt.ylabel("".join(["PC 2: ", str(round(pca_var_ratio[1], 2))]), fontsize=15)

    plt.legend()

    plt.title("PCA Plot, Labeled by Treatment/Genotype")
    plt.show()


def make_centroid_plot(df, to_drop=None, style=DEFAULT_STYLE):

    if not "Conditions" in df.columns:
        print("Error. Please have a Conditions column in df.")

    df_from_pca, pca = run_pca(df, to_drop=to_drop)

    pca_var_ratio = pca.explained_variance_ratio_

    labels = df_from_pca["Conditions"].unique()

    centroids = []

    for i_label in labels:

        logic = df_from_pca["Conditions"] == i_label

        # how many samples we got in this subset
        n_rows = len(df_from_pca["PC1"].loc[logic])

        x_coor = sum(df_from_pca["PC1"].loc[logic]) / n_rows
        y_coor = sum(df_from_pca["PC2"].loc[logic]) / n_rows

        centroids.append((x_coor, y_coor))

    plt.figure(figsize=[8, 8])
    plt.style.use(style)

    for i_centroid, i_label in zip(centroids, labels):

        plt.scatter(i_centroid[0], i_centroid[1], label=i_label)

    plt.xlabel("".join(["PC 1: ", str(round(pca_var_ratio[0], 2))]), fontsize=15)
    plt.ylabel("".join(["PC 2: ", str(round(pca_var_ratio[1], 2))]), fontsize=15)

    plt.legend()

    plt.title("PCA Centroids, Labeled by Treatment/Genotype")
    plt.show()


def make_scree_plot(df, to_drop=None, style=DEFAULT_STYLE, n_comp=None):

    if not "Conditions" in df.columns:
        print("Error. Please have a Conditions column in df.")

    if to_drop is None:
        to_drop = get_default_col_to_drop()

    cond_series = df["Conditions"].copy()

    to_graph = df.drop(columns=to_drop)

    if "Conditions" in to_graph.columns:
        to_graph = to_graph.drop(columns="Conditions")

    if n_comp is None:
        n_comp = min(to_graph.shape)

    x = to_graph.values
    y = cond_series.values

    pca = PCA(n_components=n_comp)

    scaled_x = StandardScaler().fit_transform(x)
    pc_values = pca.fit_transform(scaled_x)

    # create a proper list "PC1", "PC2", etc.
    cols = ["".join(["PC", str(i + 1)]) for i in range(n_comp)]

    principal_df = pd.DataFrame(data=pc_values, columns=cols, index=cond_series.index,)

    pca_plottable_df = pd.concat([principal_df, cond_series], axis=1)

    thing = np.cumsum(np.round(pca.explained_variance_ratio_, decimals=4) * 100)

    plt.figure(figsize=[8, 8])
    plt.style.use(style)

    plt.plot(thing)

    plt.xlabel("Num PC")
    plt.ylabel("Cumulative PC")

    plt.title("Scree Plot")
    plt.show()


def pca_suite(df, to_drop=None, style=DEFAULT_STYLE):

    make_pca_plot(df, to_drop=to_drop, style=style)
    make_scree_plot(df, to_drop=to_drop, style=style)
    make_centroid_plot(df, to_drop=to_drop, style=style)


def scatter_length_distribution(data_dir, name_dict, data_name="", savefig=False):

    data = mt.analyze_mitochondrial_length_distribution(
        data_dir=data_dir, name_dict=name_dict, data_name=data_name
    )

    # get a list of all images we need to create rows for
    unique_images = data.index.unique()

    # determine which image has the max # of mito (and more specifically what that # is)
    max_num_mito = max(map(lambda x: len(data.loc[x]), unique_images))

    the_index = []
    row_vectors = []

    for each_image in unique_images:

        subset = data.loc[each_image]

        # get things sorted
        lengths_of_mito = np.sort(subset["Length"].values)
        lengths_of_mito = lengths_of_mito[::-1]

        if len(lengths_of_mito) == max_num_mito:
            new_vector = lengths_of_mito
        else:
            num_zeros_needed = max_num_mito - len(lengths_of_mito)
            pad = np.zeros(num_zeros_needed)
            pad[:] = np.nan
            new_vector = np.concatenate([lengths_of_mito, pad])

        new_vector = np.log2(new_vector)

        the_index.append(each_image)
        row_vectors.append(new_vector)

    new = pd.DataFrame(row_vectors)
    new["Filename"] = the_index
    new = new.set_index("Filename")

    #####

    new_with_conds = mt.append_conditions(new, name_dict=name_dict)

    ####

    sorted_list = []
    for each_cond in name_dict.values():
        sorted_list.append(
            new_with_conds.loc[new_with_conds["Conditions"] == each_cond]
        )

    sorted_data = pd.concat(sorted_list)

    stacked_list = []

    def do_the_counts(part):

        col = part.isna().sum(axis=1)
        new_thing = part.copy()
        new_thing["counts"] = col
        new_thing = new_thing.sort_values(by="counts", ascending=False)

        return new_thing

    for each_cond in name_dict.values():
        subset = sorted_data.loc[sorted_data["Conditions"] == each_cond]
        stacked_list.append(do_the_counts(subset))

    stacked_data = pd.concat(stacked_list)

    stacked_data = stacked_data.drop(columns=["Conditions", "counts"])

    cmap = sns.diverging_palette(150, 275, s=80, l=55, n=9, as_cmap=True)
    fig = plt.figure(figsize=[12, 12])
    ax = plt.axes()
    sns.heatmap(
        stacked_data, ax=ax, cmap=cmap, cbar_kws={"label": "Mitochondrial Length"}
    )
    ax.set(xlabel="Number of Mitochondria", ylabel="Sample")
    fig.subplots_adjust(bottom=0.30, left=0.3)

    if savefig:
        filename = "".join([data_name, "_mito_dist_", "_.png"])
        fig.savefig(filename, dpi=300)

    plt.show()

    return data
