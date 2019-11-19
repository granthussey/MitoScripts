import seaborn as sns
import matplotlib.pyplot as plt

def scattered_box_plot(data, column, sample_order):

    sns.set(style="ticks")

    # Initialize the figure with a logarithmic x axis
    f, ax = plt.subplots(figsize=(7, 6))

    # Load the example planets dataset

    # Plot the orbital period with horizontal boxes
    sns.boxplot(
        x="Condition",
        y=column,
        data=data,
        order=sample_order,
        whis="range",
        palette="vlag",
    )

    # Add in points to show each observation
    sns.swarmplot(
        x="Condition",
        y=column,
        data=data,
        order=sample_order,
        size=2,
        color=".3",
        linewidth=0,
    )

    # Tweak the visual presentation
    ax.xaxis.grid(True)
    ax.set(ylabel=column)
    sns.despine(trim=True, left=True)
    plt.xticks(rotation=45)
    plt.show()


