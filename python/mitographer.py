import seaborn as sns
import matplotlib.pyplot as plt

def scattered_box_plot(data, column, sample_order, data_name=""):

    sns.set(style="ticks")

    # Initialize the figure with a logarithmic x axis
    f, ax = plt.subplots(figsize=(7, 6))

    # Load the example planets dataset

    # Plot the orbital period with horizontal boxes
    sns.boxplot(
        x="Conditions",
        y=column,
        data=data,
        order=sample_order,
        whis="range",
        palette="vlag",
    )

    # Add in points to show each observation
    sns.swarmplot(
        x="Conditions",
        y=column,
        data=data,
        order=sample_order,
        size=2,
        color=".3",
        linewidth=0,
    )

    # Tweak the visual presentation
    ax.xaxis.grid(True)
    ax.set(ylabel=column, title=" ".join([data_name, column]))
    sns.despine(trim=True, left=True)
    plt.xticks(rotation=45)
    plt.show()

    return f


def scatter_plot(**kwargs):
    fig = plt.figure(figsize=(5, 5))
    sns.scatterplot(**kwargs)
    plt.ylim(-3, 3)
    plt.xlim(-3, 3)
    plt.title("{x} vs {y}".format(**kwargs))
    plt.show()