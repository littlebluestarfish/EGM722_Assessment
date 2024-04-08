# Loading the necessary libraries
import matplotlib.pyplot as plt
import numpy
import rasterio
import math


# Extracting the data from the red and near-infrared bands
# insp('C:/Users/Mervyn Boyle/Documents/GitHub/EGM722_Assessment/NIR_Sheet_162/62_16_2022a_4BAND.tif')
# filename16 = '162_16_2022a_4BAND.tif'

# importing the image
image_file = 'C:/Users/Mervyn Boyle/Documents/GitHub/EGM722_Assessment/NIR_Sheet_162/162_16_2022a_4BAND.tif'
sat_data = rasterio.open(image_file)


# Calculating the dimensions of the image on earth in metres
width_in_projected_units = sat_data.bounds.right - sat_data.bounds.left
height_in_projected_units = sat_data.bounds.top - sat_data.bounds.bottom

print("Width: {}, Height: {}".format(width_in_projected_units, height_in_projected_units))
print("Rows: {}, Columns: {}".format(sat_data.height, sat_data.width))

# Converting the pixel co-ordinates to longitudes and latitudes
# Upper left pixel
row_min = 0
col_min = 0

# Lower right pixel.  Rows and columns are zero indexing.
row_max = sat_data.height - 1
col_max = sat_data.width - 1

# Transform coordinates with the dataset's affine transformation.
topleft = sat_data.transform * (row_min, col_min)
botright = sat_data.transform * (row_max, col_max)

print("Top left corner coordinates: {}".format(topleft))
print("Bottom right corner coordinates: {}".format(botright))

# Bands
print(sat_data.count)

# sequence of band indexes
print(sat_data.indexes)

# Visualising the Satellite Imagery
# Load the 4 bands into 2d arrays - recall that we previously learned PlanetScope band order is BGRN.
b, g, r, n = sat_data.read()
# Displaying the blue band.

fig = plt.imshow(b)
plt.show()

# Displaying the green band.

fig = plt.imshow(g)
fig.set_cmap('gist_earth')
plt.show()

# Displaying the red band.

fig = plt.imshow(r)
fig.set_cmap('inferno')
plt.colorbar()
plt.show()

# Displaying the infrared band.

fig = plt.imshow(n)
fig.set_cmap('winter')
plt.colorbar()
plt.show()






with rasterio.open(image_file) as src:
    band_red = src.read(3)
with rasterio.open(image_file) as src:
    band_nir = src.read(4)

# Calculating NDVI

# Do not display error when divided by zero
numpy.seterr(divide='ignore', invalid='ignore')

# NDVI
ndvi = (band_nir.astype(float) - band_red.astype(float)) / (band_nir + band_red)

# Checking the range of NDVI values(excluding NaN)
print(numpy.nanmin(ndvi))
print(numpy.nanmax(ndvi))

# Saving the NDVI image
# get the metadata of original GeoTIFF:
meta = src.meta
print(meta)

# get the dtype of our NDVI array:
ndvi_dtype = ndvi.dtype
print(ndvi_dtype)

# set the source metadata as kwargs we'll use to write the new data:
kwargs = meta

# update the 'dtype' value to match our NDVI array's dtype:
kwargs.update(dtype=ndvi_dtype)

# update the 'count' value since our output will no longer be a 4-band image:
kwargs.update(count=1)

# Finally, use rasterio to write new raster file 'data/ndvi.tif':
with rasterio.open('ndvi.tif', 'w', **kwargs) as dst:
    dst.write(ndvi, 1)

# Applying a color scheme to visualize the NDVI values on the new image
from matplotlib import colors

class MidpointNormalize(colors.Normalize):

    def __init__(self, vmin=None, vmax=None, midpoint=None, clip=False):
        self.midpoint = midpoint
        colors.Normalize.__init__(self, vmin, vmax, clip)

    def __call__(self, value, clip=None):
        x, y = [self.vmin, self.midpoint, self.vmax], [0, 0.5, 1]
        return numpy.ma.masked_array(numpy.interp(value, x, y), numpy.isnan(value))

# Interpretation of NDVI
# Set min/max values from NDVI range for image

min = numpy.nanmin(ndvi)
max = numpy.nanmax(ndvi)

# Set our custom midpoint for most effective NDVI analysis
mid = 0.1

# Setting color scheme ref:https://matplotlib.org/users/colormaps.html as a reference
colormap = plt.cm.RdYlGn
norm = MidpointNormalize(vmin=min, vmax=max, midpoint=mid)
fig = plt.figure(figsize=(20, 10))

ax = fig.add_subplot(111)

# Use 'imshow' to specify the input data, colormap, min, max, and norm for the colorbar
cbar_plot = ax.imshow(ndvi, cmap=colormap, vmin=min, vmax=max, norm=norm)

# Turn off the display of axis labels
ax.axis('off')

# Set a title
ax.set_title('Normalized Difference Vegetation Index', fontsize=17, fontweight='bold')

# Configure the colorbar
cbar = fig.colorbar(cbar_plot, orientation='horizontal', shrink=0.65)

# Call 'savefig' to save this plot to an image file
fig.savefig("ndvi-image.png", dpi=200, bbox_inches='tight', pad_inches=0.7)

# let's visualize
plt.show()

# Generating a histogram of NDVI values
# Define a new figure
fig2 = plt.figure(figsize=(20, 10))

# Give this new figure a subplot, which will contain the histogram itself
ax = fig2.add_subplot(111)

# Add a title & (x,y) labels to the plot
plt.title("NDVI Histogram", fontsize=18, fontweight='bold')
plt.xlabel("NDVI values", fontsize=14)
plt.ylabel("Number of pixels", fontsize=14)

# For the x-axis, we want to count every pixel that is not an empty value
x = ndvi[~numpy.isnan(ndvi)]
color = 'g'

# call 'hist` with our x-axis, bins, and color details
ax.hist(x, bins=30, color=color, histtype='bar', ec='black')

# Save the generated figure to an external image file
fig2.savefig("ndvi-histogram.png", dpi=200, bbox_inches='tight', pad_inches=0.5)

plt.show()