'''
import os
import glob
import fiona
import rasterio
from rasterio.features import geometry_mask

# Assuming `root_folder` is the path to the parent directory containing subfolders
root_folder = '/home/antonimestre/Documents/Tesnime/SiameseSSL-master/SpaceNet7/sn7_train_labels'

# Define the rasterization parameters
out_shape = (512, 512)  # Output raster shape
transform = rasterio.Affine(1, 0, 0, 0, -1, 0)  # Output raster transformation

# Iterate through the subfolders
for subfolder in glob.glob(os.path.join(root_folder, '*')):
    # Check if the subfolder is a directory
    if os.path.isdir(subfolder):
        # Locate the .geojson file in the subfolder
        geojson_file = glob.glob(os.path.join(subfolder, '*.geojson'))
        if geojson_file:
            geojson_file = geojson_file[0]
            # Open the .geojson file with fiona
            with fiona.open(geojson_file, 'r') as src:
                # Read the geometries and transform them to raster shape
                shapes = [feature['geometry'] for feature in src]
                mask = geometry_mask(shapes, out_shape, transform=transform)
                # Create an output raster file with the same name as the .geojson file
                out_raster_file = os.path.splitext(geojson_file)[0] + '.tif'
                # Write the rasterized mask to the output raster file
                with rasterio.open(out_raster_file, 'w', driver='GTiff', width=out_shape[1], height=out_shape[0], count=1, dtype='uint8', transform=transform) as dst:
                    dst.write(mask.astype('uint8'), 1)
                print(f'Rasterized {geojson_file} to {out_raster_file}')




'''

import glob
import os
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
import json

def  raster():
	print("Enetered raster function")
	# Loop through all the GeoJSON files in the specified directory
	for geojson_path in glob.glob('/home/antonimestre/Documents/Tesnime/SiameseSSL-master/SpaceNet7/sn7_train_labels/*/*/labels.geojson'):

	    print("Path: "+geojson_path)
	    # Determine the AOI ID from the GeoJSON file path
	    aoi_id = os.path.basename(os.path.dirname(geojson_path))
	    aoi_id= aoi_id.replace("labels", "source")
	    print("aoi_id: "+aoi_id)

	    # Determine the input mosaic file path from the AOI ID
	    mosaic_path = glob.glob(f'/home/antonimestre/Documents/Tesnime/SiameseSSL-master/SpaceNet7/sn7_train_source/{aoi_id}/mosaic.tif')[0]

	    # Determine the output raster file path based on the GeoJSON file path
	    output_path = os.path.join(os.path.dirname(geojson_path), 'labeled.tif')

	    # Load the GeoJSON file and extract the shapes to be rasterized
	    with open(geojson_path) as f:
	    	shapes = f.read()
	    	print(type(shapes))
	    	shapes = json.loads(shapes)
	    	print(type(shapes))

	    # Load the mosaic file and get its width, height, and resolution
	    with rasterio.open(mosaic_path) as src:
	    	width = src.width
	    	print("width ="+str(width))
	    	height = src.height
	    	print("height ="+str(height))
	    	#res = src.res[0]

	    # Get the bounding box of the shapes
	    minx, miny, maxx, maxy = rasterio.features.bounds(shapes)
	    print(minx)
	    print(miny)
	    print(maxx)
	    print(maxy)

	    # Create a transform from the bounding box, resolution, and output size
	    transform = from_bounds(minx, miny, maxx, maxy, width, height)

	    # Rasterize the shapes to a new array with the same size and resolution as the output raster
	    arr = rasterize(shapes, out_shape=(height, width), transform=transform)

	    # Write the new raster to a GeoTIFF file
	    with rasterio.open(output_path, 'w', driver='GTiff', height=height, width=width, count=1, dtype=arr.dtype, crs='+init=epsg:4326', transform=transform) as dst:
	    	dst.write(arr, 1)


if __name__ == '__main__':
	raster()
	
	
	
	


