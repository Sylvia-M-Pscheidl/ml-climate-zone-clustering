import rasterio
import numpy as np


def reclassify_raster(input_raster_path, output_raster_path):
    """
    Reclassifies the pixel values of a raster based on a defined set of rules.
    """
    with rasterio.open(input_raster_path) as src:
        # Read the metadata
        meta = src.meta.copy()

        # Read the raster data from the first band into a numpy array
        data = src.read(1)

        # Get the NoData value
        nodata_value = src.nodata

        # # Reclassification matrix for köppen-geiger map
        # # Subzones get reclassified into five main zones
        #
        # conditions = [
        #     np.isin(data, [1, 2, 3]),
        #     np.isin(data, [4, 5, 6, 7, 8]),
        #     np.isin(data, [9, 10, 11, 12, 13, 14, 15, 16, 17]),
        #     np.isin(data, [18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28]),
        #     np.isin(data, [29, 30])
        # ]
        #
        # # Values for new classes
        # vals = [1, 2, 3, 4, 5]

        # Reclassify cluster results to match köppen-geiger map
        conditions = [
            np.isin(data, [0]),
            np.isin(data, [6, 8]),
            np.isin(data, [5]),
            np.isin(data, [7]),
            np.isin(data, [4]),
            np.isin(data, [1, 3]),
            np.isin(data, [2])
        ]

        # Values for new classes
        # 0: Noise
        # 6: Mixed zones
        vals = [0, 1, 2, 3, 4, 5, 6]

        reclassified_data = np.select(conditions, vals, default=nodata_value)

        # Update the metadata
        meta.update(
            dtype=rasterio.int16,
            nodata=nodata_value
        )

        # Write the reclassified data to a new GeoTIFF file
        with rasterio.open(output_raster_path, 'w', **meta) as dst:
            dst.write(reclassified_data.astype(rasterio.int16), 1)



if __name__ == '__main__':
    INPUT_RASTER = r'../output/cluster_32.tif'
    OUTPUT_RASTER = r'../data/cluster32_reclass.tif'

    reclassify_raster(INPUT_RASTER, OUTPUT_RASTER)