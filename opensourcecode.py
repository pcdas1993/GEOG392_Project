#!pip install mapclassify
#!pip install branca

import folium
import geopandas as gpd
import mapclassify as mc
import branca

# Washington, D.C. coordinates
latitude = 38.9072
longitude = -77.0369

# Initialize map
m = folium.Map(location=[latitude, longitude], zoom_start=10, tiles='Stamen Terrain')

shapefile_path = "C:\\Users\\casey\\OneDrive\\Desktop\\GIS Programming Final Project"

gdf = gpd.read_file(shapefile_path)

# Visualized in map
column_name = "Elec_Prod_"

# Classifying the data into 3 classes using Natural Breaks (Jenks) method
breaks = mc.NaturalBreaks(gdf[column_name], k=3).bins
breaks = list(breaks)

if breaks[0] > gdf[column_name].min():
    breaks.insert(0, gdf[column_name].min())
if breaks[-1] < gdf[column_name].max():
    breaks.append(gdf[column_name].max())

# How polygons will look
def style_function(feature):
    value = feature['properties'][column_name]
    
    if value <= breaks[0]:
        return {'fillColor': '#FFFF00', 'fillOpacity': 0.5, 'color': '#000000'}
    elif value <= breaks[1]:
        return {'fillColor': '#FFA500', 'fillOpacity': 0.5, 'color': '#000000'}
    else:
        return {'fillColor': '#FF0000', 'fillOpacity': 0.5, 'color': '#000000'}

# Create chloropleth layer
choropleth = folium.GeoJson(
    data=gdf.to_json(),
    style_function=style_function,
    name='Elec Production in MWh'
).add_to(m)

# Add colors
colors = ['#FFFF00', '#FFA500', '#FF0000']
# Add colormap
cmap = branca.colormap.StepColormap(
    colors,
    vmin=0,  
    vmax=max(breaks), 
    index=breaks,
    caption='Elec Production in MWh'
)

# Add colormap legend to the map
cmap.add_to(m)
m

