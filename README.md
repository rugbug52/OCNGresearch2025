# NOAA-ERDDAP-Downloads

To download the data, rasterize it and export to an Esri file Geodatabase, run the 

Start by changing the start/end date and the output directory. In ArcGIS Pro,, create a file Geodatabase on your machine and copy that path into the variable. 
To change from chlorophyll to SST, change the "NetCDF dimension and variable names" to match the params from the sensor on the NOAA website.
You need to find your sensor on NOAAs website, then copy the URL into "base_url"
You also need to change the "params" varibale but this can be easily done by copying the query part of the NOAA URL

