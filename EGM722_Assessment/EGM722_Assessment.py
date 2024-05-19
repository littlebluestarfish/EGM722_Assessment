import os
import numpy as np
import rioxarray as rxr
import matplotlib.pyplot as plt
import rasterio
from matplotlib.colors import LinearSegmentedColormap
from osgeo import gdal  # Import GDAL

# Set GDAL to use exceptions
gdal.UseExceptions()

# Define the directory containing the images
data_dir = "C:/Users/Mervyn Boyle/Documents/GitHub/EGM722_Assessment/NIR_Sheet_162/"

# Loop through the images
for i in range(1, 17):
    # Construct the file path
    file_path = os.path.join(data_dir, f"4BAND_162_2022_{i:02d}.tif")  # Use zero-padding for the file name

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        continue  # Move to the next iteration if the file does not exist

    try:
        # Open raster data
        NIR_Sheet_162_data = rxr.open_rasterio(file_path)

        # Convert to float to avoid type errors
        red_band = NIR_Sheet_162_data.sel(band=4).astype(float)  # Red band is typically band 4 in Landsat data
        nir_band = NIR_Sheet_162_data.sel(band=1).astype(float)  # NIR band is typically band 1 in Landsat data

        # Calculate NDVI
        with np.errstate(divide='ignore', invalid='ignore'):
            NDVI = (nir_band - red_band) / (nir_band + red_band)

        # Normalize NDVI values to the range -1 to 1
        NDVI = np.clip(NDVI, -1, 1)

        # Save NDVI as GeoTIFF with colormap
        output_ndvi_path = os.path.join(data_dir, f"4BAND_162_2022_{i:02d}_ndvi.tif")
        cmap = LinearSegmentedColormap.from_list('ndvi_cmap', [(0.0, 'red'), (0.5, 'yellow'), (1.0, 'green')])
        NIR_Sheet_162_data.rio.to_raster(output_ndvi_path, dtype='float32', indexes=1, colormap=cmap, overwrite=True)

        print(f"NDVI for image {i} saved successfully.")
    except Exception as e:
        print(f"Error processing image {i}: {e}")
