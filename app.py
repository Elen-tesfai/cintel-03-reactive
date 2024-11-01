import plotly.express as px
from shiny import reactive
from shiny.express import input, render, ui
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
import seaborn as sns
import matplotlib.pyplot as plt

# Load penguins dataset
penguins_df = load_penguins()

# Set up the UI page options
ui.page_opts(title="Elen's Palmer Penguin Dataset Exploration", fillable=True)

# Create the sidebar for user interaction
with ui.sidebar(open="open"):
    ui.h2("Sidebar", style="font-size: 16px;")
    
    # Dropdown to select attribute
    ui.tags.div(
        ui.input_selectize(
            "selected_attribute",
            "Select Attribute",
            ["bill_length_mm", "flipper_length_mm", "body_mass_g"],
        ),
        style="font-size: 12px;"
    )
    
    # Numeric input for Plotly histogram bins
    ui.tags.div(
        ui.input_numeric("plotly_bin_count", "Plotly Bin Count", 30),
        style="font-size: 12px;"
    )
    
    # Slider for Seaborn histogram bins
    ui.tags.div(
        ui.input_slider(
            "seaborn_bin_count",
            "Seaborn Bin Count",
            1,
            100,
            30,
        ),
        style="font-size: 12px;"
    )
    
    # Checkbox group for selecting species
    ui.tags.div(
        ui.input_checkbox_group(
            "selected_species_list",
            "Select Species",
            ["Adelie", "Gentoo", "Chinstrap"],
            selected=["Adelie"],
            inline=True,
        ),
        style="font-size: 12px;"
    )

# Layout columns for organizing content
with ui.layout_columns():
    # Data Table card
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        async def penguin_datatable():
            return await filtered_data()  # Use filtered data

    # Data Grid card
    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        async def penguin_datagrid():
            return await filtered_data()  # Use filtered data

# Add a reactive calculation to return the original DataFrame
@reactive.calc
async def filtered_data():
    return penguins_df  # Simply return the original DataFrame

# Layout columns for visualizations
with ui.layout_columns():
    # Tabbed tabset card for plots
    with ui.navset_card_tab(id="plot_tabs"):
        # Plotly Histogram tab
        with ui.nav_panel("Plotly Histogram"):

            @render_plotly
            async def plotly_histogram():
                try:
                    data = await filtered_data()  # Get the current data
                    if data.empty:
                        return None
                    plotly_hist = px.histogram(
                        data_frame=data,
                        x=input.selected_attribute(),
                        nbins=input.plotly_bin_count(),
                        color="species",
                        color_discrete_sequence=["#5e4b8a", "#a55e8b", "#d59b84"],
                    ).update_layout(
                        title="Plotly Penguins Data by Attribute",
                        xaxis_title="Selected Attribute",
                        yaxis_title="Count",
                        plot_bgcolor='#ffebee',
                        paper_bgcolor='#ffebee',
                    )
                    return plotly_hist
                except Exception as e:
                    print("Error generating Plotly histogram:", e)
                    return None

        # Seaborn Histogram tab
        with ui.nav_panel("Seaborn Histogram"):

            @render.plot
            async def seaborn_histogram():
                try:
                    data = await filtered_data()
                    if data.empty:
                        return None
                    plt.figure(facecolor='#ffebee')
                    seaborn_hist = sns.histplot(
                        data=data,
                        x=input.selected_attribute(),
                        bins=input.seaborn_bin_count(),
                        color="#5e4b8a",
                    )
                    seaborn_hist.set_title("Seaborn Penguin Data by Attribute")
                    seaborn_hist.set_xlabel("Selected Attribute")
                    seaborn_hist.set_ylabel("Count")
                    plt.gca().set_facecolor('#ffebee')
                    plt.tight_layout()
                    return seaborn_hist
                except Exception as e:
                    print("Error generating Seaborn histogram:", e)
                    return None

        # Plotly Scatterplot tab
        with ui.nav_panel("Plotly Scatterplot"):

            @render_plotly
            async def plotly_scatterplot():
                try:
                    data = await filtered_data()
                    if data.empty:
                        return None
                    plotly_scatter = px.scatter(
                        data_frame=data,
                        x="bill_length_mm",
                        y="bill_depth_mm",
                        color="species",
                        size_max=8,
                        title="Plotly Scatterplot: Bill Depth and Length",
                        labels={
                            "bill_depth_mm": "Bill Depth (mm)",
                            "bill_length_mm": "Bill Length (mm)",
                        },
                        color_discrete_sequence=["#5e4b8a", "#a55e8b", "#d59b84"],
                    ).update_layout(
                        plot_bgcolor='#ffebee',
                        paper_bgcolor='#ffebee',
                    )
                    return plotly_scatter
                except Exception as e:
                    print("Error generating Plotly scatterplot:", e)
                    return None

        # Grouped Bar Plot tab
        with ui.nav_panel("Grouped Bar Plot"):

            @render_plotly
            async def grouped_bar_plot():
                try:
                    data = await filtered_data()
                    if data.empty:
                        return None
                    grouped_bar = px.bar(
                        data_frame=data,
                        x="island",
                        y="bill_length_mm",
                        color="species",
                        barmode="group",
                        title="Average Bill Length by Island",
                        labels={"bill_length_mm": "Average Bill Length (mm)"},
                        color_discrete_sequence=["#5e4b8a", "#a55e8b", "#d59b84"],
                    ).update_layout(
                        plot_bgcolor='#ffebee',
                        paper_bgcolor='#ffebee',
                    )
                    return grouped_bar
                except Exception as e:
                    print("Error generating grouped bar plot:", e)
                    return None
