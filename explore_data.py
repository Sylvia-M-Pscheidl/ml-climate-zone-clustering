import rasterio as rio
import numpy as np

file_path = 'data/koppen_geiger_reclass.tif'

#Print number of raster cells per climate zone
with rio.open(file_path) as raster:
    data = raster.read(1)
    unique_values, counts = np.unique(data, return_counts=True)

    for value, count in zip(unique_values, counts):
        print(f"Climate Zone: {value} -> Cluster Size: {count}")
