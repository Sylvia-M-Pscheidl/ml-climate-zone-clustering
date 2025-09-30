import rasterio
from rasterio.warp import reproject, Resampling
import numpy as np


def align_and_stack_rasters(reference_file, file_to_align, stacked_output_file):

    with rasterio.open(reference_file) as src_ref:
        ref_meta = src_ref.meta.copy()
        ref_transform = src_ref.transform
        ref_crs = src_ref.crs
        ref_height = src_ref.height
        ref_width = src_ref.width
        ref_data = src_ref.read(1)

    with rasterio.open(file_to_align) as src_align:
        # New array for aligned raster
        aligned_data = np.zeros((ref_height, ref_width), dtype=ref_meta['dtype'])

        # Reprojection
        reproject(
            source=rasterio.band(src_align, 1),
            destination=aligned_data,
            src_transform=src_align.transform,
            src_crs=src_align.crs,
            dst_transform=ref_transform,
            dst_crs=ref_crs,
            resampling=Resampling.nearest
        )

    # update meta data
    ref_meta.update(count=2)

    # Create new raster stack
    with rasterio.open(stacked_output_file, 'w', **ref_meta) as dst:
        dst.write_band(1, ref_data)
        dst.write_band(2, aligned_data)


if __name__ == '__main__':
    REFERENCE_RASTER = r'../data/koppen_geiger_0p1.tif'
    RASTER_TO_ALIGN = r'../output/cluster_32.tif'
    OUTPUT_STACK_FILE = r'../data_testing/eval_stack_aligned.tif'

    align_and_stack_rasters(REFERENCE_RASTER, RASTER_TO_ALIGN, OUTPUT_STACK_FILE)