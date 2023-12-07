import arcpy
from arcpy.sa import *

# Input and output raster paths
dsm = "C:\\Users\\casey\\OneDrive\\Music\\Documents\\ArcGIS\\Projects\\Solar\\DSM.tif"
solar_radiation = "C:\\Users\\casey\\OneDrive\\Music\\Documents\\ArcGIS\\Projects\\Solar\\Solar.gdb\\solar__rad"
arcpy.env.workspace = "C:\\Users\\casey\\OneDrive\\Music\\Documents\\ArcGIS\\Projects\\Solar\\Solar.gdb"

# Create slope raster
slope_raster = Slope(dsm)
slope_raster.save("Slope_DSM")

# Create aspect raster
aspect_raster = Aspect(dsm)
aspect_raster.save("Aspect_DSM")

# Filter out slopes > 45 degrees
slope_condition = Con(slope_raster <= 45, solar_radiation)
slope_condition.save("Solar_Rad_S")

# Filter out areas with solar radiation less than 800 kWh/m2
solar_condition = Con(slope_condition >= 800, slope_condition)
solar_condition.save("Solar_Rad_S_HS")

# Consider areas with slope <= 10 degrees low slope
low_slope_condition = Con(slope_raster <= 10, solar_condition)
low_slope_condition.save("low_slope_condition")

# Filter out north facing slopes (value < 22.5 or > 337.5)
north_condition = Con(((aspect_raster > 22.5) & (aspect_raster < 337.5)), solar_condition, low_slope_condition)
north_condition.save("Solar_Rad_S_HS_NN")

# Set the stretch type to "Minimum Maximum" for the north_condition raster
north_conditionLayer = arcpy.MakeRasterLayer_management(north_condition, "north_condition")
north_conditionLayer = north_conditionLayer.getOutput(0)
arcpy.ApplySymbologyFromLayer_management(north_conditionLayer, "C:\\Users\\casey\\OneDrive\\Desktop\\GIS Programming Final Project\\Solar_Rad.lyrx")

# Calulate area covered by suitable cells and their average solar radiation (kWh/m2)
arcpy.sa.ZonalStatisticsAsTable(
    in_zone_data="Buildings_with_Address_1",
    zone_field="OBJECTID",
    in_value_raster="north_condition",
    out_table="C:\\Users\\casey\\OneDrive\\Music\\Documents\\ArcGIS\\Projects\\Solar\\Solar.gdb\\Solar_Rad_Tbl",
    ignore_nodata="DATA",
    statistics_type="MEAN",
)

# Join Fields
arcpy.management.JoinField(
    in_data="Buildings_with_Address_1",
    in_field="OBJECTID",
    join_table="Solar_Rad_Tbl",
    join_field="OBJECTID_1",
    fields="AREA;MEAN",
)

Buildings_with_Address = "C:\\Users\\casey\\OneDrive\\Music\\Documents\\ArcGIS\\Projects\\Solar\\Solar.gdb\\Buildings_with_Address_1" 
expression = "AREA_1 >= 30"  

# Perform the selection
arcpy.SelectLayerByAttribute_management(Buildings_with_Address, "NEW_SELECTION", expression)

# Specify the input feature class (Building_Footprints) and the output feature class (Suitable_Buildings)
input_feature_class = "C:\\Users\\casey\\OneDrive\\Music\\Documents\\ArcGIS\\Projects\\Solar\\Solar.gdb\\Buildings_with_Address_1"
output_feature_class = "C:\\Users\\casey\\OneDrive\\Music\\Documents\\ArcGIS\\Projects\\Solar\\Solar.gdb\\Suitable_Buildings"

# Export features using the Export Features tool
arcpy.management.CopyFeatures(input_feature_class, output_feature_class)

# Calculate Usable_SR_MWh field
arcpy.management.AddField("Suitable_Buildings", "Usable_SR_MWh", "DOUBLE")
arcpy.management.CalculateField("Suitable_Buildings", "Usable_SR_MWh", "(!AREA_1! * !MEAN_1!) / 1000", "PYTHON3")

# Calculate Elec_Prod_MWh field
arcpy.management.AddField("Suitable_Buildings", "Elec_Prod_MWh", "DOUBLE")
arcpy.management.CalculateField("Suitable_Buildings", "Elec_Prod_MWh", "!Usable_SR_MWh! * 0.16 * 0.86", "PYTHON3")

#Apply Symbology to new layer
arcpy.management.ApplySymbologyFromLayer(
    in_layer="Suitable_Buildings",
    in_symbology_layer=r"C:\Users\casey\OneDrive\Desktop\GIS Programming Final Project\Suitable_Buildings.lyrx",
    symbology_fields="VALUE_FIELD Elec_Prod_MWh Elec_Prod_MWh",
    update_symbology="DEFAULT"
)


