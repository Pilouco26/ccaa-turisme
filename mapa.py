import json
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap

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
# Load the data from get_data function
# Load the data into the dictionary
data = load_data_from_file()
print("data fetched")

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

# Define a blue colormap
blues = LinearSegmentedColormap.from_list('blues', ['#deebf7', '#3182bd'])

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(15, 15))
spain.plot(ax=ax, color='white', edgecolor='black')

# Plot the subdivisions with the blue colormap
es_gdf.plot(ax=ax, column='value', legend=True, cmap=blues)

# Save the plot as an image
plt.savefig('spain_map.png', dpi=300, bbox_inches='tight')

# Close the plot to avoid display in interactive environments
plt.close()
