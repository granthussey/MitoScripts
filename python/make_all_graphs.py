import graph as g

to_graph = ((
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
        "p53_mdivi_2W": "KRAS_mdivi_2W",
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
        "p53_mdivi_2W": "KRAS_mdivi_2W",
        "KRAS_nodrug_control": "KRAS_nodrug_ctrl",
        "KRAS_nodrug_2W": "KRAS_nodrug_2W",
        "KRAS_mdivi_control": "KRAS_mdivi_ctrl",
        "KRAS_mdivi_2W": "KRAS_mdivi_2W",
    },
    "/Users/granthussey/Lab/FreshResults/cellrox",
))

for each_sample in to_graph:
    g.create_graph_suite(data_dir=each_sample[2], data_name=each_sample[0], name_dict=each_sample[1])
