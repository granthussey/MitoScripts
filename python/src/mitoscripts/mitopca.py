from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import pandas as pd
import numpy as np
import mitoscripts.mitographer as mtgrapher

def run_2_dim_pca(df, take_sum=True):
    x = df.values

    pca = PCA(n_components=2)

    scaled_x = StandardScaler().fit_transform(x)
    pc_values = pca.fit_transform(scaled_x)

    if take_sum:
        return sum(pca.explained_variance_ratio_)
    elif not take_sum:
        return pca.explained_variance_ratio_


def remove_dissimilarity(df, threshold=0.95, min_cols=6):
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

    n_cols = df.shape[1]

    conds = df["Conditions"].copy()
    df = df.drop(columns="Conditions")

    prev_max = 0

    while n_cols > min_cols:

        cur_remove, cur_max = find_weakest_link(df)
        print(cur_remove)
        new_df = df.drop(columns=cur_remove)

        if prev_max > cur_max:
            break

        if cur_max > threshold:
            break

        df = new_df.copy()
        n_cols = df.shape[1]

    final_df = pd.concat([new_df, conds], axis=1)

    return final_df, cur_max


def run_special_pca(df, threshold=0.95, min_cols=6):

    new_df, _ = remove_dissimilarity(df=df, threshold=threshold, min_cols=min_cols)
    mtgrapher.pca_suite(df=new_df, to_drop=[])


def force_50_50_axes(df, min_cols=6):
    """Currently not working"""

    def find_most_similar(df):

        cols = df.columns.values

        list_dfs = []
        for i_col in cols:
            list_dfs.append(df.drop(columns=i_col))

        pca_results = list(map(lambda x: run_2_dim_pca(x, take_sum=False), list_dfs))

        abs_array = list(map(lambda x: np.abs(x - 0.5), pca_results))

        concat_abs_array = np.stack(abs_array)

        PC1_low = np.min(concat_abs_array[:, 0])
        PC2_low = np.min(concat_abs_array[:, 1])

        lowest = min([PC1_low, PC2_low])

        idx = concat_abs_array == lowest

        lowest_col = cols[np.logical_or(idx[:, 0], idx[:, 1])]

        return lowest_col

    n_cols = df.shape[1]

    conds = df["Conditions"].copy()
    df = df.drop(columns="Conditions")

    for i in range(5):
        col_to_remove = find_most_similar(df)
        new_df = df.drop(columns=col_to_remove)
        df = new_df.copy()

    final_df = pd.concat([new_df, conds])

    return final_df
