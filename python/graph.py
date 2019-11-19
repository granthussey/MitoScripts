
import pandas as pd
import mitographer as mtgraph
import mitodata as mt

sample_order = {
    "p53_control": "p53_ctrl",
    "p53_aga": "p53_aga",
    "p53_2W": "p53_2W",
    "KRAS_control": "KRAS_cntrl",
    "KRAS_aga": "KRAS_aga",
    "KRAS_2W": "KRAS_2W"
}

cur_data = mt.analyze_images(data_dir='/Users/granthussey/Lab/FreshResults/compression', name_dict=sample_order)


for each_col in columns:
    mtgraph.scattered_box_plot(data=cur_data, column=each_col, sample_order=sample_order)