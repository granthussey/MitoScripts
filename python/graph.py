
import mitographer as mtgraph
import mitodata as mt

def create_graph_suite(data_dir, data_name, name_dict):

    cur_data = mt.analyze_images(data_dir=data_dir, name_dict=name_dict)

    columns = list(cur_data.columns.values)
    columns.remove("Conditions")


    figures = map(lambda x: mtgraph.scattered_box_plot(data=cur_data, column=x, sample_order=name_dict.values(), data_name=data_name), columns)

    i = 0
    for item in list(figures):
        cur_col = columns[i]
        item.savefig(''.join([data_name,"_",cur_col,".png"]))
        i = i + 1