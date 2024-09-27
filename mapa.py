import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd

from parser import get_data, convert_data

# Load the map of Spain from the local shapefile
world = gpd.read_file('data/ne_10m_admin_0_countries.shp')
spain = world[world['NAME'] == "Spain"]




data = get_data()
converted_data = convert_data(data)
print(converted_data)
df = pd.DataFrame(converted_data)

# Plot the map
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
spain.plot(ax=ax, color='white', edgecolor='black')

# Add your data to the map
for idx, row in df.iterrows():
    plt.text(row['longitude'], row['latitude'], row['value'], fontsize=12)

plt.show()
