import json

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import geopandas as gpd
from matplotlib.ticker import FuncFormatter

def load_data_from_file(file):
    source = {}
    with open(file, mode='r', encoding='utf-8') as file:
        for line in file:
            # Each line has the format: "ccaa: tourists"
            ccaa, tourists = line.strip().split(': ')
            source[ccaa] = int(tourists)  # Convert tourists to an integer
    return source


def plot_data_map(data, max_value):
    # Convert the data to a DataFrame
    # Load the map of Spain from the local shapefile
    # Load the map of Spain from the local shapefile
    world = gpd.read_file('../maps/ne_10m_admin_0_countries.shp')
    spain = world[world['NAME'] == "Spain"]

    # Load the JSON data
    with open('../maps/es.json') as f:
        es_data = json.load(f)

    # Convert JSON data to GeoDataFrame
    es_gdf = gpd.GeoDataFrame.from_features(es_data["features"])
    # Fixing the encoding issues in the name column
    es_gdf['name'] = es_gdf['name'].replace({
        'PaÃ­s Vasco': 'País Vasco',
        'CataluÃ±a': 'Cataluña',
        'Aragon': 'Aragón',
        'Navarra, Comunidad Foral de': 'Navarra',
        'AndalucÃ­a': 'Andalucía',
        'Castilla y LeÃ³n': 'Castilla y León'
    })
    # Ensure the coordinate reference system (CRS) matches
    es_gdf.crs = spain.crs
    data_df = pd.DataFrame(list(data.items()), columns=['name', 'value'])
    print(data_df)
    # Merge the data with the GeoDataFrame using the 'name' field
    es_gdf = es_gdf.merge(data_df, on='name', how='left')

    # Define a blue colormap with more shades for better contrast
    blues = LinearSegmentedColormap.from_list('blues', ['#eff3ff', '#bdd7e7', '#6baed6', '#3182bd', '#08519c'])

    # Plot the map with the updated colormap
    fig, ax = plt.subplots(1, 1, figsize=(15, 15))
    spain.plot(ax=ax, color='white', edgecolor='black')

    # Function to format legend labels in millions
    formatter = FuncFormatter(lambda x, _: f'{int(x / 1e6) if x % 1e6 == 0 else x / 1e6}')

    # Plot the subdivisions with the enhanced blue colormap and scale in millions
    # Set vmin and vmax to control the color range
    es_gdf.plot(ax=ax, column='value', legend=True, cmap=blues, vmin=0, vmax=max_value, legend_kwds={
        'shrink': 0.5,  # Shrink the size of the colorbar (scale)
        'aspect': 30  # Control the thickness of the colorbar
    })

    # Remove the x and y axes
    ax.set_axis_off()

    # Add a title to the plot
    ax.set_title('Turismo en España 2023', fontsize=20, weight='bold')

    # Modify the legend to display numbers in millions
    cbar = ax.get_figure().get_axes()[1]  # Get the colorbar axis
    cbar.yaxis.set_major_formatter(formatter)  # Apply the formatter

    # Set the colorbar label to "en millones de personas"
    cbar.set_ylabel('en millones de personas')

    # Save the plot as an image
    plt.savefig('spain_map.png', dpi=300, bbox_inches='tight')
