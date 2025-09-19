# NOAA-ERDDAP-Downloads

To download the data, rasterize it and export to an Esri file Geodatabase, run the "NOAAErdappDownloadand Rasterize.py" script
The script must be run in an ArcPy environment, meaning that your IDE must point to your ArcGIS python evironment when calling for the interpeter. 

Start by changing the start/end date and the output directory. In ArcGIS Pro, create a file Geodatabase (fGDB) on your machine and copy that path into the variable. 
To change from chlorophyll to SST, change the "NetCDF dimension and variable names" to match the params from the sensor on the NOAA website.
You need to find your sensor on NOAAs website, then copy the URL into "base_url"
You also need to change the "params" varibale but this can be easily done by copying the query part of the NOAA URL
The tool is currently set up for chlorophyll

This will create a file geodatabase for the variable you inputted. Change the parameters and re run the tool for SST and you will have both variables. 

Once you have a file Geodatabase for each one, run the "Create Mosaic Dataset" for each, creating a Mosaic Dataset in each of the respective file GDB.
Then run "Add Rasters to Mosaic Dataset" in ArcPro for each Mosaic. Then you are finished.
