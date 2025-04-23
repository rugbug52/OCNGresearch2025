###### MUST RUN IN ARCFIBER ENVIRONMENT ########

###OLD, NO STORAGE SPACE###

import arcpy
import os
import requests
from datetime import datetime, timedelta
from tqdm import tqdm

# === USER CONFIGURATION ===
start_date_str = "2018-01-05"
end_date_str   = "2024-12-31" 
output_dir     = "C:/Users/rugbug/Documents/OCNGresearch/chloro_erddap_files_all"
output_gdb     = "C:/Users/rugbug/Documents/ArcGIS/Projects/Whales/ChloroNew.gdb"





# NetCDF variable and dimension names
#Needs to be changed depending on what variable is present in your NetCDF file
variable = "chlor_a"
x_dim = "longitude"
y_dim = "latitude"
time_dim = "time"

# === BASE URL COMPONENTS ===
base_url = "https://coastwatch.pfeg.noaa.gov/erddap/griddap/noaacwNPPN20S3ASCIDINEOF2kmDaily.nc"

# These parts stay fixed
params = (
    "?chlor_a%5B({date}T12:00:00Z)%5D%5B(0.0)%5D%5B(-29.98959):(-54.98959)%5D%5B(-69.98959):(-45.01041)%5D"
    "&.draw=surface"
    "&.vars=longitude%7Clatitude%7Cchlor_a"
    "&.colorBar=%7C%7C%7C%7C%7C"
    "&.bgColor=0xffccccff"
)

# === SETUP ===
start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
os.makedirs(output_dir, exist_ok=True)

# === Download and Process Loop ===
dates = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

print("\n Starting download + raster conversion...\n")
for current_date in tqdm(dates, desc="Processing SST data"):
    date_str = current_date.strftime("%Y-%m-%d")
    filename = f"sst_{date_str}.nc"
    output_path = os.path.join(output_dir, filename)

    # === DOWNLOAD ===
    if not os.path.exists(output_path):
        try:
            full_url = base_url + params.format(date=date_str)
            response = requests.get(full_url, stream=True)
            if response.status_code == 200:
                with open(output_path, 'wb') as f:
                    f.write(response.content)
            else:
                tqdm.write(f"❌ Failed download: {date_str}, HTTP {response.status_code}")
                continue
        except Exception as e:
            tqdm.write(f"🚫 Download error for {date_str}: {e}")
            continue

    # === ARCPY CONVERSION ===
    try:
        layer_name = filename.replace("-", "_").removesuffix(".nc")

        arcpy.md.MakeNetCDFRasterLayer(
            in_netCDF_file=output_path,
            variable=variable,
            x_dimension=x_dim,
            y_dimension=y_dim,
            out_raster_layer=layer_name,
            band_dimension=time_dim,
            dimension_values="",
            value_selection_method="BY_VALUE"
        )

        out_raster_path = os.path.join(output_gdb, layer_name)
        arcpy.management.CopyRaster(layer_name, out_raster_path, nodata_value="NaN")
    except Exception as e:
        tqdm.write(f"⚠️ ArcPy error on {filename}: {e}")
        continue

print("\n✅ Finished downloading and converting all rasters.")

