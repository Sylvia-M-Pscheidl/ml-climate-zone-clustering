import os
import glob
import geopandas as gpd
import rasterio
from rasterio.mask import mask

def clip_rasters_by_geopackage(input_folder, output_folder, geopackage_path):
    """
    Clips all raster (.tif) files in a folder by a mask layer from a GeoPackage.

    Args:
        input_folder (str): Path to the folder containing the input raster files.
        output_folder (str): Path to the folder where clipped rasters will be saved.
        geopackage_path (str): Path to the GeoPackage file (.gpkg) used for clipping.
        layer_name (str, optional): The name of the layer within the GeoPackage to use.
                                    If None, the first layer is used. Defaults to None.
    """
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Read the specific layer from the GeoPackage
    try:
        mask_gdf = gpd.read_file(geopackage_path)
    except Exception as e:
        print(f"Error reading GeoPackage file: {e}")
        return

    # Get the geometries from the GeoDataFrame
    geometries = mask_gdf.geometry

    # Find all .tif files in the input folder
    raster_files = glob.glob(os.path.join(input_folder, '*.tif'))
    if not raster_files:
        print(f"No .tif files found in {input_folder}")
        return

    print(f"Found {len(raster_files)} raster files to clip.")

    # Iterate over each raster file
    for raster_path in raster_files:
        try:
            with rasterio.open(raster_path) as src:
                # Ensure the mask and raster have the same CRS (Coordinate Reference System)
                if src.crs != mask_gdf.crs:
                    print(f"Reprojecting mask CRS from {mask_gdf.crs} to {src.crs}")
                    mask_gdf = mask_gdf.to_crs(src.crs)
                    geometries = mask_gdf.geometry

                # Clip the raster with the mask
                out_image, out_transform = mask(src, geometries, crop=True)
                out_meta = src.meta.copy()

            # Update the metadata of the clipped raster
            out_meta.update({"driver": "GTiff",
                             "height": out_image.shape[1],
                             "width": out_image.shape[2],
                             "transform": out_transform})

            # Define the output path for the clipped raster
            base_name = os.path.basename(raster_path)
            output_path = os.path.join(output_folder, f"clipped_{base_name}")

            # Save the clipped raster
            with rasterio.open(output_path, "w", **out_meta) as dest:
                dest.write(out_image)

            print(f"Successfully clipped {raster_path} to {output_path}")

        except Exception as e:
            print(f"Error processing {raster_path}: {e}")

if __name__ == '__main__':
    # --- PLEASE MODIFY THE PATHS AND LAYER NAME BELOW ---

    # Folder containing your original .tif files
    input_raster_folder = r'../data_north'

    # Folder where the clipped rasters will be saved
    output_clipped_folder = r'../data_north'

    # Path to your GeoPackage file
    mask_geopackage = r'../data/mask_north.gpkg'

    # Name of the layer in the GeoPackage to use for clipping.
    # If your .gpkg has only one layer, you can set this to None.
    #mask_layer_name = 'your_layer_name' # e.g., 'mask_polygon' or None

    clip_rasters_by_geopackage(input_raster_folder,
                               output_clipped_folder,
                               mask_geopackage,
                               )

    print("Clipping process finished.")