import graph as g

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

g.create_graph_suite(data_dir=to_graph[2], data_name=to_graph[0], name_dict=to_graph[1])
