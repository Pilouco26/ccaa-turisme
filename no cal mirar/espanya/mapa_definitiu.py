import folium
import json
import webbrowser
import geopandas as gpd
from visualize import load_data_from_file

# Load the data into the dictionary
data = load_data_from_file('../data/data_tourism')

# Convert tourist numbers to millions and round them
data = {k: round(v / 1_000_000) for k, v in data.items()}

# Load the geojson file into a GeoDataFrame
es_gdf = gpd.read_file('../maps/es.json')

# Correct the region names
es_gdf['name'] = es_gdf['name'].replace({
    'PaÃ­s Vasco': 'País Vasco',
    'CataluÃ±a': 'Cataluña',
    'Aragon': 'Aragón',
    'Navarra, Comunidad Foral de': 'Navarra',
    'AndalucÃ­a': 'Andalucía',
    'Castilla y LeÃ³n': 'Castilla y León'
})

# Add the tourists data to the GeoDataFrame
es_gdf['Tourists'] = es_gdf['name'].map(data)

# Determine the maximum number of tourists
max_tourists = es_gdf['Tourists'].max()

# Define bins for the color scale
bins = [0, max_tourists * 0.25, max_tourists * 0.5, max_tourists * 0.75, max_tourists]

# Convert the corrected GeoDataFrame back to GeoJSON format
geojson_data = json.loads(es_gdf.to_json())

# Create a folium map
m = folium.Map(location=[40.4168, -3.7038], zoom_start=6)

# Add the geojson data to the map with Choropleth
choropleth = folium.Choropleth(
    geo_data=geojson_data,
    name='choropleth',
    data=es_gdf,
    columns=['name', 'Tourists'],
    key_on='feature.properties.name',
    fill_color='Blues',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of Tourists (in millions)',
    bins=bins
).add_to(m)

# Add hover functionality with GeoJson
geojson = folium.GeoJson(
    geojson_data,
    style_function=lambda feature: {
        'fillColor': '#ffffff00',
        'color': '#00000000',
        'weight': 0
    },
    tooltip=folium.GeoJsonTooltip(
        fields=['name', 'Tourists'],
        aliases=['Region:', 'Tourists (millions):'],
        localize=True
    )
).add_to(m)

# Save the map to an HTML file
html_file = 'spain_map.html'
m.save(html_file)

# Open the HTML file in the default web browser
webbrowser.open(html_file)

print("Interactive map created and saved as spain_map.html")
