import mitodata as mt
import mitographer as mtgrapher
import pandas as pd

doot = (
    "/Users/granthussey/github/MitoScripts/MitoScripts/DontSync/data",
    {
        "KRAS_mdivi_2W": "KRAS_mdivi_2W",
        "KRAS_mdivi_control": "KRAS_mdivi_ctrl",
        "KRAS_nodrug_control": "KRAS_nodrug_ctrl",
    },
)
thing = mt.get_indiv_data(data_dir=doot[0], name_dict=doot[1], data_name="test")

pd.sort_values(by=)

mtgrapher.scattered_box_plot(
    data=thing,
    column="Length",
    sample_order=thing.index.unique(),
    data_name="test",
    x=thing.index,
 )


 # next thing to do: get this graphing in order
 # use a jupyter notebook