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

    # Checkbox group for selecting islands
    ui.tags.div(
        ui.input_checkbox_group(
            "selected_island_list",
            "Select Island",
            ["Torgersen", "Biscoe", "Dream"],
            selected=["Torgersen"],
            inline=True,
        ),
        style="font-size: 12px;"
    )

    # User feedback
    ui.tags.div(
        ui.input_text_area("user_feedback", "Leave your feedback (e.g., suggestions, questions):", ""),
        style="font-size: 12px;"
    )
    
    # Submit button for feedback
    ui.tags.div(
        ui.input_action_button("submit_feedback", "Submit Feedback"),
        style="font-size: 12px;"
    )

# Layout columns for organizing content
with ui.layout_columns():
    # Data Table card
    with ui.card():
        ui.card_header("Data Table")

        @render.data_frame
        async def penguin_datatable():
            # Get filtered data
            data = await filtered_data()
            # Get the selected attribute from the input
            selected_attribute = input.selected_attribute()
            # Only show the selected attribute column along with species and island for better clarity
            if selected_attribute in data.columns:
                return data[['species', 'island', selected_attribute]]
            else:
                return data  # Fallback to show all data in case something goes wrong

    # Data Grid card
    with ui.card():
        ui.card_header("Data Grid")

        @render.data_frame
        async def penguin_datagrid():
            # Get filtered data
            data = await filtered_data()
            # Get the selected attribute from the input
            selected_attribute = input.selected_attribute()
            # Only show the selected attribute column along with species and island
            if selected_attribute in data.columns:
                return data[['species', 'island', selected_attribute]]
            else:
                return data  # Fallback to show all data in case something goes wrong

    # Summary Statistics card
    with ui.card():
        ui.card_header("Summary Statistics")

        @render.text
        async def summary_statistics():
            data = await filtered_data()
            if data.empty:
                return "No data available."
            summary = data.describe().to_string()
            return f"Summary Statistics:\n{summary}"

# Add a reactive calculation to return filtered DataFrame
@reactive.calc
async def filtered_data():
    selected_species = input.selected_species_list()
    selected_islands = input.selected_island_list()
    filtered_df = penguins_df

    if selected_species:
        filtered_df = filtered_df[filtered_df['species'].isin(selected_species)]
    
    if selected_islands:
        filtered_df = filtered_df[filtered_df['island'].isin(selected_islands)]

    return filtered_df  # Return filtered DataFrame

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

        # Box Plot tab
        with ui.nav_panel("Box Plot"):

            @render_plotly
            async def box_plot():
                try:
                    data = await filtered_data()
                    if data.empty:
                        return None
                    box_fig = px.box(
                        data_frame=data,
                        x="species",
                        y="bill_length_mm",
                        title="Box Plot of Bill Length by Species",
                        labels={"bill_length_mm": "Bill Length (mm)"},
                    ).update_layout(
                        plot_bgcolor='#ffebee',
                        paper_bgcolor='#ffebee',
                    )
                    return box_fig
                except Exception as e:
                    print("Error generating box plot:", e)
                    return None

# Reactive to handle feedback submission
@reactive.event(input.submit_feedback)
async def handle_feedback():
    feedback = input.user_feedback()
    if feedback:
        print(f"Feedback received: {feedback}")
        # You can store the feedback or process it as needed here
        # For example, save to a file, send to a database, etc.
