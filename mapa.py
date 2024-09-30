import json
import os

import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import FuncFormatter

def load_data_from_file():
    source = {}
    with open('data_tourism.txt', mode='r', encoding='utf-8') as file:
        for line in file:
            # Each line has the format: "ccaa: tourists"
            ccaa, tourists = line.strip().split(': ')
            source[ccaa] = int(tourists)  # Convert tourists to an integer
    return source

# Load the map of Spain from the local shapefile
world = gpd.read_file('data/ne_10m_admin_0_countries.shp')
spain = world[world['NAME'] == "Spain"]

# Load the JSON data
with open('data/es.json') as f:
    es_data = json.load(f)

# Convert JSON data to GeoDataFrame
es_gdf = gpd.GeoDataFrame.from_features(es_data["features"])

# Ensure the coordinate reference system (CRS) matches
es_gdf.crs = spain.crs

print("getting data...")
# Load the data into the dictionary
data = load_data_from_file()
print("data fetched")

# Calculate the region with the maximum number of tourists
max_region = max(data, key=data.get)  # Get the region with the max tourists
max_value = data[max_region]  # Get the max number of tourists

# Fixing the encoding issues in the name column
es_gdf['name'] = es_gdf['name'].replace({
    'PaÃ­s Vasco': 'País Vasco',
    'CataluÃ±a': 'Cataluña',
    'Aragon': 'Aragón',
    'Navarra, Comunidad Foral de': 'Navarra',
    'AndalucÃ­a': 'Andalucía',
    'Castilla y LeÃ³n': 'Castilla y León'
})

# Convert the data to a DataFrame
data_df = pd.DataFrame(list(data.items()), columns=['name', 'value'])

# Merge the data with the GeoDataFrame using the 'name' field
es_gdf = es_gdf.merge(data_df, on='name', how='left')

# Define a blue colormap with a smaller range of blues
blues = LinearSegmentedColormap.from_list('blues', ['#deebf7', '#3182bd'])

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
spain.plot(ax=ax, color='white', edgecolor='black')

# Function to format legend labels in millions
formatter = FuncFormatter(lambda x, _: f'{x / 1e6:.1f} millones')

# Plot the subdivisions with the blue colormap and scale in millions
# Set vmin and vmax to control the color range
es_gdf.plot(ax=ax, column='value', legend=True, cmap=blues, vmin=0, vmax=max_value, legend_kwds={
    'shrink': 0.5,  # Shrink the size of the colorbar (scale)
    'aspect': 30    # Control the thickness of the colorbar
})

# Remove the x and y axes
ax.set_axis_off()

# Add a title to the plot
ax.set_title('Turismo registrado en España 2023', fontsize=20, weight='bold')

# Modify the legend to display numbers in millions
cbar = ax.get_figure().get_axes()[1]  # Get the colorbar axis
cbar.yaxis.set_major_formatter(formatter)  # Apply the formatter

# Set the colorbar label to "en millones de personas"
cbar.set_ylabel('en millones de personas')

# Save the plot as an image
plt.savefig('spain_map.png', dpi=300, bbox_inches='tight')
os.startfile('spain_map.png')
# Close the plot to avoid display in interactive environments
plt.close()
