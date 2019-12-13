import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt


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


data = pd.read_csv(
    "/Users/granthussey/github/MitoScripts/compression_results_for_pca.csv"
)

data = data.set_index("compression")

name_dict = {
    "KRAS_control": "No compression",
    "KRAS_aga": "Agarose only",
    "KRAS_2W": "Weighted compression",
}

proper_conds = append_conditions(data, name_dict)

# %%


def scattered_box_plot(
    data, column, sample_order, the_y_label, data_name="", ax=None, x="Conditions"
):

    sns.set(style="ticks")

    f, ax = plt.subplots(figsize=(7, 5))

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
    ax.set(ylabel=the_y_label, xlabel="")
    sns.despine(trim=True, left=True)
    plt.xticks(rotation=0)
    plt.show()

    return f


scattered_box_plot(
    proper_conds,
    column="n_Mitochondria",
    sample_order=name_dict.values(),
    the_y_label="Number of Mitochondria",
)
scattered_box_plot(
    proper_conds,
    column="Median_Edge_Length",
    sample_order=name_dict.values(),
    the_y_label="Median Edge Length (um)",
)
