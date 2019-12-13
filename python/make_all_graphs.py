import mitographer as mtgraph

to_graph = (
    (
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
    ),
    (
        "mdivi",
        {
            "p53_nodrug_cntrl": "p53_nodrug_ctrl",
            "p53_nodrug_aga": "p53_nodrug_aga",
            "p53_nodrug_2W": "p53_nodrug_2W",
            "p53_mdivi_cntrl": "p53_mdivi_ctrl",
            "p53_mdivi_aga": "p53_mdivi_aga",
            "p53_mdivi_2W": "p53_mdivi_2W",
            "KRAS_nodrug_cntrl": "KRAS_nodrug_ctrl",
            "KRAS_nodrug_aga": "KRAS_nodrug_aga",
            "KRAS_nodrug_2W": "KRAS_nodrug_2W",
            "KRAS_mdivi_cntrl": "KRAS_mdivi_ctrl",
            "KRAS_mdivi_aga": "KRAS_mdivi_aga",
            "KRAS_mdivi_2W": "KRAS_mdivi_2W",
        },
        "/Users/granthussey/Lab/FreshResults/mdivi",
    ),
    (
        "cellrox",
        {
            "p53_nodrug_control": "p53_nodrug_ctrl",
            "p53_nodrug_2W": "p53_nodrug_2W",
            "p53_mdivi_control": "p53_mdivi_ctrl",
            "p53_mdivi_2W": "p53_mdivi_2W",
            "KRAS_nodrug_control": "KRAS_nodrug_ctrl",
            "KRAS_nodrug_2W": "KRAS_nodrug_2W",
            "KRAS_mdivi_control": "KRAS_mdivi_ctrl",
            "KRAS_mdivi_2W": "KRAS_mdivi_2W",
        },
        "/Users/granthussey/Lab/FreshResults/cellrox",
    ),
)

# this not only graphs and saves preliminary data, but also outputs cur_data for each sample.
# it returns the df as an immutable

summary_dfs = []

for each_sample in to_graph:
    summary_dfs.append(
        mtgraph.create_graph_suite(
            data_dir=each_sample[2], data_name=each_sample[0], name_dict=each_sample[1]
        )
    )


def run_per_treatment_heatmap_analysis(full_summary_sheet):

    name = full_summary_sheet.index.name

    unique_treatments = list(full_summary_sheet.Conditions.unique())

    def find_rows_with_condition_name(sheet, cond):
        those_rows = sheet.loc[sheet["Conditions"] == cond]
        those_rows.index.name = cond
        return those_rows

    all_rows = map(
        lambda x: find_rows_with_condition_name(full_summary_sheet, cond=x),
        unique_treatments,
    )

    set(
        map(
            lambda x: mtgraph.heatmap(
                x, title=x.index.name, data_name=name, savefig=True,
            ),
            all_rows,
        )
    )

    set(
        map(
            lambda x: mtgraph.clustermap(
                x, title=x.index.name, data_name=name, savefig=True,
            ),
            all_rows,
        )
    )


for each_sheet in summary_dfs:
    run_per_treatment_heatmap_analysis(each_sheet)
