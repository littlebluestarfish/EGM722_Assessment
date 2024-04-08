import rasterio
import numpy as np
import matplotlib.pyplot as plt

def calculate_ndvi(red_band, nir_band):
    """Calculate NDVI."""
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    return ndvi

def plot_ndvi(ndvi, transform):
    """Plot NDVI."""
    plt.imshow(ndvi, cmap='RdYlGn')
    plt.colorbar(label='NDVI')
    plt.title('Normalized Difference Vegetation Index')
    plt.xlabel('Column #')
    plt.ylabel('Row #')
    plt.grid(False)
    plt.show()

def main():
    # Path to the red and near-infrared bands of the aerial imagery
    red_band_path = 'C:/Users/Mervyn Boyle/Documents/GitHub/EGM722_Assessment/NIR_Sheet_162/162_16_2022a_4BAND.tif'
    nir_band_path = 'C:/Users/Mervyn Boyle/Documents/GitHub/EGM722_Assessment/NIR_Sheet_162/162_16_2022a_4BAND.tif'

    # Open the red and near-infrared bands
    with rasterio.open(red_band_path) as red_band_src:
        red_band = red_band_src.read(1, masked=True)  # Read the band as a numpy array
        red_meta = red_band_src.meta
        red_transform = red_band_src.transform

    with rasterio.open(nir_band_path) as nir_band_src:
        nir_band = nir_band_src.read(1, masked=True)  # Read the band as a numpy array
        nir_meta = nir_band_src.meta
        nir_transform = nir_band_src.transform

    # Check if both bands have the same dimensions
    if red_band.shape != nir_band.shape:
        raise ValueError("Red and NIR bands have different dimensions.")

    # Calculate NDVI
    ndvi = calculate_ndvi(red_band.astype(np.float32), nir_band.astype(np.float32))

    # Plot NDVI
    plot_ndvi(ndvi, red_transform)

if __name__ == "__main__":
    main()
