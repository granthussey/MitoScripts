import mitodata as mt
import mitographer as mtgrapher

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

cur_data = mt.analyze_images(data_dir=data_dir, name_dict=name_dict, data_name='compression')


# %%
"""

conditions = cur_data.Conditions.unique()

for cond in conditions:
    subset = cur_data.loc[cur_data["Conditions"] == cond]
    mtgrapher.clustermap(subset, title=cond, savefig=True)
    mtgrapher.heatmap(subset, title=cond, savefig=True)

"""


# %% Make PCA Plot

col = "Conditions"

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

# %%
to_graph = cur_data.drop(
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
            "FreeEnds",
            "FourWayJunc",
            'Vol_From_Length',
            "Median_Edge_Length",
        ])
cond_table = cur_data['Conditions'].copy()

# make array
x = to_graph.values
y = cond_table.values

# Standardizing the features
x = StandardScaler().fit_transform(x)

pca = PCA(n_components=2)
principalComponents = pca.fit_transform(x)
principalDf = pd.DataFrame(
    data=principalComponents,
    columns=["principal component 1", "principal component 2"],
    index=cond_table.index,
)

finalDf = pd.concat([principalDf, cond_table], axis=1)

ratio = pca.explained_variance_ratio_

fig = plt.figure(figsize=(8, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_xlabel("".join(["PC 1: ", str(round(ratio[0], 2))]), fontsize=15)
ax.set_ylabel("".join(["PC 2: ", str(round(ratio[1], 2))]), fontsize=15)
ax.set_title('PCA Plot, Labeled by Treatment/Geno')


targets = cond_table.unique()
colors = ["#1f77b4", "#17becf", '#7f7f7f', '#d62728', '#9467bd', '#e377c2']

for target, color in zip(targets, colors):

    indicesToKeep = finalDf[col] == target

    ax.scatter(
        finalDf.loc[indicesToKeep, "principal component 1"],
        finalDf.loc[indicesToKeep, "principal component 2"],
        c=color,
        s=50,
    )



ax.legend(targets)
ax.grid()

fig.savefig('PCA.pdf')


plt.show()



# %%

# break up data into each treatment group
# sum all x, sum all y, dividide by n_smaples
# plot 6 points


centroids = []

for each_group in targets:

    logic = finalDf['Conditions'] == each_group
    n_rows = len(finalDf['principal component 1'].loc[logic])

    x_coor = sum(finalDf['principal component 1'].loc[logic]) / n_rows
    y_coor = sum(finalDf['principal component 2'].loc[logic]) / n_rows


    centroids.append((x_coor, y_coor))

# %%

fig2 = plt.figure(figsize=(8, 8))
ax2 = fig.add_subplot(1, 1, 1)
ax2.set_label = 'doot'

for each_centroid, color, target in zip(centroids, colors, targets):
    ax2.scatter(
        each_centroid[0],
        each_centroid[1],
        c=color,
        label= target
    )

ax.legend(targets)
ax.grid()

plt.show()


# %%

# remove one at a time
# see if it gets better
import numpy as np

def run_2_dim_pca(df):

    x = df.values

    pca = PCA(n_components=2)

    scaled_x = StandardScaler().fit_transform(x)
    pc_values = pca.fit_transform(scaled_x)

    return sum(pca.explained_variance_ratio_)

df = cur_data

df = df.drop(columns='Conditions')

#drop_indices = np.random.choice(df.index, 1, replace=False)
#df_subset = df.drop(drop_indices)

#n_new_cols = 10
#while n_new_cols > 6:

# %%


from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pandas as pd
import numpy as np

# %%

def run_2_dim_pca(df):

    x = df.values

    pca = PCA(n_components=2)

    scaled_x = StandardScaler().fit_transform(x)
    pc_values = pca.fit_transform(scaled_x)

    return sum(pca.explained_variance_ratio_)


def find_weakest_link(df):
    cols = df.columns.values

    list_dfs = []

    for i_col in cols:

        list_dfs.append(df.drop(columns=i_col))

    pca_results = list(map(run_2_dim_pca, list_dfs))

    the_max = max(pca_results)

    index = pca_results == the_max

    remove = cols[index]

    print(len(remove))

    return remove[0], the_max


def do_it(df, threshold=0.95, min_cols=6):

    n_cols = df.shape[1]

    conds = df['Conditions'].copy()
    df = df.drop(columns='Conditions')

    prev_max = 0


    while n_cols > min_cols:

        cur_remove, cur_max = find_weakest_link(df)
        new_df = df.drop(columns=cur_remove)

        if prev_max > cur_max:
            break

        if cur_max > threshold:
            break

        df = new_df.copy()

        n_cols = df.shape[1]

    final_df = pd.concat([new_df, conds], axis=1)

    return final_df, cur_max


def run_it(df, threshold=0.95, min_cols=6):

    new_df, max = do_it(df=df, threshold=threshold, min_cols=min_cols)

    pca_suite(df=new_df, to_drop=[])