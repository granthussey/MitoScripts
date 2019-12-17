# MitoScripts

This Python package, **MitoScripts**, assists in quantifies mitochondrial morphology. It was written by me, Grant Hussey, as a rotation project in the Holt Lab at NYU Langone Health's Institute of Molecular Biomedicine. 

This package first requires data to be processed into 3D models by using [MitoGraph](https://github.com/vianamp/MitoGraph), an open-source software developed by [Matheus Viana](https://sites.google.com/site/vianamp/).

This build of MitoScripts works for MitoGraph v3, and was tested on mammilian cells.

 ## General Notes and Procedure

 MitoGraph is a software that takes z-stack images of mitochondria and produces a 3D model. This Python package, _MitoScripts_, takes the output from MitoGraph and quantifies it.

### Steps 

<a name="step1"></a>**1. Acquire your data.**

*Be sure to have a consistent naming scheme for these image files that do not repeat, in order to automate the quantification process downstream.*

 <a name="step2"></a>**2. Process your data through MitoGraph.**

**3. Run MitoScripts.**

After MitoGraph processing is completed, you get *.gnet* and *.mitograph* files. These are used by MitoScripts to quantify mitochondrial morphology.

First, gather the *.gnet* and *.mitograph* files into a single directory. Next, import the python package, which has three modules, [mitographer](#mtgrapher), [mitodata](#mt), and [mitopca](#mtpca). You will most likely only interface with **mitographer**.

As of now, MitoScripts works best if used in scientific mode in an IDE or a jupyter notebook.

`` import mitodata as mt ``

`` import mitographer as mtgrapher ``

`` import mitopca as mtpca``

**4. Run the analysis of choice.**

&nbsp;

# What MitoScripts Can Do

##  <a name="mtgrapher"></a> MitoGrapher module

This is the most self-explainatory MitoScripts module. Interface with it to produce automated graphs based on your MitoGraph outputs, *.gnet* and *.mitograph* files.

`create_graph_suite` takes `data_dir`, `data_name`, `name_dict`, and `savefigs`. Produces a scattered box plot graph for a plethora of quantifiable metrics from MitoGraph. This function **returns a Pandas DataFrame** containing the extracted metrics. **Keep this DataFrame for downstream analysis.**

* `data_dir`: the directory of your *.gnet* and *.mitograph* files.
* `data_name`: a user-defined name unique to the experiment (for example, "20oct19_treatment_with_chemical_x")
* `name_dict`: a [user-defined dictionary that maps your filenames to their respective labels](#name_dic).
* `savefigs`: set this to `True` to save figures inside of your current directory.


`pca_suite` takes `df`, or the DataFrame returned by `create_graph_suite`, and runs a PCA analysis. It also creates a scree plot and a centroid plot (where the centroid of each cluster is graphed instead of the points). It takes `df`, `to_drop`, and `style`.

* `df`: as explained above
* `to_drop`: defaults to None. If None, will initialize to the automated output of `get_default_col_to_drop`. This removes 1) redundant metrics and 2) irrevelant metrics. Set to a user-defined list if you want to customize the metrics used by MitoPCA.

* `style`: defaults to "tableau-colorblind10", a Seaborn style, as defined in the global variable `DEFAULT_STYLE`. 

`scatter_length_distribution` takes `data_dir`, `data_name`, `name_dict`, and `savefigs`. Variable definitions are the same as above. This function will create a heatmap that displays the individual distributions of each image to visualize distribution of lengths in each image's greater mitochondrial network.


 ## <a name="mt"></a>  MitoData module

This is the main backbone of the MitoGrapher module. Of note, there may be one function you'd interface with:

`analyze_images` takes `data_dir`, `name_dict`, and `data_name` and produces the `df` explained above.

 ##  <a name="mitopca"></a> MitoPCA module

This module is the backbone of `mitographer.pca_suite`. There is one notable function:

`run_special_pca` uses an algorithm to drop columns producing the most dissimilarity in the data, then displays the resultant data's PCA graph. It takes `df`, `threshold`, `min_cols`.

`threshold` and `min_cols` work in tandem. They define two different conditions that the algorithm will stop. `threshold` defines the max cutoff for PC 1's explained variance ratio, while `min_cols` defines the min number of columns in `df` you wish to keep in the final DataFrame. 

For example, let's say I have a DataFrame with 20 columns. The algorithm will start deleting columns that produce the most dissimiliarity. If deleting a column makes PC1's explanied variance ratio greater than `threshold`, it will stop deleting columns, then run a final PCA.

If `threshold` is not met, then the loop will continue.

Simiarly, the algorithm checks each loop if you've whittled the DataFrame down below `min_cols`. If so, the algorithm will also stop deleting columns and run a final PCA.

&nbsp;


# Other Things

### A longer description on `name_dict`

 <a name="name_dic"></a> `name_dict` has key:value pairs as filename:treatment_name. For example, lets say you're treating cells with hydrogen peroxide and seeing if there is a change in mitochondrial morphology. You need to save your images in the form of "control_000", "control_001", "control_nnn" and "h2o2_000", "h2o2_001", "h2o2_nnn", then create a name_dict like so: 

``
name_dict = {
    'control':'Control Group',
    'h2o2':'With Hydrogen Peroxide'
}
``

This way, your graphs and variables will be displayed with the nicer headers "Control Group" and "With Hydrogen Peroxide."

---

### Extended notes for each step

[For Step 1](#step1): 
Read the papers on MitoGraph (namely [this one](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6322684/)) to follow best imaging practices for good MitoGraph results. 

[For Step 2](#step2): 
If you wish to use the normal MitoGraph pipeline, please see [MitoGraph's github repo](https://github.com/vianamp/MitoGraph) for procedure. You may skip to the next step.

Otherwise, if curious, I have provided here my own ImageJ macros based upon those supplied by Matheus that were useful in my pipeline. In order of use: 

*Tiff_and_MaxProfs.ijm*: This macro takes a directory of *.nd2* files, the output of our confocal microscope, and produces a *.tif* image for each file. Next, it take sthe *.tif* files and produces a new z-stack containing max projections of each image. *Use case:* In the MitoGraph pipeline, you need to create such a z-stack to assist in cropping out individual cells from each image.

*CropCells_Complete.ijm*: This macro takes a directory containing the *.tif* files from above, the max projection from above, and an ROISet.zip file containing ROIs for each cell (user-defined) and crops out the ROIs, creating one new *.tif* image per ROI. *Use case:* In my pipeline, I need not only a directory containing each one file per cell ROI, as is used in the normal MitoGraph pipeline, but also a directory of directories where each directory contains a single ROI. This extra "directory of directories" is used on the compute cluster offered at my institution.

*createMontage.ijm*: This macro creates a montage directly comparing the *.png* file output from MitoGraph (which displays the mitochondrial segmentation) to the original *.tif* for manual quality control. *Use case:* Post-MitoGraph processing, use this to see if any catastrophic segmentation errors occured.

---

**Dependencies**: 'numpy', 'pandas', 'scikit-learn', 'igraph', 'matplotlib', 'seaborn'. Please import these into your environment.

