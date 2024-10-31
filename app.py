import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from pathlib import Path
import palmerpenguins
import pandas as pd
import matplotlib.pyplot as plt
from shiny import reactive
import seaborn as sns

# Load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# Optional title for the app
app_title = "Elen's Palmer Penguin Dataset Exploration"

@reactive.calc
def dat():
    infile = Path(__file__).parent / "penguins.csv"
    return pd.read_csv(infile)

# Default dataset to be displayed
@reactive.calc
def filtered_data():
    return penguins_df  # Always return the full dataset

with ui.sidebar(bg="#f8f8f8"):
    ui.input_slider("n", "N", 0, 100, 20)
    ui.input_checkbox_group(
        "checkbox_group", 
        "Penguin Species", 
        {
            "Chinstrap": "Chinstrap",
            "Gentoo": "Gentoo",
            "Adelie": "Adelie",
        }
    )
    ui.input_checkbox_group(
        "island_checkbox_group", 
        "Select Islands", 
        {
            "Biscoe": "Biscoe",
            "Dream": "Dream",
            "Torgersen": "Torgersen"
        }
    )

# Main content
ui.page_opts(title=app_title, fillable=True)

with ui.layout_columns():  # Use layout_columns for a grid-like structure
    # Data Frame with Title
    with ui.card():  # Create a card-like frame
        ui.h4("Data Frame Table")  # Smaller title size
        @render.data_frame
        def frame():
            return dat()

    # Flipper Length Distribution
    @render_plotly
    def plotly_flipper_length_histogram():
        return px.histogram(penguins_df, x="flipper_length_mm", color="species", 
                             title="Flipper Length Distribution by Species")

    # Bill Length Distribution
    @render_plotly
    def plotly_bill_length_histogram():
        return px.histogram(penguins_df, x="bill_length_mm", color="species", 
                             title="Bill Length Distribution by Species")

    # Body Mass Distribution
    @render.plot
    def seaborn_body_mass_histogram():
        fig, ax = plt.subplots(figsize=(8, 6))  # Match size with other plots
        sns.histplot(data=penguins_df, x="body_mass_g", hue="species", 
                     multiple="stack",  # Use 'stack' to avoid overlapping
                     bins=15,  # Adjust number of bins
                     ax=ax, 
                     alpha=0.9)  # Set transparency
        ax.set_title("Body Mass Distribution by Species", fontsize=10, fontweight='normal')  # Unbolded title
        ax.set_xlabel("Mass (g)", fontsize=9)  # Smaller xlabel size
        ax.set_ylabel("Count", fontsize=9)  # Smaller ylabel size
        plt.tight_layout()  # Adjust layout for better spacing
        ax.legend(title='Species', labels=['Adelie', 'Gentoo', 'Chinstrap'], loc='upper left', bbox_to_anchor=(1.05, 1))  # Unbolded species names
        return fig

    # Scatter Plot of Flipper Length vs. Bill Length
    @render_plotly
    def plotly_scatterplot():
        return px.scatter(penguins_df, x="flipper_length_mm", y="bill_length_mm", color="species", 
                          title="Flipper Length vs. Bill Length")

    # Pie Chart of Species Distribution
    @render_plotly
    def plotly_species_distribution():
        species_counts = penguins_df['species'].value_counts()
        return px.pie(species_counts, values=species_counts.values, names=species_counts.index,
                      title="Distribution of Penguin Species")
