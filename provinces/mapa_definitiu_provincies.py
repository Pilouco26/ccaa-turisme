import folium
import webbrowser
import geopandas as gpd
import json

# Function to load the tourism data from the file (you'll need to implement this if not already done)
from espanya.visualize import load_data_from_file

# Load the tourism data into a dictionary
data = load_data_from_file('data_provincia.txt')

# Round the number of tourists to the nearest million
data = {k: round(v) for k, v in data.items()}

# Load the GeoJSON file with correct utf-8 encoding
with open('../maps/spain2.geojson', encoding='utf-8') as f:
    geojson_data = json.load(f)

# Load the GeoDataFrame from the GeoJSON file
es_gdf = gpd.read_file('../maps/spain2.geojson')

# Add the tourists data to the GeoDataFrame
es_gdf['Tourists'] = es_gdf['provincia'].map(data)

# Determine the maximum number of tourists (for scaling the map if needed)
max_tourists = es_gdf['Tourists'].max()

# Create a Folium map centered on Spain
m = folium.Map(location=[41.3851, 2.1734], zoom_start=8)

# Add the Choropleth layer to the map with a different color scale
folium.Choropleth(
    geo_data=geojson_data,  # Use the loaded GeoJSON data
    name='choropleth',
    data=es_gdf,
    columns=['provincia', 'Tourists'],
    key_on='feature.properties.provincia',  # Ensure the property matches your GeoJSON structure
    fill_color='YlOrRd',  # Change the color scale to Yellow-Orange-Red
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Number of Tourists (in millions)'
).add_to(m)

# Add a title to the map
title_html = '''
             <h3 align="center" style="font-size:20px"><b>¿Qué visitan los españoles?</b></h3>
             '''
m.get_root().html.add_child(folium.Element(title_html))

# Save the map to an HTML file
html_file = 'spain_map.html'
m.save(html_file)

# Open the HTML file in the default web browser
webbrowser.open(html_file)

print("Interactive map created and saved as spain_map.html")
