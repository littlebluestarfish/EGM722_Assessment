import rasterio
import numpy as np
import matplotlib.pyplot as plt

def calculate_ndvi(red_band, nir_band):
    """Calculate NDVI."""
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    return ndvi

def plot_ndvi(ndvi):
    """Plot NDVI."""
    plt.imshow(ndvi, cmap='RdYlGn')
    plt.colorbar(label='NDVI')
    plt.title('Normalized Difference Vegetation Index')
    # plt.xlabel('Column #')
    # plt.ylabel('Row #')
    # plt.grid(False)
    plt.show()

def main():
    # Path to the red and near-infrared bands of the aerial imagery
    red_band = [
        'C:/Users/Mervyn Boyle/Documents/GitHub/EGM722_Assessment/NIR_Sheet_162/4BAND_162_2022_1.tif'.format(i) for i in
        range(5, 16)]
    nir_band = [
        'C:/Users/Mervyn Boyle/Documents/GitHub/EGM722_Assessment/NIR_Sheet_162/4BAND_162_2022_1.tif'.format(i) for i in
        range(5, 16)]

    # Initialize an empty list to store NDVI results
    ndvi_results = []

    # Iterate over the image pairs and calculate NDVI
    for red_band, nir_band in zip(red_band, nir_band):
        with rasterio.open(red_band) as red_band_src:
            red_band = red_band_src.read(1)  # Read the band as a numpy array

        with rasterio.open(nir_band) as nir_band_src:
            nir_band = nir_band_src.read(1)  # Read the band as a numpy array

        # Calculate NDVI
        ndvi = calculate_ndvi(red_band, nir_band)
        ndvi_results.append(ndvi)

    # Convert the list of results to a numpy array
    ndvi_results = np.array(ndvi_results)

    # Calculate the mean NDVI across all images
    mean_ndvi = np.mean(ndvi_results, axis=0)

    # Plot the mean NDVI
    plot_ndvi(mean_ndvi)

if __name__ == "__main__":
    main()

    # Open the red and near-infrared bands
# with rasterio.open(red_band_path) as red_band_src:
#   red_band = red_band_src.read(1, masked=True)  # Read the band as a numpy array
#     red_meta = red_band_src.meta
#   red_transform = red_band_src.transform

#   with rasterio.open(nir_band_path) as nir_band_src:
#    nir_band = nir_band_src.read(1, masked=True)  # Read the band as a numpy array
#    nir_meta = nir_band_src.meta
#    nir_transform = nir_band_src.transform

# Check if both bands have the same dimensions
# if red_band.shape != nir_band.shape:
#   raise ValueError("Red and NIR bands have different dimensions.")

# Calculate NDVI
# ndvi = calculate_ndvi(red_band.astype(np.float32), nir_band.astype(np.float32))

# Plot NDVI
# plot_ndvi(ndvi, red_transform)

# if __name__ == "__main__":
# main()
