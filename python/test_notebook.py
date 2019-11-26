import seaborn as sns
import matplotlib.pyplot as plt
import mitodata as mt

# %%


def scatter_plot(**kwargs):
    fig = plt.figure(figsize=(5, 5))
    sns.scatterplot(**kwargs)
    plt.ylim(-3, 3)
    plt.xlim(-3, 3)
    plt.title("{x} vs {y}".format(**kwargs))
    plt.show()
    return fig


# %%
to_graph = (
    "compression",
    {
        "p53_control": "p53_ctrl",
        "p53_aga": "p53_aga",
        "p53_2W": "p53_2W",
        "KRAS_control": "KRAS_ctrl",
        "KRAS_aga": "KRAS_aga",
        "KRAS_2W": "KRAS_2W",
    },
    "/Users/granthussey/Lab/FreshResults/compression",
)

data_dir = to_graph[2]
name_dict = to_graph[1]

cur_data = mt.analyze_images(data_dir=data_dir, name_dict=name_dict)


# %%

df_graph = cur_data.drop(
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
        "PHI"
    ]
)


# %%

df_graph_corr = df_graph.corr()
cmap = sns.diverging_palette(10, 220, sep=80, as_cmap=True)

# %%

plt.figure(figsize=[6,6])
sns.heatmap(df_graph_corr, cmap=cmap, square=True, vmax=1, vmin=-1)
plt.show()

# %%
g = sns.clustermap(data=df_graph_corr, cmap=cmap, figsize=[10,10], square=True, vmin=-1, vmax=1)
plt.show()
