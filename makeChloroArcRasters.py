###### MUST RUN IN ARCFIBER ENVIRONMENT ########

import arcpy
import os

# Input folder and output folder
nc_folder = "C:/Users/rugbug/Documents/OCNGresearch/chloro_erddap_files_all" 
output_gdb = "C:/Users/rugbug/Documents/ArcGIS/Projects/Whales/ChloroNew.gdb"  # Save to a file geodatabase

# Variable and dimensions (you must adjust these to your NetCDF's structure)
variable = "chlor_a"
x_dim = "longitude"
y_dim = "latitude"
time_dim = "time"

# List all .nc files
nc_files = [f for f in os.listdir(nc_folder) if f.endswith(".nc")]

for i, nc_file in enumerate(nc_files):
    nc_path = os.path.join(nc_folder, nc_file)
    layer_name = str(nc_file)
    layer_name = layer_name.replace("-","_").removesuffix(".nc")
    print(layer_name)
    
    # Make raster layer from NetCDF
    arcpy.md.MakeNetCDFRasterLayer(
        in_netCDF_file=nc_path,
        variable=variable,
        x_dimension=x_dim,
        y_dimension=y_dim,
        out_raster_layer=layer_name,
        band_dimension=time_dim,
        dimension_values="",
        value_selection_method="BY_VALUE"
    )
    
    # Save the raster permanently to GDB
    out_raster = os.path.join(output_gdb, f"{layer_name}")
    arcpy.management.CopyRaster(layer_name, out_raster)
    
    print(f"Saved raster: {out_raster}")
