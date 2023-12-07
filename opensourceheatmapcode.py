#!pip install leafmap
import leafmap.leafmap as leafmap

filepath = "C:\\Users\\casey\\OneDrive\\Desktop\\GIS Programming Final Project\\Suitable_Buildings_Table_TableToExcel.csv"

m = leafmap.Map()
m.add_basemap("Stamen.Toner")
m.add_heatmap(
    filepath,
    latitude="LATITUDE",
    longitude='LONGITUDE',
    value="Elec_Prod_MWh",
    name="Heat map",
    radius=7.55,
)
m

colors = ['blue', 'lime', 'yellow', 'red']
vmin = 0
vmax = 10

m.add_colorbar(colors=colors, vmin=vmin, vmax=vmax)

